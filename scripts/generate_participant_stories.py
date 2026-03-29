from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from issue_snapshot_tools import build_questionnaire_match_index, decode_record_from_issue_body
from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = ROOT / "scripts" / "admin_issues_snapshot.json"
OUTPUT_PATH = ROOT / "participant-stories.html"
QUESTIONNAIRE_BASE_URL = "https://olymarkes.github.io/high-performance/participant_questionnaires_april_2026"
WEEK1_TRACKER_BASE_URL = "https://olymarkes.github.io/high-performance/week_1_trackers_april_2026"
TRACKER_VERSION_QUERY = "v=materials-pdf-v4"
PRIVATE_REPO = "OLYMARKES/high-performance-leads"
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
LEGACY_COURSE_VALUES = set(COURSE_LABELS)
LEGACY_PELVIC_LABELS = [
    "Попадание воздуха во влагалище во время секса",
    "Боли или тяжесть в области лобка",
    "Частое мочеиспускание или недержание при нагрузке, смехе, кашле",
    "Ничего из перечисленного",
]
LEGACY_NUTRITION_LABELS = [
    "Подозреваю РПП, к специалисту не обращалась",
    "Часто беспокоюсь о весе, ограничиваю себя",
    "Мысли о еде занимают непропорционально много времени",
    "Бывают эпизоды переедания",
    "Строго считаю калории",
    "Избегаю углеводов или сахара",
    "Окружающие замечают, что я зациклена на весе",
    "Регулярно чувствую вину после еды",
]


def load_issues() -> list[dict]:
    payload = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def label_for_course(value: str) -> str:
    return COURSE_LABELS.get(value, value or "—")


def format_timestamp(value: str) -> str:
    if not value:
        return "—"

    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return dt.strftime("%d.%m.%Y %H:%M UTC")


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\r", " ").replace("\n", " ")).strip()


def normalize_multiline(value: object) -> str:
    cleaned = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def has_meaningful_value(value: object) -> bool:
    if isinstance(value, list):
        return any(has_meaningful_value(item) for item in value)
    if isinstance(value, dict):
        return any(has_meaningful_value(item) for item in value.values())
    return bool(normalize_multiline(value))


def merge_meaningful(fallback: object, current: object) -> object:
    if isinstance(fallback, list) or isinstance(current, list):
        return current if has_meaningful_value(current) else (fallback or [])

    if isinstance(fallback, dict) or isinstance(current, dict):
        merged: dict[str, object] = {}
        for key in set((fallback or {}).keys()) | set((current or {}).keys()):
            merged[key] = merge_meaningful((fallback or {}).get(key), (current or {}).get(key))
        return merged

    return current if has_meaningful_value(current) else (fallback if fallback is not None else current)


def build_empty_response_data() -> dict:
    return {
        "participantEmail": "",
        "visionFuture": "",
        "selectedPath": "",
        "courseChoice": "",
        "personalContext": "",
        "vip": {
            "purpose": "",
            "age": "",
            "height": "",
            "weight": "",
            "childrenStatus": "",
            "childrenDetail": "",
            "pregnantDetail": "",
            "healthRestrictions": "",
            "diastasis": "",
            "pelvicFloorFlags": [],
            "nutritionFlags": [],
            "typicalDay": "",
            "foodHabits": "",
            "medications": "",
            "curatorMessage": "",
        },
    }


def is_likely_metric(value: object) -> bool:
    normalized = normalize_text(value)
    return bool(normalized and re.fullmatch(r"\d{1,3}([.,]\d+)?", normalized))


