from __future__ import annotations

import base64
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = ROOT / "scripts" / "admin_issues_snapshot.json"
OUTPUT_PATH = ROOT / "admissions-dashboard.html"
PRIVATE_REPO = "OLYMARKES/high-performance-leads"
QUESTIONNAIRE_BASE_URL = "https://olymarkes.github.io/high-performance/participant_questionnaires_april_2026"
COURSE_LABELS = {
    "care": "Care",
    "basics": "Basics",
    "superhuman": "SuperHuman",
    "abs": "Пресс",
    "woman-health": "Женское здоровье",
    "soft-power": "Soft Power",
    "stretch": "Растяжка",
    "pregnancy": "Для беременных",
    "mama": "Мама",
    "bed": "Не вставая с кровати",
    "body-contact": "Контакт с телом",
}


def decode_record(body: str) -> dict | None:
    match = re.search(r"<!-- lead-data:v1:([^>]+) -->", body or "")
    if not match:
        return None

    try:
        return json.loads(base64.b64decode(match.group(1)).decode("utf-8"))
    except (ValueError, json.JSONDecodeError):
        return None


def load_issues() -> list[dict]:
    payload = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def label_for_path(value: str) -> str:
    if value == "short":
        return "Короткий"
    if value == "personal":
        return "Персональный"
    return "—"


def label_for_course(value: str) -> str:
    return COURSE_LABELS.get(value, value or "")


