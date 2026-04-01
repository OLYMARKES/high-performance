from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def decode_record_from_issue_body(body: str) -> dict | None:
    match = re.search(r"<!-- lead-data:v1:([^>]+) -->", body or "")
    if not match:
        return None

    try:
        return json.loads(base64.b64decode(match.group(1)).decode("utf-8"))
    except (ValueError, json.JSONDecodeError):
        return None


def normalize_key(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def questionnaire_record_updated_at(record: dict, issue: dict) -> str:
    return str(record.get("submittedAt") or issue.get("updated_at") or "")


def extract_page_filename(page_url: str) -> str:
    if not page_url:
        return ""

    parsed = urlparse(str(page_url))
    return Path(parsed.path).name


def build_lead_email_by_issue(issues: list[dict]) -> dict[int, str]:
    lead_email_by_issue: dict[int, str] = {}

    for issue in issues:
        record = decode_record_from_issue_body(issue.get("body", ""))
        if not record or record.get("kind") != "high-performance-lead":
            continue

        issue_number = issue.get("number")
        if not isinstance(issue_number, int):
            continue

        email = normalize_key(str(record.get("email") or ""))
        if email:
            lead_email_by_issue[issue_number] = email

    return lead_email_by_issue


def _score_questionnaire_match(
    record: dict,
    participant: dict,
    filename: str,
    lead_email_by_issue: dict[int, str],
) -> tuple[int, str]:
    record_email = normalize_key(str(record.get("email") or record.get("responseData", {}).get("participantEmail") or ""))
    record_slug = str(record.get("participantSlug") or "").strip()
    record_filename = extract_page_filename(str(record.get("pageUrl") or ""))
    participant_slug = str(participant.get("slug") or "").strip()
    participant_lead_issue = participant.get("lead_issue")
    participant_email = lead_email_by_issue.get(participant_lead_issue) if isinstance(participant_lead_issue, int) else ""

    best_score = 0
    best_method = ""

    if participant_email and record_email and participant_email == record_email:
        best_score = 1000
        best_method = "lead-email"

    if record_filename and filename and record_filename == filename and best_score < 400:
        best_score = 400
        best_method = "page-url"

    if record_slug and participant_slug and record_slug == participant_slug and best_score < 300:
        best_score = 300
        best_method = "slug"

    return best_score, best_method


def build_questionnaire_match_index(participants: list[dict], issues: list[dict]) -> dict[str, dict]:
    lead_email_by_issue = build_lead_email_by_issue(issues)
    latest_by_slug: dict[str, dict] = {}

    participant_files = {
        participant["slug"]: participant.get("filename") or f"q_{participant['token']}.html"
        for participant in participants
    }

    for issue in issues:
        record = decode_record_from_issue_body(issue.get("body", ""))
        if not record or record.get("kind") != "high-performance-participant-questionnaire":
            continue

        best_participant: dict | None = None
        best_score = 0
        best_method = ""

        for participant in participants:
            score, method = _score_questionnaire_match(
                record=record,
                participant=participant,
                filename=participant_files.get(participant["slug"], ""),
                lead_email_by_issue=lead_email_by_issue,
            )
            if score > best_score:
                best_participant = participant
                best_score = score
                best_method = method

        if not best_participant or best_score <= 0:
            continue

        participant_slug = best_participant["slug"]
        candidate_date = questionnaire_record_updated_at(record, issue)
        existing = latest_by_slug.get(participant_slug)
        existing_date = ""
        if existing:
            existing_date = questionnaire_record_updated_at(existing["record"], existing["issue"])

        if not existing or candidate_date > existing_date:
            latest_by_slug[participant_slug] = {
                "record": record,
                "issue": issue,
                "matchedBy": best_method,
                "score": best_score,
            }

    return latest_by_slug