def parse_legacy_draft_state(state: object) -> dict | None:
    values: list[object]
    if isinstance(state, list):
        values = state
    elif isinstance(state, dict) and isinstance(state.get("fields"), list):
        values = state["fields"]
    else:
        return None

    if not values:
        return None

    parsed = {
        "email": "",
        "selectedPath": "",
        "courseChoice": "",
        "personalContext": "",
        "responseData": build_empty_response_data(),
    }

    if isinstance(values[0], str):
        parsed["email"] = normalize_text(values[0])
        parsed["responseData"]["participantEmail"] = parsed["email"]

    if len(values) > 1 and isinstance(values[1], str):
        parsed["responseData"]["visionFuture"] = normalize_multiline(values[1])

    age_index = -1
    for index in range(3, 6):
        if len(values) <= index + 4:
            continue
        if (
            is_likely_metric(values[index])
            and is_likely_metric(values[index + 1])
            and is_likely_metric(values[index + 2])
            and isinstance(values[index + 3], bool)
            and isinstance(values[index + 4], bool)
        ):
            age_index = index
            break

    if age_index == -1:
        freeform = normalize_multiline(values[2] if len(values) > 2 else "")
        if freeform:
            parsed["selectedPath"] = "short" if freeform in LEGACY_COURSE_VALUES else "personal"
            if parsed["selectedPath"] == "short":
                parsed["courseChoice"] = freeform
                parsed["responseData"]["courseChoice"] = freeform
            else:
                parsed["personalContext"] = freeform
                parsed["responseData"]["personalContext"] = freeform
            parsed["responseData"]["selectedPath"] = parsed["selectedPath"]
        return parsed

    path_field = normalize_multiline(values[2] if len(values) > 2 else "")
    purpose_index = 3 if age_index == 4 else -1
    if path_field:
        if path_field in LEGACY_COURSE_VALUES:
            parsed["selectedPath"] = "short"
            parsed["courseChoice"] = path_field
            parsed["responseData"]["courseChoice"] = path_field
        else:
            parsed["selectedPath"] = "personal"
            parsed["personalContext"] = path_field
            parsed["responseData"]["personalContext"] = path_field
        parsed["responseData"]["selectedPath"] = parsed["selectedPath"]

    if purpose_index != -1 and len(values) > purpose_index and isinstance(values[purpose_index], str):
        parsed["responseData"]["vip"]["purpose"] = normalize_multiline(values[purpose_index])

    parsed["responseData"]["vip"]["age"] = normalize_text(values[age_index])
    parsed["responseData"]["vip"]["height"] = normalize_text(values[age_index + 1])
    parsed["responseData"]["vip"]["weight"] = normalize_text(values[age_index + 2])

    cursor = age_index + 3
    no_children = bool(values[cursor]) if len(values) > cursor else False
    has_children = bool(values[cursor + 1]) if len(values) > cursor + 1 else False
    cursor += 2

    children_detail = ""
    pregnant = False
    if len(values) > cursor and isinstance(values[cursor], str):
        children_detail = normalize_multiline(values[cursor])
        cursor += 1
        pregnant = bool(values[cursor]) if len(values) > cursor else False
        cursor += 1
    elif len(values) > cursor and isinstance(values[cursor], bool):
        pregnant = bool(values[cursor])
        cursor += 1

    parsed["responseData"]["vip"]["childrenStatus"] = "pregnant" if pregnant else "yes" if has_children else "no" if no_children else ""
    parsed["responseData"]["vip"]["childrenDetail"] = children_detail
    parsed["responseData"]["vip"]["healthRestrictions"] = normalize_multiline(values[cursor] if len(values) > cursor else "")
    cursor += 1
    parsed["responseData"]["vip"]["diastasis"] = normalize_text(values[cursor] if len(values) > cursor else "")
    cursor += 1

    flags: list[bool] = []
    while len(values) > cursor and isinstance(values[cursor], bool):
        flags.append(bool(values[cursor]))
        cursor += 1

    parsed["responseData"]["vip"]["pelvicFloorFlags"] = [
        label for index, label in enumerate(LEGACY_PELVIC_LABELS) if index < len(flags) and flags[index]
    ]
    parsed["responseData"]["vip"]["nutritionFlags"] = [
        label
        for index, label in enumerate(LEGACY_NUTRITION_LABELS, start=len(LEGACY_PELVIC_LABELS))
        if index < len(flags) and flags[index]
    ]

    remaining_text = [normalize_multiline(value) for value in values[cursor:] if normalize_multiline(value)]
    fields = ["typicalDay", "foodHabits", "medications", "curatorMessage"]
    for field_name, text in zip(fields, remaining_text):
        parsed["responseData"]["vip"][field_name] = text

    return parsed


def hydrate_questionnaire_record(record: dict) -> dict:
    legacy = parse_legacy_draft_state(record.get("draftState"))
    response_data = merge_meaningful(
        legacy["responseData"] if legacy else build_empty_response_data(),
        record.get("responseData") or {},
    )
    return {
        **record,
        "email": normalize_text(record.get("email") or (legacy or {}).get("email") or response_data.get("participantEmail") or ""),
        "selectedPath": normalize_text(record.get("selectedPath") or response_data.get("selectedPath") or (legacy or {}).get("selectedPath") or ""),
        "courseChoice": normalize_text(record.get("courseChoice") or response_data.get("courseChoice") or (legacy or {}).get("courseChoice") or ""),
        "personalContext": normalize_multiline(record.get("personalContext") or response_data.get("personalContext") or (legacy or {}).get("personalContext") or ""),
        "responseData": response_data,
    }