def normalize_key(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def format_timestamp(value: str) -> str:
    if not value:
        return "—"

    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value

    return dt.strftime("%d.%m.%Y %H:%M UTC")


def build_questionnaire_index(issues: list[dict]) -> dict[str, dict]:
    latest_by_slug: dict[str, dict] = {}

    for issue in issues:
        record = decode_record(issue.get("body", ""))
        if not record or record.get("kind") != "high-performance-participant-questionnaire":
            continue

        slug = str(record.get("participantSlug") or "").strip()
        if not slug:
            continue

        current_date = str(record.get("submittedAt") or issue.get("updated_at") or "")
        existing = latest_by_slug.get(slug)
        existing_date = ""
        if existing:
            existing_record = existing["record"]
            existing_issue = existing["issue"]
            existing_date = str(existing_record.get("submittedAt") or existing_issue.get("updated_at") or "")

        if not existing or current_date > existing_date:
            latest_by_slug[slug] = {"record": record, "issue": issue}

    return latest_by_slug


def build_lead_index(issues: list[dict]) -> tuple[dict[int, dict], dict[str, dict], dict[str, dict]]:
    leads_by_issue: dict[int, dict] = {}
    leads_by_contact: dict[str, dict] = {}
    leads_by_name: dict[str, list[dict]] = {}

    for issue in issues:
        record = decode_record(issue.get("body", ""))
        if not record or record.get("kind") != "high-performance-lead":
            continue

        lead_name = str(record.get("name", "")).strip()
        contact = str(record.get("contact", "")).strip()
        if "smoke" in normalize_key(lead_name) or "smoke" in normalize_key(contact):
            continue

        lead = {
            "issueNumber": issue.get("number"),
            "issueUrl": issue.get("html_url", ""),
            "submittedAt": record.get("submittedAt") or issue.get("created_at") or "",
            "submittedAtLabel": format_timestamp(str(record.get("submittedAt") or issue.get("created_at") or "")),
            "name": lead_name,
            "contact": contact,
            "email": record.get("email", ""),
            "about": record.get("about", ""),
        }

        issue_number = issue.get("number")
        if isinstance(issue_number, int):
            leads_by_issue[issue_number] = lead

        contact_key = normalize_key(contact)
        if contact_key and contact_key not in leads_by_contact:
            leads_by_contact[contact_key] = lead

        name_key = normalize_key(lead_name)
        if name_key:
            leads_by_name.setdefault(name_key, []).append(lead)

    unique_leads_by_name = {name: items[0] for name, items in leads_by_name.items() if len(items) == 1}
    return leads_by_issue, leads_by_contact, unique_leads_by_name


def stage_for_row(row: dict) -> str:
    if row["courseOpened"]:
        return "course-opened"
    if row["questionnaireFilled"]:
        return "questionnaire"
    if row["paid"]:
        return "paid"
    if row["leadSubmitted"]:
        return "lead"
    return "other"


def build_rows() -> tuple[list[dict], str]:
    issues = load_issues()
    snapshot_time = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    participants = get_participants()
    questionnaire_index = build_questionnaire_index(issues)
    leads_by_issue, leads_by_contact, unique_leads_by_name = build_lead_index(issues)
    participant_name_counts: dict[str, int] = {}
    for participant in participants:
        key = normalize_key(participant["name"])
        participant_name_counts[key] = participant_name_counts.get(key, 0) + 1

    rows: list[dict] = []
    used_lead_issue_numbers: set[int] = set()
    used_lead_contacts: set[str] = set()
    used_unique_names: set[str] = set()

    for participant in participants:
        lead = None
        lead_issue = participant.get("lead_issue")
        if isinstance(lead_issue, int):
            lead = leads_by_issue.get(lead_issue)
        if not lead:
            lead = leads_by_contact.get(normalize_key(participant["telegram_handle"]))
        participant_name_key = normalize_key(participant["name"])
        if not lead and participant_name_counts.get(participant_name_key) == 1:
            lead = unique_leads_by_name.get(participant_name_key)

        if lead and isinstance(lead.get("issueNumber"), int):
            used_lead_issue_numbers.add(int(lead["issueNumber"]))
        if lead and lead.get("contact"):
            used_lead_contacts.add(normalize_key(str(lead["contact"])))
        if participant_name_counts.get(participant_name_key) == 1 and participant_name_key:
            used_unique_names.add(participant_name_key)

        questionnaire_match = questionnaire_index.get(participant["slug"])
        record = questionnaire_match["record"] if questionnaire_match else {}
        issue = questionnaire_match["issue"] if questionnaire_match else {}
        response_data = record.get("responseData", {}) if isinstance(record, dict) else {}
        vip = response_data.get("vip", {}) if isinstance(response_data, dict) else {}
        selected_course = str(record.get("courseChoice") or response_data.get("courseChoice") or "")
        selected_path = str(record.get("selectedPath") or response_data.get("selectedPath") or "")
        personal_context = str(record.get("personalContext") or response_data.get("personalContext") or "")
        resolved_email = str(record.get("email") or response_data.get("participantEmail") or (lead.get("email", "") if lead else ""))
        resolved_updated_at = str(record.get("submittedAt") or issue.get("updated_at") or (lead.get("submittedAt", "") if lead else ""))

        ready_to_open = bool(selected_course) and not participant["course_opened"]
        needs_pick = bool(not selected_course and (selected_path == "personal" or personal_context.strip()))

        rows.append(
            {
                "rowId": participant["slug"] or f"participant-{participant['token']}",
                "slug": participant["slug"],
                "displayName": participant["display_name"],
                "telegramHandle": participant["telegram_handle"],
                "leadSubmitted": bool(lead),
                "paid": bool(participant["paid"]),
                "questionnaireFilled": bool(questionnaire_match),
                "courseOpened": bool(participant["course_opened"]),
                "openedCourse": participant.get("opened_course", "") or label_for_course(selected_course),
                "needsPick": needs_pick,
                "readyToOpen": ready_to_open,
                "selectedCourse": selected_course,
                "selectedCourseLabel": label_for_course(selected_course) or "—",
                "selectedPathLabel": label_for_path(selected_path),
                "leadIssueNumber": lead.get("issueNumber") if lead else participant.get("lead_issue"),
                "leadIssueUrl": lead.get("issueUrl", "") if lead else (
                    f"https://github.com/{PRIVATE_REPO}/issues/{participant['lead_issue']}" if participant.get("lead_issue") else ""
                ),
                "questionnaireIssueNumber": issue.get("number", ""),
                "questionnaireIssueUrl": issue.get("html_url", ""),
                "questionnaireUrl": f"{QUESTIONNAIRE_BASE_URL}/q_{participant['token']}.html",
                "email": resolved_email,
                "updatedAt": resolved_updated_at,
                "updatedAtLabel": format_timestamp(resolved_updated_at),
                "leadAbout": lead.get("about", "") if lead else "",
                "summary": {
                    "visionFuture": response_data.get("visionFuture", ""),
                    "personalContext": personal_context,
                    "purpose": vip.get("purpose", ""),
                    "healthRestrictions": vip.get("healthRestrictions", ""),
                    "nutritionFlags": vip.get("nutritionFlags", []),
                    "foodHabits": vip.get("foodHabits", ""),
                    "medications": vip.get("medications", ""),
                    "curatorMessage": vip.get("curatorMessage", ""),
                },
            }
        )

    for issue_number, lead in leads_by_issue.items():
        if issue_number in used_lead_issue_numbers:
            continue
        if lead.get("contact") and normalize_key(str(lead["contact"])) in used_lead_contacts:
            continue
        if normalize_key(str(lead["name"])) in used_unique_names:
            continue

        rows.append(
            {
                "rowId": f"lead-{issue_number}",
                "slug": "",
                "displayName": lead["name"] or lead["contact"] or f"Lead #{issue_number}",
                "telegramHandle": lead["contact"] or "—",
                "leadSubmitted": True,
                "paid": False,
                "questionnaireFilled": False,
                "courseOpened": False,
                "openedCourse": "",
                "needsPick": False,
                "readyToOpen": False,
                "selectedCourse": "",
                "selectedCourseLabel": "—",
                "selectedPathLabel": "—",
                "leadIssueNumber": issue_number,
                "leadIssueUrl": lead["issueUrl"],
                "questionnaireIssueNumber": "",
                "questionnaireIssueUrl": "",
                "questionnaireUrl": "",
                "email": lead["email"],
                "updatedAt": lead["submittedAt"],
                "updatedAtLabel": lead["submittedAtLabel"],
                "leadAbout": lead["about"],
                "summary": {
                    "visionFuture": "",
                    "personalContext": "",
                    "purpose": "",
                    "healthRestrictions": "",
                    "nutritionFlags": [],
                    "foodHabits": "",
                    "medications": "",
                    "curatorMessage": "",
                },
            }
        )

    stage_priority = {
        "lead": 0,
        "paid": 1,
        "questionnaire": 2,
        "course-opened": 3,
    }

    def sort_key(row: dict) -> tuple[int, int, int, float, str]:
        stage = stage_for_row(row)
        if row["needsPick"]:
            action_priority = 0
        elif row["readyToOpen"]:
            action_priority = 1
        elif row["paid"] and not row["questionnaireFilled"]:
            action_priority = 2
        elif row["leadSubmitted"] and not row["paid"]:
            action_priority = 3
        else:
            action_priority = 4

        timestamp = 0.0
        if row["updatedAt"]:
            try:
                timestamp = datetime.fromisoformat(str(row["updatedAt"]).replace("Z", "+00:00")).timestamp()
            except ValueError:
                timestamp = 0.0

        return (
            action_priority,
            stage_priority.get(stage, 9),
            0 if row["paid"] else 1,
            -timestamp,
            str(row["displayName"]),
        )

    rows.sort(key=sort_key)
    return rows, snapshot_time


def script_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def build_html(rows: list[dict], snapshot_time: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>High Performance - Admissions Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #0d1110;
      --surface: #151a19;
      --surface-alt: #111615;
      --border: #28302e;
      --text: #edf0ed;
      --muted: #96a29d;
      --accent: #d4a25f;
      --green: #8cc68c;
      --yellow: #f0c36f;
      --radius: 18px;
    }}
    body {{
      background:
        radial-gradient(circle at top left, rgba(212, 162, 95, 0.08), transparent 28%),
        linear-gradient(180deg, #0b0f0e 0%, #101514 100%);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      padding: 28px 16px 56px;
    }}
    .page {{ max-width: 1360px; margin: 0 auto; }}
    .hero {{
      text-align: center;
      padding: 24px 0 30px;
    }}
    .hero-label {{
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.34em;
      font-size: 11px;
      font-weight: 600;
    }}
    h1 {{
      margin-top: 22px;
      font-family: 'Playfair Display', serif;
      font-size: clamp(44px, 9vw, 72px);
      line-height: 0.98;
      font-weight: 400;
    }}
    h1 em {{ color: var(--accent); font-style: italic; }}
    .hero-sub {{
      max-width: 860px;
      margin: 18px auto 0;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.8;
    }}
    .panel {{
      background: rgba(21, 26, 25, 0.92);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px;
      margin-top: 18px;
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18);
      backdrop-filter: blur(8px);
    }}
    .snapshot {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }}
    .snapshot strong {{ color: var(--text); }}
    .search {{
      width: 100%;
      margin-top: 16px;
      padding: 14px 16px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: var(--surface-alt);
      color: var(--text);
      font: inherit;
    }}
    .filters, .status-filters {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }}
    .chip {{
      border: 1px solid var(--border);
      border-radius: 999px;
      background: transparent;
      color: var(--text);
      padding: 11px 16px;
      font: inherit;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      cursor: pointer;
    }}
    .chip.is-active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #171310;
      font-weight: 600;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 14px;
    }}
    .stat {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 18px;
    }}
    .stat-label {{
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.14em;
    }}
    .stat-value {{
      margin-top: 8px;
      font-family: 'Playfair Display', serif;
      font-size: 38px;
      line-height: 1;
    }}
    .queues {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }}
    .queue {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 18px;
    }}
    .queue h2 {{
      font-family: 'Playfair Display', serif;
      font-size: 28px;
      line-height: 1.05;
      font-weight: 400;
    }}
    .queue p {{
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }}
    .queue-list {{
      display: grid;
      gap: 10px;
      margin-top: 18px;
    }}
    .queue-item {{
      padding: 12px 13px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: #0f1312;
    }}
    .queue-name {{ font-weight: 600; }}
    .queue-meta {{
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.6;
    }}
    .empty-note {{ color: var(--muted); font-size: 13px; }}
    .table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: 16px;
      margin-top: 18px;
    }}
    table {{
      width: 100%;
      min-width: 1320px;
      border-collapse: collapse;
      background: var(--surface-alt);
    }}
    th, td {{
      text-align: left;
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
      font-size: 14px;
    }}
    th {{
      color: var(--accent);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.16em;
    }}
    .name {{
      font-weight: 600;
      display: block;
    }}
    .meta {{
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }}
    .links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 8px;
    }}
    .link, .link:visited {{
      color: var(--accent);
      text-decoration: none;
      font-size: 12px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 7px 11px;
      font-size: 12px;
      border: 1px solid var(--border);
      white-space: nowrap;
      margin-right: 6px;
      margin-bottom: 6px;
    }}
    .badge.ok {{
      color: var(--green);
      border-color: rgba(140, 198, 140, 0.4);
      background: rgba(140, 198, 140, 0.08);
    }}
    .badge.todo {{
      color: var(--yellow);
      border-color: rgba(240, 195, 111, 0.35);
      background: rgba(240, 195, 111, 0.08);
    }}
    .badge.muted {{ color: var(--muted); }}
    .action-title {{ font-weight: 600; display: block; }}
    .action-note {{
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }}
    .details-btn {{
      background: transparent;
      color: var(--accent);
      border: 1px solid rgba(212, 162, 95, 0.28);
      border-radius: 999px;
      padding: 8px 12px;
      font: inherit;
      font-size: 12px;
      cursor: pointer;
    }}
    .details-btn.is-muted {{
      color: var(--muted);
      border-color: var(--border);
    }}
    .button-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .modal {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(6, 8, 8, 0.78);
      padding: 24px;
      overflow: auto;
      z-index: 100;
    }}
    .modal.visible {{ display: block; }}
    .modal-card {{
      max-width: 860px;
      margin: 36px auto;
      background: #0f1312;
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 24px;
    }}
    .modal-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
      margin-bottom: 14px;
    }}
    .modal-title {{
      font-family: 'Playfair Display', serif;
      font-size: 34px;
      line-height: 1.05;
    }}
    .close {{
      background: transparent;
      border: none;
      color: var(--muted);
      font: inherit;
      cursor: pointer;
    }}
    .section {{
      border-top: 1px solid var(--border);
      padding-top: 16px;
      margin-top: 16px;
    }}
    .section h3 {{
      color: var(--accent);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 10px;
    }}
    .section p, .section li {{
      color: var(--muted);
      font-size: 14px;
      line-height: 1.8;
    }}
    .section ul {{ padding-left: 18px; }}
    @media (max-width: 1100px) {{
      .stats, .queues {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 720px) {{
      .stats, .queues {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <div class="hero-label">High Performance</div>
      <h1>Admissions <em>dashboard</em></h1>
      <p class="hero-sub">
        Сквозная воронка по людям: кто оставил заявку, кто уже в программе, кто заполнил анкету и где курс уже открыт.
        Внутри остаются и операционные очереди: кому подобрать курс, кому открыть доступ и кого ещё дожать до анкеты.
      </p>
    </section>

    <section class="panel">
      <div class="snapshot"><strong>Снимок данных:</strong> {format_timestamp(snapshot_time)}. Данные подтянуты из последних GitHub issues и встроены прямо в страницу.</div>
      <div class="snapshot">Скрытие работает локально в этом браузере: можно убирать тех, кто не пошёл, не меняя исходные данные.</div>
      <input class="search" id="search-input" type="text" placeholder="Поиск по имени, Telegram, email, курсу или slug">
      <div class="filters" id="stage-filters">
        <button class="chip is-active" data-stage="all" type="button">Все</button>
        <button class="chip" data-stage="lead" type="button">Заявки</button>
        <button class="chip" data-stage="paid" type="button">Оплатили</button>
        <button class="chip" data-stage="questionnaire" type="button">Анкета</button>
        <button class="chip" data-stage="course-opened" type="button">Курс открыт</button>
      </div>
      <div class="status-filters" id="status-filters">
        <button class="chip is-active" data-status="all" type="button">Все действия</button>
        <button class="chip" data-status="unpaid" type="button">Ждём оплату</button>
        <button class="chip" data-status="waiting-questionnaire" type="button">Ждём анкету</button>
        <button class="chip" data-status="needs-pick" type="button">Подобрать курс</button>
        <button class="chip" data-status="ready-open" type="button">Открыть курс</button>
        <button class="chip" data-status="hidden" type="button">Скрытые</button>
      </div>
    </section>

    <section class="panel">
      <div class="stats">
        <div class="stat"><div class="stat-label">Всего людей</div><div class="stat-value" id="stat-total">0</div></div>
        <div class="stat"><div class="stat-label">Подали заявку</div><div class="stat-value" id="stat-leads">0</div></div>
        <div class="stat"><div class="stat-label">Оплатили</div><div class="stat-value" id="stat-paid">0</div></div>
        <div class="stat"><div class="stat-label">Заполнили анкету</div><div class="stat-value" id="stat-questionnaire">0</div></div>
        <div class="stat"><div class="stat-label">Курс открыт</div><div class="stat-value" id="stat-course-opened">0</div></div>
        <div class="stat"><div class="stat-label">Скрыто</div><div class="stat-value" id="stat-hidden">0</div></div>
      </div>
    </section>

    <section class="panel">
      <div class="queues">
        <div class="queue">
          <h2>Ждём оплату</h2>
          <p>Новые лиды, которые ещё не переведены в список участниц.</p>
          <div class="queue-list" id="queue-unpaid"></div>
        </div>
        <div class="queue">
          <h2>Ждём анкету</h2>
          <p>Участницы уже в программе, но серверной анкеты ещё нет.</p>
          <div class="queue-list" id="queue-waiting-questionnaire"></div>
        </div>
        <div class="queue">
          <h2>Подобрать курс</h2>
          <p>Анкета есть, но курс нужно выбрать вручную по контексту.</p>
          <div class="queue-list" id="queue-needs-pick"></div>
        </div>
        <div class="queue">
          <h2>Открыть курс</h2>
          <p>Участница уже указала курс, осталось открыть доступ.</p>
          <div class="queue-list" id="queue-ready-open"></div>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Человек</th>
              <th>Этапы</th>
              <th>Следующее действие</th>
              <th>Курс / путь</th>
              <th>Email</th>
              <th>Обновлено</th>
              <th>Детали</th>
            </tr>
          </thead>
          <tbody id="results-body"></tbody>
        </table>
      </div>
    </section>
  </div>

  <div class="modal" id="details-modal">
    <div class="modal-card">
      <div class="modal-head">
        <div class="modal-title" id="modal-title">Карточка</div>
        <button class="close" id="close-modal" type="button">закрыть</button>
      </div>
      <div id="modal-content"></div>
    </div>
  </div>

  <script>
    const ALL_ROWS = {script_json(rows)};
    const HIDDEN_KEY = 'hp-admissions-hidden-v1';
    const searchInput = document.getElementById('search-input');
    const stageFilters = document.getElementById('stage-filters');
    const statusFilters = document.getElementById('status-filters');
    const resultsBody = document.getElementById('results-body');
    const queueUnpaid = document.getElementById('queue-unpaid');
    const queueWaitingQuestionnaire = document.getElementById('queue-waiting-questionnaire');
    const queueNeedsPick = document.getElementById('queue-needs-pick');
    const queueReadyOpen = document.getElementById('queue-ready-open');
    const statTotal = document.getElementById('stat-total');
    const statLeads = document.getElementById('stat-leads');
    const statPaid = document.getElementById('stat-paid');
    const statQuestionnaire = document.getElementById('stat-questionnaire');
    const statCourseOpened = document.getElementById('stat-course-opened');
    const statHidden = document.getElementById('stat-hidden');
    const detailsModal = document.getElementById('details-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    const closeModal = document.getElementById('close-modal');

    let activeStage = 'all';
    let activeStatus = 'all';
    let hiddenIds = loadHiddenIds();

    function loadHiddenIds() {{
      try {{
        const raw = localStorage.getItem(HIDDEN_KEY);
        const parsed = raw ? JSON.parse(raw) : [];
        return new Set(Array.isArray(parsed) ? parsed.map((value) => String(value)) : []);
      }} catch (error) {{
        return new Set();
      }}
    }}

    function persistHiddenIds() {{
      localStorage.setItem(HIDDEN_KEY, JSON.stringify([...hiddenIds]));
    }}

    function isHidden(row) {{
      return hiddenIds.has(String(row.rowId));
    }}

    function setRowHidden(row, hidden) {{
      const key = String(row.rowId);
      if (hidden) {{
        hiddenIds.add(key);
      }} else {{
        hiddenIds.delete(key);
      }}
      persistHiddenIds();
      syncPage();
    }}

    function escapeHtml(value) {{
      return String(value || '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;');
    }}

    function paragraph(value) {{
      if (!value) return '<p>—</p>';
      return `<p>${{escapeHtml(String(value)).replaceAll('\\n', '<br>')}}</p>`;
    }}

    function list(values) {{
      if (!values || !values.length) return '<p>—</p>';
      return `<ul>${{values.map((value) => `<li>${{escapeHtml(value)}}</li>`).join('')}}</ul>`;
    }}

    function sectionHtml(title, body) {{
      return `
        <div class="section">
          <h3>${{escapeHtml(title)}}</h3>
          ${{body}}
        </div>
      `;
    }}

    function stageForRow(row) {{
      if (row.courseOpened) return 'course-opened';
      if (row.questionnaireFilled) return 'questionnaire';
      if (row.paid) return 'paid';
      if (row.leadSubmitted) return 'lead';
      return 'other';
    }}

    function statusForRow(row) {{
      if (row.readyToOpen) return 'ready-open';
      if (row.needsPick) return 'needs-pick';
      if (row.paid && !row.questionnaireFilled) return 'waiting-questionnaire';
      if (row.leadSubmitted && !row.paid) return 'unpaid';
      return 'complete';
    }}

    function nextAction(row) {{
      if (row.courseOpened) {{
        return ['Курс уже открыт', row.openedCourse ? `Открыт курс: ${{row.openedCourse}}` : 'Этап закрыт.'];
      }}
      if (row.readyToOpen) {{
        return [`Открыть курс ${{row.selectedCourseLabel}}`, 'Участница уже выбрала курс в анкете.'];
      }}
      if (row.needsPick) {{
        return ['Подобрать курс', 'Нужен ручной выбор курса по анкете.'];
      }}
      if (row.paid && !row.questionnaireFilled) {{
        return ['Напомнить про анкету', 'Оплата есть, но анкета ещё не сохранена.'];
      }}
      if (row.leadSubmitted && !row.paid) {{
        return ['Довести до оплаты', 'Есть заявка, но человек ещё не переведён в список участниц.'];
      }}
      return ['Проверить вручную', 'Статус не требует действия или закрыт.'];
    }}

    function rowSearchIndex(row) {{
      return [
        row.displayName,
        row.telegramHandle,
        row.slug,
        row.email,
        row.selectedCourse,
        row.selectedCourseLabel,
        row.summary?.personalContext,
        row.summary?.visionFuture,
        row.leadAbout
      ].join(' ').toLowerCase();
    }}

    function getVisibleRows() {{
      const query = searchInput.value.trim().toLowerCase();
      return ALL_ROWS.filter((row) => {{
        const stageMatches = activeStage === 'all' ? true : stageForRow(row) === activeStage;
        const hiddenState = isHidden(row);
        const hiddenMatches = activeStatus === 'hidden' ? hiddenState : !hiddenState;
        const statusMatches =
          activeStatus === 'all' || activeStatus === 'hidden' ? true : statusForRow(row) === activeStatus;
        const searchMatches = !query || rowSearchIndex(row).includes(query);
        return stageMatches && hiddenMatches && statusMatches && searchMatches;
      }});
    }}

    function updateStats() {{
      const activeRows = ALL_ROWS.filter((row) => !isHidden(row));
      statTotal.textContent = String(activeRows.length);
      statLeads.textContent = String(activeRows.filter((row) => row.leadSubmitted).length);
      statPaid.textContent = String(activeRows.filter((row) => row.paid).length);
      statQuestionnaire.textContent = String(activeRows.filter((row) => row.questionnaireFilled).length);
      statCourseOpened.textContent = String(activeRows.filter((row) => row.courseOpened).length);
      statHidden.textContent = String(ALL_ROWS.filter((row) => isHidden(row)).length);
    }}

    function renderQueue(container, rows, emptyText) {{
      if (!rows.length) {{
        container.innerHTML = `<div class="empty-note">${{escapeHtml(emptyText)}}</div>`;
        return;
      }}

      container.innerHTML = rows.map((row) => {{
        const [title, note] = nextAction(row);
        return `
          <div class="queue-item">
            <div class="queue-name">${{escapeHtml(row.displayName)}}</div>
            <div class="queue-meta">${{escapeHtml(row.telegramHandle || '—')}}${{row.email ? ` · ${{escapeHtml(row.email)}}` : ''}}</div>
            <div class="queue-meta">${{escapeHtml(title)}}${{row.selectedCourseLabel && row.selectedCourseLabel !== '—' ? ` · ${{escapeHtml(row.selectedCourseLabel)}}` : ''}}</div>
            <div class="queue-meta">${{escapeHtml(note)}}</div>
          </div>
        `;
      }}).join('');
    }}

    function renderRows(rows) {{
      if (!rows.length) {{
        resultsBody.innerHTML = '<tr><td colspan="7">Нет людей под текущий фильтр.</td></tr>';
        return;
      }}

      resultsBody.innerHTML = rows.map((row, index) => {{
        const [actionTitle, actionNote] = nextAction(row);
        const hiddenButtonLabel = isHidden(row) ? 'Вернуть' : 'Скрыть';
        const hiddenButtonClass = isHidden(row) ? '' : ' is-muted';
        return `
          <tr>
            <td>
              <span class="name">${{escapeHtml(row.displayName)}}</span>
              <span class="meta">${{escapeHtml(row.telegramHandle || '—')}}</span>
              <span class="meta">${{row.slug ? `slug: ${{escapeHtml(row.slug)}}` : 'без slug'}}</span>
              <div class="links">
                ${{row.leadIssueUrl ? `<a class="link" href="${{row.leadIssueUrl}}" target="_blank" rel="noopener noreferrer">lead #${{row.leadIssueNumber}}</a>` : ''}}
                ${{row.questionnaireUrl ? `<a class="link" href="${{row.questionnaireUrl}}" target="_blank" rel="noopener noreferrer">анкета</a>` : ''}}
                ${{row.questionnaireIssueUrl ? `<a class="link" href="${{row.questionnaireIssueUrl}}" target="_blank" rel="noopener noreferrer">record #${{row.questionnaireIssueNumber}}</a>` : ''}}
              </div>
            </td>
            <td>
              <span class="badge ${{row.leadSubmitted ? 'ok' : 'muted'}}">Заявка</span>
              <span class="badge ${{row.paid ? 'ok' : 'muted'}}">Оплата</span>
              <span class="badge ${{row.questionnaireFilled ? 'ok' : 'muted'}}">Анкета</span>
              <span class="badge ${{row.courseOpened ? 'ok' : 'muted'}}">Курс открыт</span>
            </td>
            <td>
              <span class="action-title">${{escapeHtml(actionTitle)}}</span>
              <span class="action-note">${{escapeHtml(actionNote)}}</span>
            </td>
            <td>
              <span class="name">${{escapeHtml(row.courseOpened ? (row.openedCourse || row.selectedCourseLabel || '—') : (row.selectedCourseLabel || '—'))}}</span>
              <span class="meta">Путь: ${{escapeHtml(row.selectedPathLabel || '—')}}</span>
            </td>
            <td>${{escapeHtml(row.email || '—')}}</td>
            <td>${{escapeHtml(row.updatedAtLabel || '—')}}</td>
            <td>
              <div class="button-row">
                <button class="details-btn" type="button" data-index="${{index}}">Открыть</button>
                <button class="details-btn${{hiddenButtonClass}}" type="button" data-hide-index="${{index}}">${{hiddenButtonLabel}}</button>
              </div>
            </td>
          </tr>
        `;
      }}).join('');
    }}

    function openDetails(index) {{
      const row = getVisibleRows()[index];
      if (!row) return;

      const [actionTitle, actionNote] = nextAction(row);
      const body = [
        sectionHtml('Идентификация', paragraph([row.displayName, row.telegramHandle || '—', row.slug ? `slug: ${{row.slug}}` : 'без slug'].join('\\n'))),
        sectionHtml('Этапы', paragraph([
          row.leadSubmitted ? 'Заявка есть' : 'Заявки нет',
          row.paid ? 'Оплата есть' : 'Оплаты нет',
          row.questionnaireFilled ? 'Анкета заполнена' : 'Анкета не заполнена',
          row.courseOpened ? 'Курс открыт' : 'Курс не открыт'
        ].join('\\n'))),
        sectionHtml('Следующее действие', paragraph([actionTitle, actionNote].join('\\n'))),
        sectionHtml('Lead note', paragraph(row.leadAbout)),
        sectionHtml('Vision', paragraph(row.summary?.visionFuture)),
        sectionHtml('Personal context', paragraph(row.summary?.personalContext)),
        sectionHtml('Purpose', paragraph(row.summary?.purpose)),
        sectionHtml('Health restrictions', paragraph(row.summary?.healthRestrictions)),
        sectionHtml('Nutrition flags', list(row.summary?.nutritionFlags)),
        sectionHtml('Food habits', paragraph(row.summary?.foodHabits)),
        sectionHtml('Medications', paragraph(row.summary?.medications)),
        sectionHtml('Message for curator', paragraph(row.summary?.curatorMessage))
      ].join('');

      modalTitle.textContent = row.displayName;
      modalContent.innerHTML = body;
      detailsModal.classList.add('visible');
    }}

    function syncPage() {{
      const rows = getVisibleRows();
      const activeRows = ALL_ROWS.filter((row) => !isHidden(row));
      renderRows(rows);
      renderQueue(queueUnpaid, activeRows.filter((row) => statusForRow(row) === 'unpaid'), 'Сейчас нет лидов без оплаты.');
      renderQueue(queueWaitingQuestionnaire, activeRows.filter((row) => statusForRow(row) === 'waiting-questionnaire'), 'Сейчас нет участниц без анкеты.');
      renderQueue(queueNeedsPick, activeRows.filter((row) => statusForRow(row) === 'needs-pick'), 'Сейчас нет участниц, которым нужно подобрать курс.');
      renderQueue(queueReadyOpen, activeRows.filter((row) => statusForRow(row) === 'ready-open'), 'Сейчас нет участниц, которым нужно открыть курс.');
      updateStats();
    }}

    function activateFilter(container, key, value) {{
      [...container.querySelectorAll(`[data-${{key}}]`)].forEach((button) => {{
        button.classList.toggle('is-active', button.dataset[key] === value);
      }});
    }}

    stageFilters.addEventListener('click', (event) => {{
      const button = event.target.closest('[data-stage]');
      if (!button) return;
      activeStage = button.dataset.stage || 'all';
      activateFilter(stageFilters, 'stage', activeStage);
      syncPage();
    }});

    statusFilters.addEventListener('click', (event) => {{
      const button = event.target.closest('[data-status]');
      if (!button) return;
      activeStatus = button.dataset.status || 'all';
      activateFilter(statusFilters, 'status', activeStatus);
      syncPage();
    }});

    searchInput.addEventListener('input', syncPage);
    resultsBody.addEventListener('click', (event) => {{
      const button = event.target.closest('[data-index]');
      if (button) {{
        openDetails(Number(button.dataset.index));
        return;
      }}

      const hideButton = event.target.closest('[data-hide-index]');
      if (!hideButton) return;
      const row = getVisibleRows()[Number(hideButton.dataset.hideIndex)];
      if (!row) return;
      setRowHidden(row, !isHidden(row));
    }});
    closeModal.addEventListener('click', () => detailsModal.classList.remove('visible'));
    detailsModal.addEventListener('click', (event) => {{
      if (event.target === detailsModal) detailsModal.classList.remove('visible');
    }});

    syncPage();
  </script>
</body>
</html>
"""


def main() -> None:
    rows, snapshot_time = build_rows()
    OUTPUT_PATH.write_text(build_html(rows, snapshot_time), encoding="utf-8")
    print(f"Generated admissions dashboard with {len(rows)} rows at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