def extract_leads_by_issue(issues: list[dict]) -> dict[int, dict]:
    leads: dict[int, dict] = {}
    for issue in issues:
        record = decode_record_from_issue_body(issue.get("body", ""))
        if not record or record.get("kind") != "high-performance-lead":
            continue
        issue_number = issue.get("number")
        if isinstance(issue_number, int):
            leads[issue_number] = record
    return leads


def first_sentences(text: str, limit: int = 2, max_chars: int = 340) -> str:
    source = normalize_multiline(text)
    if not source:
        return ""
    chunks = re.split(r"(?<=[.!?])\s+|\n+", source)
    selected: list[str] = []
    total = 0
    for chunk in chunks:
        item = chunk.strip()
        if not item:
            continue
        if selected and (len(selected) >= limit or total + len(item) > max_chars):
            break
        selected.append(item)
        total += len(item)
        if len(selected) >= limit and total >= max_chars * 0.55:
            break
    if not selected:
        return source[:max_chars].strip()
    return " ".join(selected).strip()


def take_paragraphs(text: str, max_paragraphs: int = 3, max_chars: int = 900) -> str:
    source = normalize_multiline(text)
    if not source:
        return ""

    paragraphs = [part.strip() for part in re.split(r"\n{2,}", source) if part.strip()]
    if not paragraphs:
        paragraphs = [source]

    selected: list[str] = []
    total = 0
    for paragraph in paragraphs:
        if selected and (len(selected) >= max_paragraphs or total + len(paragraph) > max_chars):
            break
        selected.append(paragraph)
        total += len(paragraph)

    if not selected:
        return source[:max_chars].strip()
    return "\n\n".join(selected).strip()


def children_label(status: str, detail: str) -> str:
    if status == "pregnant":
        return f"Беременность{f' ({detail})' if detail else ''}"
    if status == "yes":
        return f"Есть дети{f' ({detail})' if detail else ''}"
    if status == "no":
        return "Детей нет"
    return "Не указано"


def build_story(row: dict) -> dict[str, str]:
    response_data = row.get("responseData") or {}
    vip = response_data.get("vip") or {}
    lead_about = row.get("leadAbout") or ""
    selected_path = row.get("selectedPath") or response_data.get("selectedPath") or ""
    course_choice = row.get("courseChoice") or response_data.get("courseChoice") or ""
    selected_course_label = label_for_course(course_choice) if course_choice else ""
    age = normalize_text(vip.get("age"))
    height = normalize_text(vip.get("height"))
    weight = normalize_text(vip.get("weight"))
    children = children_label(normalize_text(vip.get("childrenStatus")), normalize_text(vip.get("childrenDetail") or vip.get("pregnantDetail")))
    vision = normalize_multiline(response_data.get("visionFuture"))
    personal_context = normalize_multiline(row.get("personalContext") or response_data.get("personalContext"))
    purpose = normalize_multiline(vip.get("purpose"))
    health = normalize_multiline(vip.get("healthRestrictions"))
    day = normalize_multiline(vip.get("typicalDay"))
    food = normalize_multiline(vip.get("foodHabits"))
    medications = normalize_multiline(vip.get("medications"))
    curator_message = normalize_multiline(vip.get("curatorMessage"))
    nutrition_flags = vip.get("nutritionFlags") or []
    pelvic_flags = vip.get("pelvicFloorFlags") or []

    if row.get("hasQuestionnaire"):
        route_line = (
            f"Выбрала курс «{selected_course_label}»."
            if selected_course_label
            else "Нуждается в ручном подборе курса."
            if selected_path == "personal"
            else "Анкета сохранена, но выбор курса пока не зафиксирован."
        )
        profile_bits = []
        if age:
            profile_bits.append(f"{age} лет")
        if height:
            profile_bits.append(f"{height} см")
        if weight:
            profile_bits.append(f"{weight} кг")
        profile_bits.append(children)
        profile_line = ", ".join(bit for bit in profile_bits if bit)

        intro = " ".join(
            bit
            for bit in [
                route_line,
                f"Базовый профиль: {profile_line}." if profile_line else "",
                f"Главный запрос: {take_paragraphs(purpose or personal_context or lead_about, max_paragraphs=2, max_chars=520)}" if has_meaningful_value(purpose or personal_context or lead_about) else "",
            ]
            if bit
        )

        context = take_paragraphs(vision or lead_about or personal_context, max_paragraphs=3, max_chars=1100)
        rhythm = take_paragraphs(day or personal_context, max_paragraphs=3, max_chars=1000)

        health_parts = []
        if health:
            health_parts.append(f"По здоровью и ограничениям отмечает:\n{take_paragraphs(health, max_paragraphs=3, max_chars=900)}")
        if normalize_text(vip.get("diastasis")):
            health_parts.append(f"Диастаз: {normalize_text(vip.get('diastasis'))}.")
        if pelvic_flags:
            health_parts.append(f"По тазовому дну отмечены пункты: {', '.join(pelvic_flags)}.")
        health_summary = "\n\n".join(health_parts)

        food_parts = []
        if nutrition_flags:
            food_parts.append(f"По отношению к питанию видны риски/триггеры: {', '.join(nutrition_flags)}.")
        if food:
            food_parts.append(f"Пищевой паттерн сейчас выглядит так:\n{take_paragraphs(food, max_paragraphs=4, max_chars=1000)}")
        food_summary = "\n\n".join(food_parts)

        extra_parts = []
        if medications and medications.lower() != "нет":
            extra_parts.append(f"Препараты: {take_paragraphs(medications, max_paragraphs=2, max_chars=300)}")
        if curator_message:
            extra_parts.append(f"Отдельный запрос к куратору:\n{take_paragraphs(curator_message, max_paragraphs=2, max_chars=340)}")
        extra = "\n\n".join(extra_parts)
    else:
        intro = " ".join(
            bit
            for bit in [
                "Сохранённой серверной анкеты пока нет.",
                "Есть только исходная заявка." if has_meaningful_value(lead_about) else "",
                f"Из заявки: {take_paragraphs(lead_about, max_paragraphs=3, max_chars=1100)}" if has_meaningful_value(lead_about) else "",
            ]
            if bit
        )
        context = ""
        rhythm = ""
        health_summary = ""
        food_summary = ""
        extra = ""

    return {
        "intro": intro,
        "context": context,
        "rhythm": rhythm,
        "healthSummary": health_summary,
        "foodSummary": food_summary,
        "extra": extra,
        "vision": vision,
        "personalContext": personal_context,
        "purpose": purpose,
        "health": health,
        "typicalDay": day,
        "foodHabits": food,
        "medications": medications,
        "curatorMessage": curator_message,
        "nutritionFlags": ", ".join(nutrition_flags),
        "pelvicFlags": ", ".join(pelvic_flags),
        "leadAbout": normalize_multiline(lead_about),
    }


def build_rows() -> tuple[list[dict], str]:
    issues = load_issues()
    participants = get_participants()
    questionnaire_index = build_questionnaire_match_index(participants, issues)
    leads_by_issue = extract_leads_by_issue(issues)
    snapshot_time = max((str(issue.get("updated_at") or "") for issue in issues), default="")
    if not snapshot_time:
        snapshot_time = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    rows: list[dict] = []
    for participant in participants:
        lead = leads_by_issue.get(participant.get("lead_issue"))
        questionnaire_match = questionnaire_index.get(participant["slug"])
        hydrated_record = hydrate_questionnaire_record(questionnaire_match["record"]) if questionnaire_match else {}
        response_data = hydrated_record.get("responseData") or build_empty_response_data()
        row = {
            "displayName": participant["display_name"],
            "slug": participant["slug"],
            "telegramHandle": participant["telegram_handle"],
            "leadIssueNumber": participant.get("lead_issue") or "",
            "leadIssueUrl": f"https://github.com/{PRIVATE_REPO}/issues/{participant['lead_issue']}" if participant.get("lead_issue") else "",
            "questionnaireIssueNumber": questionnaire_match["issue"]["number"] if questionnaire_match else "",
            "questionnaireIssueUrl": questionnaire_match["issue"]["html_url"] if questionnaire_match else "",
            "questionnaireUrl": f"{QUESTIONNAIRE_BASE_URL}/q_{participant['token']}.html",
            "week1TrackerUrl": f"{WEEK1_TRACKER_BASE_URL}/w1_{participant['token']}.html?{TRACKER_VERSION_QUERY}",
            "hasQuestionnaire": bool(questionnaire_match),
            "matchedBy": questionnaire_match.get("matchedBy", "") if questionnaire_match else "",
            "submittedAt": hydrated_record.get("submittedAt") or (questionnaire_match["issue"].get("updated_at") if questionnaire_match else "") or "",
            "submittedAtLabel": format_timestamp(hydrated_record.get("submittedAt") or (questionnaire_match["issue"].get("updated_at") if questionnaire_match else "") or ""),
            "email": hydrated_record.get("email") or normalize_text((lead or {}).get("email")),
            "selectedPath": hydrated_record.get("selectedPath") or response_data.get("selectedPath") or "",
            "courseChoice": hydrated_record.get("courseChoice") or response_data.get("courseChoice") or "",
            "responseData": response_data,
            "leadAbout": normalize_multiline((lead or {}).get("about")),
        }
        row["story"] = build_story(row)
        rows.append(row)

    rows.sort(key=lambda item: (0 if item["hasQuestionnaire"] else 1, item["displayName"], item["telegramHandle"]))
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
  <title>High Performance - Participant Stories</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #0b1010;
      --surface: #131a19;
      --surface-alt: #0f1514;
      --surface-soft: #171f1e;
      --border: #293231;
      --text: #ecf1ef;
      --muted: #99a59f;
      --soft: #74817c;
      --accent: #d4a25f;
      --accent-2: #92c5a4;
      --danger: #d1867b;
      --radius: 22px;
    }}
    body {{
      min-height: 100vh;
      color: var(--text);
      font-family: 'Inter', sans-serif;
      background:
        radial-gradient(circle at top left, rgba(212, 162, 95, 0.10), transparent 28%),
        radial-gradient(circle at top right, rgba(146, 197, 164, 0.09), transparent 24%),
        linear-gradient(180deg, #0a0f0f 0%, #0f1514 100%);
      padding: 28px 16px 56px;
    }}
    .page {{ max-width: 1480px; margin: 0 auto; }}
    .hero {{
      padding: 26px 0 30px;
      text-align: center;
    }}
    .hero-label {{
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.32em;
      font-size: 11px;
      font-weight: 700;
    }}
    h1 {{
      margin-top: 20px;
      font-family: 'Playfair Display', serif;
      font-size: clamp(42px, 8vw, 78px);
      line-height: 0.96;
      font-weight: 400;
    }}
    h1 em {{ color: var(--accent); font-style: italic; }}
    .hero-sub {{
      max-width: 980px;
      margin: 18px auto 0;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.8;
      font-weight: 300;
    }}
    .panel {{
      background: rgba(19, 26, 25, 0.88);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px;
      backdrop-filter: blur(10px);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18);
    }}
    .toolbar {{
      display: grid;
      grid-template-columns: minmax(0, 1.4fr) auto;
      gap: 14px;
      align-items: center;
    }}
    .input {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: var(--surface-alt);
      color: var(--text);
      font: inherit;
      padding: 15px 18px;
      outline: none;
    }}
    .input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(212, 162, 95, 0.14);
    }}
    .filter-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: flex-end;
    }}
    .chip {{
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      border-radius: 999px;
      padding: 12px 16px;
      font: inherit;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .chip.is-active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #111;
      font-weight: 700;
    }}
    .stats {{
      margin-top: 16px;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }}
    .stat {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 18px;
    }}
    .stat-label {{
      color: var(--soft);
      text-transform: uppercase;
      letter-spacing: 0.16em;
      font-size: 11px;
      font-weight: 600;
    }}
    .stat-value {{
      margin-top: 10px;
      font-family: 'Playfair Display', serif;
      font-size: 38px;
      line-height: 1;
    }}
    .stories {{
      margin-top: 20px;
      display: grid;
      gap: 18px;
    }}
    .story-card {{
      background: rgba(19, 26, 25, 0.95);
      border: 1px solid var(--border);
      border-radius: 26px;
      padding: 24px;
      box-shadow: 0 18px 60px rgba(0, 0, 0, 0.14);
    }}
    .story-card.is-missing {{
      border-color: rgba(209, 134, 123, 0.45);
    }}
    .story-head {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: flex-start;
    }}
    .story-title {{
      font-family: 'Playfair Display', serif;
      font-size: clamp(30px, 4vw, 42px);
      line-height: 1;
      font-weight: 400;
    }}
    .story-meta {{
      margin-top: 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 8px 12px;
      border: 1px solid var(--border);
      background: var(--surface-alt);
      color: var(--muted);
      font-size: 12px;
      line-height: 1.2;
    }}
    .pill.is-ok {{
      color: #102014;
      background: var(--accent-2);
      border-color: var(--accent-2);
      font-weight: 700;
    }}
    .pill.is-missing {{
      color: #2b100c;
      background: #e5a196;
      border-color: #e5a196;
      font-weight: 700;
    }}
    .story-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: flex-end;
      max-width: 420px;
    }}
    .story-link {{
      color: var(--text);
      text-decoration: none;
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 11px 14px;
      background: var(--surface-alt);
      font-size: 13px;
      transition: all 0.2s ease;
    }}
    .story-link:hover {{
      border-color: var(--accent);
      color: var(--accent);
    }}
    .story-grid {{
      margin-top: 20px;
      display: grid;
      grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.75fr);
      gap: 18px;
    }}
    .story-main, .story-side {{
      display: grid;
      gap: 14px;
    }}
    .block {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 18px;
    }}
    .block-label {{
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 11px;
      font-weight: 700;
    }}
    .block-text {{
      margin-top: 12px;
      color: var(--text);
      font-size: 15px;
      line-height: 1.82;
      white-space: pre-wrap;
    }}
    .facts {{
      display: grid;
      gap: 10px;
    }}
    .fact {{
      display: grid;
      gap: 4px;
      padding-bottom: 10px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }}
    .fact:last-child {{
      border-bottom: none;
      padding-bottom: 0;
    }}
    .fact-label {{
      color: var(--soft);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.14em;
    }}
    .fact-value {{
      color: var(--text);
      font-size: 14px;
      line-height: 1.65;
      white-space: pre-wrap;
    }}
    details {{
      border-radius: 18px;
      border: 1px solid var(--border);
      background: var(--surface-soft);
      overflow: hidden;
    }}
    summary {{
      list-style: none;
      cursor: pointer;
      padding: 16px 18px;
      color: var(--text);
      font-weight: 600;
    }}
    summary::-webkit-details-marker {{ display: none; }}
    details[open] summary {{
      border-bottom: 1px solid var(--border);
    }}
    .details-body {{
      padding: 16px 18px 18px;
      white-space: pre-wrap;
      color: var(--muted);
      line-height: 1.8;
      font-size: 14px;
    }}
    .empty {{
      padding: 28px;
      text-align: center;
      color: var(--muted);
      border: 1px dashed var(--border);
      border-radius: 20px;
      background: var(--surface-alt);
    }}
    @media (max-width: 1100px) {{
      .toolbar {{ grid-template-columns: 1fr; }}
      .filter-bar {{ justify-content: flex-start; }}
      .stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .story-grid {{ grid-template-columns: 1fr; }}
      .story-head {{ flex-direction: column; }}
      .story-links {{ justify-content: flex-start; max-width: none; }}
    }}
    @media (max-width: 640px) {{
      body {{ padding: 18px 12px 36px; }}
      .panel, .story-card {{ padding: 18px; }}
      .stats {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <div class="hero-label">High Performance</div>
      <h1>Participant <em>Stories</em></h1>
      <p class="hero-sub">Подробные narrative summary по каждой участнице. Источник: live snapshot GitHub issues, обновлённый на {format_timestamp(snapshot_time)}.</p>
    </section>

    <section class="panel">
      <div class="toolbar">
        <input id="search" class="input" type="search" placeholder="Поиск по имени, @telegram, курсу, контексту">
        <div class="filter-bar" id="filters">
          <button class="chip is-active" type="button" data-filter="all">Все</button>
          <button class="chip" type="button" data-filter="saved">Есть анкета</button>
          <button class="chip" type="button" data-filter="missing">Нет анкеты</button>
        </div>
      </div>
      <div class="stats">
        <div class="stat">
          <div class="stat-label">Всего</div>
          <div id="stat-total" class="stat-value">0</div>
        </div>
        <div class="stat">
          <div class="stat-label">Есть анкета</div>
          <div id="stat-saved" class="stat-value">0</div>
        </div>
        <div class="stat">
          <div class="stat-label">Нет анкеты</div>
          <div id="stat-missing" class="stat-value">0</div>
        </div>
        <div class="stat">
          <div class="stat-label">Нужен подбор</div>
          <div id="stat-pick" class="stat-value">0</div>
        </div>
      </div>
    </section>

    <section id="stories" class="stories"></section>
  </div>

  <script>
    const ALL_ROWS = {script_json(rows)};
    const storiesRoot = document.getElementById('stories');
    const searchInput = document.getElementById('search');
    const filters = document.getElementById('filters');
    const statTotal = document.getElementById('stat-total');
    const statSaved = document.getElementById('stat-saved');
    const statMissing = document.getElementById('stat-missing');
    const statPick = document.getElementById('stat-pick');
    let activeFilter = 'all';

    function escapeHtml(value) {{
      return String(value || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }}

    function paragraph(text) {{
      if (!String(text || '').trim()) {{
        return '<div class="fact-value">—</div>';
      }}
      return `<div class="block-text">${{escapeHtml(text)}}</div>`;
    }}

    function detailSection(title, text) {{
      if (!String(text || '').trim()) {{
        return '';
      }}
      return `
        <details>
          <summary>${{escapeHtml(title)}}</summary>
          <div class="details-body">${{escapeHtml(text)}}</div>
        </details>
      `;
    }}

    function buildCard(row) {{
      const story = row.story || {{}};
      const hasCourse = Boolean(row.courseChoice);
      const needsPick = row.hasQuestionnaire && !hasCourse && row.selectedPath === 'personal';
      const statusPill = row.hasQuestionnaire
        ? `<span class="pill is-ok">Анкета сохранена</span>`
        : `<span class="pill is-missing">Нет серверной анкеты</span>`;
      const pickPill = needsPick
        ? `<span class="pill">Нужно подобрать курс</span>`
        : hasCourse
          ? `<span class="pill">${{escapeHtml(row.courseChoice ? 'Курс: ' + ({script_json(COURSE_LABELS)}[row.courseChoice] || row.courseChoice) : '')}}</span>`
          : '';

      return `
        <article class="story-card${{row.hasQuestionnaire ? '' : ' is-missing'}}">
          <div class="story-head">
            <div>
              <div class="story-title">${{escapeHtml(row.displayName)}}</div>
              <div class="story-meta">
                ${{statusPill}}
                ${{pickPill}}
                <span class="pill">${{escapeHtml(row.telegramHandle || 'без telegram')}}</span>
                <span class="pill">${{escapeHtml(row.submittedAtLabel || '—')}}</span>
              </div>
            </div>
            <div class="story-links">
              <a class="story-link" href="${{row.questionnaireUrl}}" target="_blank" rel="noopener noreferrer">Открыть анкету</a>
              <a class="story-link" href="${{row.week1TrackerUrl}}" target="_blank" rel="noopener noreferrer">Week 1 tracker</a>
              ${{row.questionnaireIssueUrl ? `<a class="story-link" href="${{row.questionnaireIssueUrl}}" target="_blank" rel="noopener noreferrer">GitHub issue</a>` : ''}}
            </div>
          </div>

          <div class="story-grid">
            <div class="story-main">
              <section class="block">
                <div class="block-label">Подробный рассказ</div>
                ${{paragraph(story.intro)}}
              </section>
              ${{story.context ? `<section class="block"><div class="block-label">Контекст и мотивация</div>${{paragraph(story.context)}}</section>` : ''}}
              ${{story.rhythm ? `<section class="block"><div class="block-label">Текущий ритм и жизнь</div>${{paragraph(story.rhythm)}}</section>` : ''}}
              ${{story.healthSummary ? `<section class="block"><div class="block-label">Здоровье и ограничения</div>${{paragraph(story.healthSummary)}}</section>` : ''}}
              ${{story.foodSummary ? `<section class="block"><div class="block-label">Питание и привычки</div>${{paragraph(story.foodSummary)}}</section>` : ''}}
              ${{story.extra ? `<section class="block"><div class="block-label">Дополнительно</div>${{paragraph(story.extra)}}</section>` : ''}}
              <section class="block">
                <div class="block-label">Исходные фрагменты</div>
                <div style="margin-top:12px; display:grid; gap:10px;">
                  ${{detailSection('Vision / чего хочет к концу апреля', story.vision)}}
                  ${{detailSection('Personal context / текущий контекст', story.personalContext)}}
                  ${{detailSection('Purpose / как поймёт, что идёт правильно', story.purpose)}}
                  ${{detailSection('Lead note / исходная заявка', story.leadAbout)}}
                </div>
              </section>
            </div>

            <aside class="story-side">
              <section class="block">
                <div class="block-label">Быстрые факты</div>
                <div class="facts" style="margin-top:14px;">
                  <div class="fact">
                    <div class="fact-label">Email</div>
                    <div class="fact-value">${{escapeHtml(row.email || '—')}}</div>
                  </div>
                  <div class="fact">
                    <div class="fact-label">Путь</div>
                    <div class="fact-value">${{escapeHtml(row.selectedPath || '—')}}</div>
                  </div>
                  <div class="fact">
                    <div class="fact-label">Выбранный курс</div>
                    <div class="fact-value">${{escapeHtml(row.courseChoice ? ({script_json(COURSE_LABELS)}[row.courseChoice] || row.courseChoice) : '—')}}</div>
                  </div>
                  <div class="fact">
                    <div class="fact-label">Lead issue</div>
                    <div class="fact-value">${{escapeHtml(row.leadIssueNumber ? '#' + row.leadIssueNumber : '—')}}</div>
                  </div>
                  <div class="fact">
                    <div class="fact-label">Questionnaire issue</div>
                    <div class="fact-value">${{escapeHtml(row.questionnaireIssueNumber ? '#' + row.questionnaireIssueNumber : '—')}}</div>
                  </div>
                  ${{row.matchedBy ? `<div class="fact"><div class="fact-label">Matched by</div><div class="fact-value">${{escapeHtml(row.matchedBy)}}</div></div>` : ''}}
                </div>
              </section>

              <section class="block">
                <div class="block-label">Тело, питание, быт</div>
                <div style="margin-top:12px; display:grid; gap:10px;">
                  ${{detailSection('Health restrictions', story.health)}}
                  ${{detailSection('Typical day', story.typicalDay)}}
                  ${{detailSection('Food habits', story.foodHabits)}}
                  ${{detailSection('Medications', story.medications)}}
                  ${{detailSection('Message for curator', story.curatorMessage)}}
                  ${{detailSection('Nutrition flags', story.nutritionFlags)}}
                  ${{detailSection('Pelvic floor flags', story.pelvicFlags)}}
                </div>
              </section>
            </aside>
          </div>
        </article>
      `;
    }}

    function getVisibleRows() {{
      const query = (searchInput.value || '').trim().toLowerCase();
      return ALL_ROWS.filter((row) => {{
        if (activeFilter === 'saved' && !row.hasQuestionnaire) return false;
        if (activeFilter === 'missing' && row.hasQuestionnaire) return false;
        if (!query) return true;
        const haystack = [
          row.displayName,
          row.telegramHandle,
          row.email,
          row.selectedPath,
          row.courseChoice,
          row.story?.intro,
          row.story?.context,
          row.story?.body,
          row.story?.vision,
          row.story?.personalContext,
          row.story?.leadAbout
        ].join(' ').toLowerCase();
        return haystack.includes(query);
      }});
    }}

    function syncStats() {{
      statTotal.textContent = String(ALL_ROWS.length);
      statSaved.textContent = String(ALL_ROWS.filter((row) => row.hasQuestionnaire).length);
      statMissing.textContent = String(ALL_ROWS.filter((row) => !row.hasQuestionnaire).length);
      statPick.textContent = String(ALL_ROWS.filter((row) => row.hasQuestionnaire && !row.courseChoice && row.selectedPath === 'personal').length);
    }}

    function render() {{
      const rows = getVisibleRows();
      if (!rows.length) {{
        storiesRoot.innerHTML = '<div class="empty">Под текущий фильтр ничего не найдено.</div>';
        return;
      }}
      storiesRoot.innerHTML = rows.map(buildCard).join('');
    }}

    filters.addEventListener('click', (event) => {{
      const button = event.target.closest('[data-filter]');
      if (!button) return;
      activeFilter = button.dataset.filter || 'all';
      [...filters.querySelectorAll('[data-filter]')].forEach((item) => {{
        item.classList.toggle('is-active', item.dataset.filter === activeFilter);
      }});
      render();
    }});

    searchInput.addEventListener('input', render);
    syncStats();
    render();
  </script>
</body>
</html>
"""


def main() -> None:
    rows, snapshot_time = build_rows()
    OUTPUT_PATH.write_text(build_html(rows, snapshot_time), encoding="utf-8")
    print(f"Generated participant stories page with {len(rows)} rows at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
