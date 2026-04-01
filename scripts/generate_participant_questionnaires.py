from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from issue_snapshot_tools import build_questionnaire_match_index
from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "participant_questionnaires_april_2026"
ISSUES_SNAPSHOT_PATH = ROOT / "scripts" / "admin_issues_snapshot.json"
SOURCE_TEMPLATE_PATH = Path("/Users/olymarkes/Documents/Claude/Projects/High perfomance/anketa.html")
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/participant_questionnaires_april_2026"
PRIVATE_REPO = "OLYMARKES/high-performance-leads"

TEAM_PAGE_TOKEN = "team-vault-7m4k9p2x6c8q"
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


def quote_js(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def script_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")

def course_label(value: str) -> str:
    return COURSE_LABELS.get(value, value or "")


def label_for_path(value: str) -> str:
    if value == "short":
        return "Короткий"
    if value == "personal":
        return "Персональный"
    return "—"


def format_snapshot_time(value: str) -> str:
    if not value:
        return ""

    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return dt.strftime("%d.%m.%Y %H:%M UTC")


def fetch_github_issues() -> list[dict]:
    payload = json.loads(ISSUES_SNAPSHOT_PATH.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def build_admin_snapshot(entries: list[dict[str, str]]) -> tuple[list[dict[str, object]], str, str | None]:
    snapshot_generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    try:
        issues = fetch_github_issues()
    except (FileNotFoundError, json.JSONDecodeError) as error:
        return [], snapshot_generated_at, str(error)

    latest_by_slug = build_questionnaire_match_index(entries, issues)
    latest_issue_update = max((str(issue.get("updated_at") or "") for issue in issues), default="")
    if latest_issue_update:
        snapshot_generated_at = latest_issue_update

    rows: list[dict[str, object]] = []
    for entry in entries:
        match = latest_by_slug.get(entry["slug"])
        record = match["record"] if match else {}
        issue = match["issue"] if match else {}
        response_data = record.get("responseData", {}) if isinstance(record, dict) else {}
        vip = response_data.get("vip", {}) if isinstance(response_data, dict) else {}

        selected_path = str(record.get("selectedPath") or response_data.get("selectedPath") or "")
        selected_course = str(record.get("courseChoice") or response_data.get("courseChoice") or "")
        personal_context = str(record.get("personalContext") or response_data.get("personalContext") or "")
        updated_at = str(record.get("submittedAt") or issue.get("updated_at") or "")

        status_key = "waiting"
        status_label = "Ждём анкету"
        action_title = "Напомнить заполнить"
        action_note = "Сохранённой версии анкеты пока нет."

        if record:
            if selected_course:
                status_key = "ready-open"
                status_label = "Курс выбран"
                action_title = f"Открыть курс {course_label(selected_course)}"
                action_note = "Участница сама выбрала курс в анкете."
            elif selected_path == "personal" or personal_context.strip():
                status_key = "needs-pick"
                status_label = "Нужно подобрать"
                action_title = "Подобрать курс"
                action_note = "Нужен ручной подбор по анкете."
            elif selected_path == "short":
                status_key = "review"
                status_label = "Нужно проверить"
                action_title = "Проверить выбор"
                action_note = "Короткий путь выбран, но курс не определён."
            else:
                status_key = "review"
                status_label = "Нужно проверить"
                action_title = "Проверить анкету"
                action_note = "Данные анкеты неполные для решения."

        rows.append(
            {
                "slug": entry["slug"],
                "displayName": entry["display_name"],
                "telegramHandle": entry["telegram_handle"],
                "questionnaireUrl": f"{PUBLIC_BASE_URL}/{entry['filename']}",
                "leadIssueNumber": entry.get("lead_issue"),
                "leadIssueUrl": f"https://github.com/{PRIVATE_REPO}/issues/{entry['lead_issue']}" if entry.get("lead_issue") else "",
                "issueUrl": issue.get("html_url", ""),
                "issueNumber": issue.get("number", ""),
                "matchedBy": match.get("matchedBy", "") if match else "",
                "email": record.get("email") or response_data.get("participantEmail") or "",
                "selectedPath": selected_path,
                "selectedPathLabel": label_for_path(selected_path),
                "selectedCourse": selected_course,
                "selectedCourseLabel": course_label(selected_course) or "—",
                "updatedAt": updated_at,
                "updatedAtLabel": format_snapshot_time(updated_at) or "—",
                "statusKey": status_key,
                "statusLabel": status_label,
                "actionTitle": action_title,
                "actionNote": action_note,
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

    status_priority = {"needs-pick": 0, "ready-open": 1, "review": 2, "waiting": 3}

    def sort_key(row: dict[str, object]) -> tuple[int, float, str]:
        updated_at = str(row.get("updatedAt") or "")
        timestamp = 0.0
        if updated_at:
            try:
                timestamp = datetime.fromisoformat(updated_at.replace("Z", "+00:00")).timestamp()
            except ValueError:
                timestamp = 0.0
        return (
            status_priority.get(str(row.get("statusKey") or ""), 9),
            -timestamp,
            str(row.get("displayName") or ""),
        )

    rows.sort(key=sort_key)
    return rows, snapshot_generated_at, None


def load_template() -> str:
    return SOURCE_TEMPLATE_PATH.read_text(encoding="utf-8")


def add_personalization(template: str, name: str, for_name: str) -> str:
    html = template
    html = html.replace("<title>HIGH PERFORMANCE — Анкета</title>", f"<title>HIGH PERFORMANCE — Анкета для {for_name}</title>", 1)
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots" content="noindex, nofollow, noarchive">',
        1,
    )
    html = html.replace("<div class=\"hero-greeting\">Привет, <em>{Имя}</em></div>", f"<div class=\"hero-greeting\">Привет, <em>{name}</em></div>", 1)
    html = html.replace(
        'select, textarea, input[type="text"] {',
        'select, textarea, input[type="text"], input[type="email"] {',
        1,
    )
    html = html.replace(
        'select:focus, textarea:focus, input[type="text"]:focus {',
        'select:focus, textarea:focus, input[type="text"]:focus, input[type="email"]:focus {',
        1,
    )
    html = html.replace(
        ".success-overlay p {\n    color: var(--text-secondary);\n    font-size: 16px;\n    font-weight: 300;\n  }",
        """.success-overlay p {\n    color: var(--text-secondary);\n    font-size: 16px;\n    font-weight: 300;\n    max-width: 520px;\n  }\n\n  .success-actions {\n    display: flex;\n    gap: 12px;\n    flex-wrap: wrap;\n    justify-content: center;\n    margin-top: 8px;\n  }\n\n  .save-note {\n    margin-top: 16px;\n    color: var(--text-muted);\n    font-size: 13px;\n    font-weight: 300;\n    line-height: 1.7;\n  }\n\n  .success-secondary-btn {\n    display: inline-flex;\n    align-items: center;\n    justify-content: center;\n    gap: 10px;\n    background: transparent;\n    color: var(--text);\n    border: 1px solid var(--border-hover);\n    border-radius: 60px;\n    padding: 18px 28px;\n    font-family: 'Inter', sans-serif;\n    font-size: 12px;\n    font-weight: 600;\n    letter-spacing: 1.8px;\n    text-transform: uppercase;\n    cursor: pointer;\n    transition: all 0.3s ease;\n  }\n\n  .success-secondary-btn:hover {\n    border-color: var(--accent);\n    color: var(--accent);\n    background: var(--accent-glow);\n  }""",
        1,
    )
    html = html.replace(
        '<p class="hero-sub">Я очень рада, что ты с нами. Поехали :)</p>',
        '<p class="hero-sub">Я очень рада, что ты с нами. Здесь можно спокойно заполнить всё в своём ритме — черновик сохранится автоматически.</p>',
        1,
    )
    html = html.replace(
        "<div class=\"container\">",
        """<div class="container">

  <div class="section reveal">
    <div class="section-label">Личный кабинет</div>
    <h2>Сначала оставь свой email</h2>
    <p>Он нужен нам в самом начале, чтобы создать и привязать твой личный кабинет. Это обязательное поле.</p>
    <p><em>Если у тебя уже есть аккаунт, всё равно укажи тот email, к которому хочешь его привязать.</em></p>
    <div class="spacer-sm"></div>
    <input id="participant-email" type="email" inputmode="email" autocomplete="email" placeholder="name@example.com">
  </div>

  <hr class="divider">""",
        1,
    )
    html = html.replace(
        '<textarea placeholder="Опиши своё идеальное состояние через месяц..."></textarea>',
        '<textarea id="vision-future" placeholder="Опиши своё идеальное состояние через месяц..."></textarea>',
        1,
    )
    html = html.replace(
        '<textarea placeholder="Напиши самое важное — в любой форме, любой длины..."></textarea>',
        '<textarea id="personal-context" placeholder="Напиши самое важное — в любой форме, любой длины..."></textarea>',
        1,
    )
    html = html.replace(
        '<div class="success-overlay" id="success">\n  <h2>Готово</h2>\n  <p>Я всё получила и скоро вернусь с рекомендациями.</p>\n</div>',
        '<div class="success-overlay" id="success">\n  <h2>Сохранено</h2>\n  <p id="success-message">Анкета сохранена. По этой же ссылке можно в любой момент вернуться и продолжить редактирование.</p>\n  <div class="success-actions">\n    <button class="submit-btn" id="continue-editing" type="button">Продолжить редактировать</button>\n    <button class="success-secondary-btn" id="success-close" type="button">Закрыть</button>\n  </div>\n</div>',
        1,
    )
    html = html.replace(
        '<button class="submit-btn" onclick="handleSubmit()">\n      Отправить <span>→</span>\n    </button>',
        '<button class="submit-btn" id="save-questionnaire" onclick="handleSubmit()">\n      Сохранить и редактировать <span>→</span>\n    </button>\n    <div class="save-note" id="save-note">По этой ссылке всегда будет открываться актуальная сохранённая версия анкеты.</div>',
        1,
    )
    return html


def build_runtime_script(name: str, slug: str) -> str:
    return f"""
<script>
  const FORM_ENDPOINT = 'https://high-performance-leads.markesbootcamp.workers.dev';
  const PARTICIPANT_NAME = {quote_js(name)};
  const PARTICIPANT_SLUG = {quote_js(slug)};
  const LOAD_ENDPOINT = `${{FORM_ENDPOINT}}/participant-questionnaire?slug=${{encodeURIComponent(PARTICIPANT_SLUG)}}`;
  const DRAFT_KEY = `hp-participant-questionnaire-${{PARTICIPANT_SLUG}}-v1`;
  const LAST_SAVED_KEY = `${{DRAFT_KEY}}:last-saved-at`;
  const DRAFT_VERSION = 2;
  const CONTROL_CHARS_RE = /[\\u0000-\\u0008\\u000B\\u000C\\u000E-\\u001F\\u007F]/g;
  const BIDI_CONTROL_RE = /[\\u202A-\\u202E\\u2066-\\u2069]/g;
  const LEGACY_COURSE_VALUES = new Set(['care', 'basics', 'superhuman', 'abs', 'woman-health', 'soft-power', 'stretch', 'pregnancy', 'mama', 'bed', 'body-contact']);
  const LEGACY_PELVIC_LABELS = [
    'Попадание воздуха во влагалище во время секса',
    'Боли или тяжесть в области лобка',
    'Частое мочеиспускание или недержание при нагрузке, смехе, кашле',
    'Ничего из перечисленного'
  ];
  const LEGACY_NUTRITION_LABELS = [
    'Диагностировано РПП',
    'Подозреваю РПП, к специалисту не обращалась',
    'Отношения с едой в порядке',
    'Часто беспокоюсь о весе, ограничиваю себя',
    'Мысли о еде занимают непропорционально много времени',
    'Бывают эпизоды переедания',
    'Строго считаю калории',
    'Избегаю углеводов или сахара',
    'Окружающие замечают, что я зациклена на весе',
    'Регулярно чувствую вину после еды'
  ];

  function normalizeValue(value, multiline = false) {{
    const cleaned = String(value || '')
      .replace(/\\r\\n?/g, '\\n')
      .replace(CONTROL_CHARS_RE, '')
      .replace(BIDI_CONTROL_RE, '')
      .trim();

    if (!multiline) {{
      return cleaned.replace(/\\s+/g, ' ').trim();
    }}

    return cleaned
      .split('\\n')
      .map((line) => line.trimEnd())
      .join('\\n')
      .replace(/\\n{{3,}}/g, '\\n\\n')
      .trim();
  }}

  function getVipBlockByTitle(title) {{
    return [...document.querySelectorAll('.vip-block')].find((block) => {{
      const blockTitle = block.querySelector('.vip-title');
      return blockTitle && blockTitle.textContent.trim() === title;
    }});
  }}

  function formatDate(value) {{
    if (!value) {{
      return '';
    }}

    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {{
      return '';
    }}

    return date.toLocaleString('ru-RU', {{
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }});
  }}

  function autoResizeTextarea(textarea) {{
    if (!textarea) {{
      return;
    }}

    textarea.style.height = 'auto';
    textarea.style.height = `${{Math.max(textarea.scrollHeight, 80)}}px`;
  }}

  function autoResizeAllTextareas() {{
    document.querySelectorAll('textarea').forEach((textarea) => autoResizeTextarea(textarea));
  }}

  function textFromBlock(title) {{
    const block = getVipBlockByTitle(title);
    const textarea = block?.querySelector('textarea');
    return normalizeValue(textarea?.value || '', true);
  }}

  function inputFromBlock(title, placeholderStartsWith) {{
    const block = getVipBlockByTitle(title);
    const inputs = [...(block?.querySelectorAll('input') || [])];
    const target = inputs.find((input) => (input.getAttribute('placeholder') || '').startsWith(placeholderStartsWith));
    return normalizeValue(target?.value || '');
  }}

  function checkedLabelsFromBlock(title) {{
    const block = getVipBlockByTitle(title);
    if (!block) {{
      return [];
    }}

    return [...block.querySelectorAll('input[type=\"checkbox\"]:checked')].map((input) => {{
      const label = input.closest('label');
      const textNode = label?.querySelector('.checkbox-label');
      return normalizeValue(textNode?.textContent || '');
    }}).filter(Boolean);
  }}

  function setTextInBlock(title, value) {{
    const block = getVipBlockByTitle(title);
    const textarea = block?.querySelector('textarea');
    if (textarea) {{
      textarea.value = value || '';
      autoResizeTextarea(textarea);
    }}
  }}

  function setInputInBlock(title, placeholderStartsWith, value) {{
    const block = getVipBlockByTitle(title);
    const inputs = [...(block?.querySelectorAll('input') || [])];
    const target = inputs.find((input) => (input.getAttribute('placeholder') || '').startsWith(placeholderStartsWith));
    if (target) {{
      target.value = value || '';
    }}
  }}

  function setCheckedLabelsInBlock(title, labels) {{
    const normalized = new Set((labels || []).map((label) => normalizeValue(label)));
    const block = getVipBlockByTitle(title);
    if (!block) {{
      return;
    }}

    [...block.querySelectorAll('input[type="checkbox"]')].forEach((input) => {{
      const label = input.closest('label');
      const textNode = label?.querySelector('.checkbox-label');
      const value = normalizeValue(textNode?.textContent || '');
      input.checked = normalized.has(value);
    }});
  }}

  function buildEmptyResponseData() {{
    return {{
      participantEmail: '',
      visionFuture: '',
      selectedPath: '',
      courseChoice: '',
      personalContext: '',
      vip: {{
        purpose: '',
        age: '',
        height: '',
        weight: '',
        childrenStatus: '',
        childrenDetail: '',
        pregnantDetail: '',
        healthRestrictions: '',
        diastasis: '',
        pelvicFloorFlags: [],
        nutritionFlags: [],
        typicalDay: '',
        foodHabits: '',
        medications: '',
        curatorMessage: ''
      }}
    }};
  }}

  function preferMeaningful(current, fallback) {{
    return hasMeaningfulValue(current) ? current : fallback;
  }}

  function mergeStructuredData(fallback, current) {{
    if (Array.isArray(fallback) || Array.isArray(current)) {{
      return hasMeaningfulValue(current) ? current : (fallback || []);
    }}

    if ((fallback && typeof fallback === 'object') || (current && typeof current === 'object')) {{
      const merged = {{}};
      const keys = new Set([
        ...Object.keys(fallback || {{}}),
        ...Object.keys(current || {{}})
      ]);

      keys.forEach((key) => {{
        merged[key] = mergeStructuredData(fallback?.[key], current?.[key]);
      }});
      return merged;
    }}

    return hasMeaningfulValue(current) ? current : (fallback ?? current ?? '');
  }}

  function isLikelyMetric(value) {{
    if (typeof value !== 'string') {{
      return false;
    }}

    const normalized = normalizeValue(value);
    if (!normalized) {{
      return false;
    }}

    return /^\\d{{1,3}}([.,]\\d+)?$/.test(normalized);
  }}

  function parseLegacyDraftState(state) {{
    const values = Array.isArray(state) ? state : Array.isArray(state?.fields) ? state.fields : [];
    if (!values.length) {{
      return null;
    }}

    const parsed = {{
      email: '',
      selectedPath: '',
      courseChoice: '',
      personalContext: '',
      responseData: buildEmptyResponseData()
    }};

    if (typeof values[0] === 'string') {{
      parsed.email = normalizeValue(values[0]);
      parsed.responseData.participantEmail = parsed.email;
    }}

    if (typeof values[1] === 'string') {{
      parsed.responseData.visionFuture = normalizeValue(values[1], true);
    }}

    let ageIndex = -1;
    for (let index = 3; index <= 5; index += 1) {{
      if (
        isLikelyMetric(values[index]) &&
        isLikelyMetric(values[index + 1]) &&
        isLikelyMetric(values[index + 2]) &&
        typeof values[index + 3] === 'boolean' &&
        typeof values[index + 4] === 'boolean'
      ) {{
        ageIndex = index;
        break;
      }}
    }}

    if (ageIndex === -1) {{
      const freeform = normalizeValue(values[2], true);
      if (freeform) {{
        parsed.selectedPath = LEGACY_COURSE_VALUES.has(freeform) ? 'short' : 'personal';
        if (parsed.selectedPath === 'short') {{
          parsed.courseChoice = freeform;
          parsed.responseData.courseChoice = freeform;
        }} else {{
          parsed.personalContext = freeform;
          parsed.responseData.personalContext = freeform;
        }}
        parsed.responseData.selectedPath = parsed.selectedPath;
      }}
      return parsed;
    }}

    const pathField = normalizeValue(values[2], true);
    const purposeIndex = ageIndex === 4 ? 3 : -1;
    if (pathField) {{
      if (LEGACY_COURSE_VALUES.has(pathField)) {{
        parsed.selectedPath = 'short';
        parsed.courseChoice = pathField;
        parsed.responseData.courseChoice = pathField;
      }} else {{
        parsed.selectedPath = 'personal';
        parsed.personalContext = pathField;
        parsed.responseData.personalContext = pathField;
      }}
      parsed.responseData.selectedPath = parsed.selectedPath;
    }}

    if (purposeIndex !== -1 && typeof values[purposeIndex] === 'string') {{
      parsed.responseData.vip.purpose = normalizeValue(values[purposeIndex], true);
    }}

    parsed.responseData.vip.age = normalizeValue(values[ageIndex]);
    parsed.responseData.vip.height = normalizeValue(values[ageIndex + 1]);
    parsed.responseData.vip.weight = normalizeValue(values[ageIndex + 2]);

    let cursor = ageIndex + 3;
    const noChildren = Boolean(values[cursor]);
    const hasChildren = Boolean(values[cursor + 1]);
    cursor += 2;

    let childrenDetail = '';
    let pregnant = false;
    if (typeof values[cursor] === 'string') {{
      childrenDetail = normalizeValue(values[cursor], true);
      cursor += 1;
      pregnant = Boolean(values[cursor]);
      cursor += 1;
    }} else if (typeof values[cursor] === 'boolean') {{
      pregnant = Boolean(values[cursor]);
      cursor += 1;
    }}

    parsed.responseData.vip.childrenStatus = pregnant ? 'pregnant' : hasChildren ? 'yes' : noChildren ? 'no' : '';
    parsed.responseData.vip.childrenDetail = childrenDetail;
    parsed.responseData.vip.healthRestrictions = normalizeValue(values[cursor] || '', true);
    cursor += 1;
    parsed.responseData.vip.diastasis = normalizeValue(values[cursor] || '');
    cursor += 1;

    const flagValues = [];
    while (cursor < values.length && typeof values[cursor] === 'boolean') {{
      flagValues.push(Boolean(values[cursor]));
      cursor += 1;
    }}

    parsed.responseData.vip.pelvicFloorFlags = LEGACY_PELVIC_LABELS.filter((_, index) => Boolean(flagValues[index]));
    parsed.responseData.vip.nutritionFlags = LEGACY_NUTRITION_LABELS.filter((_, index) => Boolean(flagValues[index + LEGACY_PELVIC_LABELS.length]));

    const remainingText = values.slice(cursor).filter((value) => typeof value === 'string' && normalizeValue(value, true));
    parsed.responseData.vip.typicalDay = normalizeValue(remainingText[0] || '', true);
    parsed.responseData.vip.foodHabits = normalizeValue(remainingText[1] || '', true);
    parsed.responseData.vip.medications = normalizeValue(remainingText[2] || '', true);
    parsed.responseData.vip.curatorMessage = normalizeValue(remainingText[3] || '', true);

    return parsed;
  }}

  function hydrateStoredRecord(record) {{
    const legacy = parseLegacyDraftState(record?.draftState);
    const mergedResponseData = mergeStructuredData(legacy?.responseData || buildEmptyResponseData(), record?.responseData || {{}});
    return {{
      ...record,
      email: preferMeaningful(record?.email, legacy?.email || mergedResponseData.participantEmail || ''),
      selectedPath: preferMeaningful(record?.selectedPath, mergedResponseData.selectedPath || legacy?.selectedPath || ''),
      courseChoice: preferMeaningful(record?.courseChoice, mergedResponseData.courseChoice || legacy?.courseChoice || ''),
      personalContext: preferMeaningful(record?.personalContext, mergedResponseData.personalContext || legacy?.personalContext || ''),
      responseData: mergedResponseData,
    }};
  }}

  function applySavedRecord(record) {{
    const responseData = record?.responseData || {{}};
    const vip = responseData.vip || {{}};
    const participantEmail = record?.email || responseData.participantEmail || '';
    const selectedPath = record?.selectedPath || responseData.selectedPath || '';
    const courseChoice = record?.courseChoice || responseData.courseChoice || '';
    const personalContext = record?.personalContext || responseData.personalContext || '';

    const emailField = document.getElementById('participant-email');
    if (emailField) {{
      emailField.value = participantEmail;
    }}

    const visionField = document.getElementById('vision-future');
    if (visionField) {{
      visionField.value = responseData.visionFuture || '';
      autoResizeTextarea(visionField);
    }}

    const courseSelect = document.getElementById('course-select');
    if (courseSelect) {{
      courseSelect.value = courseChoice;
    }}

    const personalContextField = document.getElementById('personal-context');
    if (personalContextField) {{
      personalContextField.value = personalContext;
      autoResizeTextarea(personalContextField);
    }}

    setTextInBlock('Я здесь, чтобы...', vip.purpose);
    setInputInBlock('Возраст / Рост / Вес', 'Возраст', vip.age);
    setInputInBlock('Возраст / Рост / Вес', 'Рост', vip.height);
    setInputInBlock('Возраст / Рост / Вес', 'Вес', vip.weight);
    setTextInBlock('Здоровье и ограничения', vip.healthRestrictions);
    setInputInBlock('Диастаз', 'Например', vip.diastasis);
    setCheckedLabelsInBlock('Отметь, если актуально', vip.pelvicFloorFlags);
    setCheckedLabelsInBlock('Отношение к питанию', vip.nutritionFlags);
    setTextInBlock('Твой обычный день', vip.typicalDay);
    setTextInBlock('Питание и привычки', vip.foodHabits);
    setTextInBlock('Препараты', vip.medications);
    setTextInBlock('Сообщение для куратора', vip.curatorMessage);

    document.querySelectorAll('input[name="children"]').forEach((radio) => {{
      radio.checked = false;
    }});
    const childrenValue = normalizeValue(vip.childrenStatus || '');
    if (childrenValue) {{
      const radio = document.querySelector(`input[name="children"][value="${{childrenValue}}"]`);
      if (radio) {{
        radio.checked = true;
      }}
    }}

    const childrenDetail = document.querySelector('#children-detail input');
    if (childrenDetail) {{
      childrenDetail.value = vip.childrenDetail || '';
    }}

    const pregnantDetail = document.querySelector('#pregnant-detail input');
    if (pregnantDetail) {{
      pregnantDetail.value = vip.pregnantDetail || '';
    }}

    syncConditionalState(selectedPath);
  }}

  function getSelectedPath() {{
    if (document.getElementById('path1')?.classList.contains('active')) {{
      return 'short';
    }}
    if (document.getElementById('path2')?.classList.contains('active')) {{
      return 'personal';
    }}
    return '';
  }}

  function syncConditionalState(explicitPath = '') {{
    const inferredPath =
      normalizeValue(document.getElementById('course-select')?.value || '') ? 'short' :
      normalizeValue(document.getElementById('personal-context')?.value || '', true) ? 'personal' :
      getSelectedPath();
    const selectedPath = explicitPath || inferredPath;
    const path1Active = selectedPath === 'short';
    const path2Active = selectedPath === 'personal';
    const path1 = document.getElementById('path1');
    const path2 = document.getElementById('path2');
    const path1Fields = document.getElementById('path1-fields');
    const path2Fields = document.getElementById('path2-fields');

    path1?.classList.toggle('active', path1Active);
    path2?.classList.toggle('active', path2Active);
    path1Fields?.classList.toggle('visible', path1Active);
    path2Fields?.classList.toggle('visible', path2Active);

    const selectedChildren = document.querySelector('input[name="children"]:checked');
    const childrenDetail = document.getElementById('children-detail');
    const pregnantDetail = document.getElementById('pregnant-detail');
    if (childrenDetail) {{
      childrenDetail.style.display = selectedChildren?.value === 'yes' ? 'block' : 'none';
    }}
    if (pregnantDetail) {{
      pregnantDetail.style.display = selectedChildren?.value === 'pregnant' ? 'block' : 'none';
    }}

    autoResizeAllTextareas();
  }}

  function collectDraftState() {{
    const responseData = collectResponseData();
    return {{
      version: DRAFT_VERSION,
      updatedAt: new Date().toISOString(),
      selectedPath: responseData.selectedPath,
      participantEmail: responseData.participantEmail,
      responseData,
    }};
  }}

  function restoreDraftState(state) {{
    if (state && typeof state === 'object' && Number(state.version) >= DRAFT_VERSION && state.responseData) {{
      applySavedRecord({{
        email: state.participantEmail || state.responseData.participantEmail || '',
        selectedPath: state.selectedPath || state.responseData.selectedPath || '',
        courseChoice: state.responseData.courseChoice || '',
        personalContext: state.responseData.personalContext || '',
        responseData: state.responseData,
      }});
      return;
    }}

    const parsedLegacy = parseLegacyDraftState(state);
    if (parsedLegacy) {{
      applySavedRecord(parsedLegacy);
    }}
  }}

  function collectResponseData() {{
    const selectedPath = getSelectedPath();
    const selectedChildren = document.querySelector('input[name="children"]:checked');
    const participantEmail = normalizeValue(document.getElementById('participant-email')?.value || '');

    return {{
      participantEmail,
      visionFuture: normalizeValue(document.getElementById('vision-future')?.value || '', true),
      selectedPath,
      courseChoice: normalizeValue(document.getElementById('course-select')?.value || ''),
      personalContext: normalizeValue(document.getElementById('personal-context')?.value || '', true),
      vip: {{
        purpose: textFromBlock('Я здесь, чтобы...'),
        age: inputFromBlock('Возраст / Рост / Вес', 'Возраст'),
        height: inputFromBlock('Возраст / Рост / Вес', 'Рост'),
        weight: inputFromBlock('Возраст / Рост / Вес', 'Вес'),
        childrenStatus: normalizeValue(selectedChildren?.value || ''),
        childrenDetail: normalizeValue(document.querySelector('#children-detail input')?.value || ''),
        pregnantDetail: normalizeValue(document.querySelector('#pregnant-detail input')?.value || ''),
        healthRestrictions: textFromBlock('Здоровье и ограничения'),
        diastasis: inputFromBlock('Диастаз', 'Например'),
        pelvicFloorFlags: checkedLabelsFromBlock('Отметь, если актуально'),
        nutritionFlags: checkedLabelsFromBlock('Отношение к питанию'),
        typicalDay: textFromBlock('Твой обычный день'),
        foodHabits: textFromBlock('Питание и привычки'),
        medications: textFromBlock('Препараты'),
        curatorMessage: textFromBlock('Сообщение для куратора')
      }}
    }};
  }}

  function saveDraft() {{
    localStorage.setItem(DRAFT_KEY, JSON.stringify(collectDraftState()));
  }}

  function setSaveNote(message) {{
    const saveNote = document.getElementById('save-note');
    if (saveNote) {{
      saveNote.textContent = message;
    }}
  }}

  async function loadSavedVersion() {{
    setSaveNote('Загружаю сохранённую версию анкеты...');

    try {{
      const response = await fetch(LOAD_ENDPOINT);
      if (!response.ok) {{
        throw new Error('load_failed');
      }}

      const result = await response.json();
      if (!result.ok || !result.found || !result.record) {{
        setSaveNote('Пока нет сохранённой версии. Можно заполнить анкету и сохранить её по этой же ссылке.');
        return false;
      }}

      applySavedRecord(hydrateStoredRecord(result.record));
      const savedAt = formatDate(result.record.submittedAt || result.updatedAt);
      setSaveNote(savedAt ? `Открыта сохранённая версия от ${{savedAt}}.` : 'Открыта последняя сохранённая версия анкеты.');
      localStorage.setItem(LAST_SAVED_KEY, result.record.submittedAt || result.updatedAt || '');
      return true;
    }} catch (error) {{
      setSaveNote('Не удалось загрузить сохранённую версию. Можно продолжить с локальным черновиком и сохранить позже.');
      return false;
    }}
  }}

  function parseComparableTime(value) {{
    if (!value) {{
      return 0;
    }}

    const parsed = Date.parse(String(value));
    return Number.isFinite(parsed) ? parsed : 0;
  }}

  function shouldRestoreLocalDraft(state, hasServerVersion) {{
    if (!hasServerVersion) {{
      return true;
    }}

    const draftVersion = Number(state?.version || 0);
    if (draftVersion < DRAFT_VERSION) {{
      return false;
    }}

    const localUpdatedAt = parseComparableTime(state?.updatedAt || state?.submittedAt || '');
    const serverSavedAt = parseComparableTime(localStorage.getItem(LAST_SAVED_KEY) || '');
    if (!localUpdatedAt || !serverSavedAt) {{
      return false;
    }}

    return localUpdatedAt > serverSavedAt;
  }}

  function restoreLocalDraft(hasServerVersion = false) {{
    const savedDraft = localStorage.getItem(DRAFT_KEY);
    if (!savedDraft) {{
      return false;
    }}

    try {{
      const draftState = JSON.parse(savedDraft);
      if (!shouldRestoreLocalDraft(draftState, hasServerVersion)) {{
        return false;
      }}
      restoreDraftState(draftState);
      setSaveNote(
        hasServerVersion
          ? 'Восстановлен более новый локальный черновик из этого браузера.'
          : 'Восстановлен локальный черновик из этого браузера.'
      );
      return true;
    }} catch (error) {{
      localStorage.removeItem(DRAFT_KEY);
      return false;
    }}
  }}

  function buildPayload() {{
    const responseData = collectResponseData();
    const participantEmail = responseData.participantEmail || '';

    return {{
      kind: 'participant-questionnaire',
      participantName: PARTICIPANT_NAME,
      participantSlug: PARTICIPANT_SLUG,
      email: participantEmail,
      draftState: collectDraftState(),
      selectedPath: responseData.selectedPath,
      courseChoice: responseData.courseChoice,
      personalContext: responseData.personalContext,
      responseData,
      source: 'high-performance-participant-questionnaire',
      pageUrl: window.location.href,
      submittedAt: new Date().toISOString()
    }};
  }}

  function hasMeaningfulValue(value) {{
    if (Array.isArray(value)) {{
      return value.some(hasMeaningfulValue);
    }}
    if (value && typeof value === 'object') {{
      return Object.values(value).some(hasMeaningfulValue);
    }}
    return Boolean(normalizeValue(value, true));
  }}

  function formatSaveError(errorCode, detail = '') {{
    const code = normalizeValue(errorCode || '');
    const extra = normalizeValue(detail || '', true);

    if (code === 'invalid_email') {{
      return 'Не удалось сохранить анкету: email указан с ошибкой.';
    }}
    if (code === 'missing_required_fields') {{
      return 'Не удалось сохранить анкету: похоже, не заполнено обязательное поле.';
    }}
    if (code === 'origin_not_allowed') {{
      return 'Не удалось сохранить анкету: открыта не та версия страницы. Лучше открыть ссылку заново.';
    }}
    if (code === 'github_write_failed') {{
      return extra
        ? `Не удалось сохранить анкету на сервере: ${{extra}}.`
        : 'Не удалось сохранить анкету на сервере.';
    }}
    if (code === 'request_failed') {{
      return 'Не удалось сохранить анкету: сервер вернул ошибку.';
    }}
    if (code === 'network_error') {{
      return 'Не удалось сохранить анкету: похоже на сетевую ошибку.';
    }}
    return 'Не удалось сохранить анкету. Локальный черновик остался в браузере.';
  }}

  async function handleSubmit() {{
    const payload = buildPayload();
    const successOverlay = document.getElementById('success');
    const successMessage = document.getElementById('success-message');
    const submitButton = document.getElementById('save-questionnaire');
    const emailValue = payload.email || '';

    if (!emailValue) {{
      alert('Сначала укажи email. Он нужен для привязки личного кабинета.');
      document.getElementById('participant-email')?.focus();
      return;
    }}

    if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(emailValue)) {{
      alert('Похоже, email указан с ошибкой. Проверь, пожалуйста, адрес ещё раз.');
      document.getElementById('participant-email')?.focus();
      return;
    }}

    if (!hasMeaningfulValue(payload.responseData)) {{
      alert('Заполни хотя бы один блок анкеты, чтобы мы могли что-то подобрать.');
      return;
    }}

    setSaveNote('Сохраняю анкету...');
    submitButton.disabled = true;
    submitButton.style.opacity = '0.7';

    try {{
      const response = await fetch(FORM_ENDPOINT, {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json'
        }},
        body: JSON.stringify(payload)
      }});

      const result = await response.json().catch(() => ({{}}));

      if (!response.ok) {{
        const requestError = new Error(normalizeValue(result?.error || 'request_failed') || 'request_failed');
        requestError.detail = normalizeValue(result?.detail || '', true);
        throw requestError;
      }}

      const savedAt = formatDate(payload.submittedAt);
      localStorage.setItem(DRAFT_KEY, JSON.stringify(payload.draftState));
      localStorage.setItem(LAST_SAVED_KEY, payload.submittedAt);
      successMessage.textContent =
        result.mode === 'updated'
          ? 'Анкета сохранена заново. По этой же ссылке всегда откроется её актуальная версия.'
          : 'Анкета сохранена. По этой же ссылке можно в любой момент вернуться и продолжить редактирование.';
      setSaveNote(savedAt ? `Сохранено ${{savedAt}}.` : 'Анкета сохранена.');
      successOverlay.classList.add('visible');
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }} catch (error) {{
      const errorCode = normalizeValue(error?.message || '') || 'network_error';
      const errorDetail = normalizeValue(error?.detail || '', true);
      const readableError = formatSaveError(errorCode, errorDetail);
      console.error('Participant questionnaire save failed', {{
        participantSlug: PARTICIPANT_SLUG,
        errorCode,
        errorDetail,
        payload
      }});
      setSaveNote(readableError);
      alert(readableError);
    }} finally {{
      submitButton.disabled = false;
      submitButton.style.opacity = '1';
    }}
  }}

  document.querySelectorAll('select, textarea, input').forEach((field) => {{
    field.addEventListener('input', () => {{
      if (field.tagName === 'TEXTAREA') {{
        autoResizeTextarea(field);
      }}
      syncConditionalState();
      saveDraft();
    }});
    field.addEventListener('change', () => {{
      syncConditionalState();
      saveDraft();
    }});
  }});

  document.getElementById('continue-editing')?.addEventListener('click', () => {{
    document.getElementById('success')?.classList.remove('visible');
    document.getElementById('personal-context')?.focus();
  }});

  document.getElementById('success-close')?.addEventListener('click', () => {{
    document.getElementById('success')?.classList.remove('visible');
  }});

  (async () => {{
    autoResizeAllTextareas();
    const hasServerVersion = await loadSavedVersion();
    restoreLocalDraft(hasServerVersion);
    syncConditionalState();
  }})();
</script>
"""


def build_participant_page(template: str, participant: dict[str, str]) -> str:
    slug = participant["slug"]
    html = add_personalization(template, participant["public_name"], participant["for_name"])
    html = html.replace("</body>\n</html>", f"{build_runtime_script(participant['public_name'], slug)}\n</body>\n</html>", 1)
    if participant.get("issue"):
        source_comment = (
            f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['public_name']} "
            f"from GitHub issue #{participant['issue']}: https://github.com/OLYMARKES/high-performance-leads/issues/{participant['issue']} -->\n"
        )
    else:
        source_comment = (
            f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['public_name']} "
            f"from manual roster update -->\n"
        )
    return source_comment + html


def build_index_page() -> str:
    return """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>HIGH PERFORMANCE — Private Questionnaires</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0e0e0e;
      --surface: #181818;
      --border: #272727;
      --text: #ebebeb;
      --text-secondary: #999;
      --accent: #c9a96e;
      --radius: 14px;
    }
    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      -webkit-font-smoothing: antialiased;
    }
    .card {
      width: min(680px, 100%);
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius);
      padding: 36px 28px;
      text-align: center;
    }
    .label {
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 6px;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 22px;
    }
    h1 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(36px, 7vw, 64px);
      font-weight: 400;
      line-height: 1.06;
      margin-bottom: 18px;
    }
    p {
      color: var(--text-secondary);
      font-size: 16px;
      line-height: 1.8;
      font-weight: 300;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="label">High Performance</div>
    <h1>Private <em>Questionnaires</em></h1>
    <p>Эта директория не публикует список анкет. Открыть анкету можно только по персональной или командной ссылке.</p>
  </div>
</body>
</html>
"""


def build_team_page(entries: list[dict[str, str]]) -> str:
    cards_html = "\n".join(
        f"""
          <a class="card" href="{entry['filename']}">
            <span class="card-name">{entry['display_name']}</span>
            <span class="card-meta">персональная анкета · {entry['telegram_handle']}</span>
          </a>"""
        for entry in entries
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>HIGH PERFORMANCE — Team Access</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    :root {{
      --bg: #0e0e0e;
      --surface: #181818;
      --surface-hover: #1e1e1e;
      --border: #272727;
      --text: #ebebeb;
      --text-secondary: #999;
      --accent: #c9a96e;
      --accent-glow: rgba(201, 169, 110, 0.12);
      --radius: 14px;
    }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
      -webkit-font-smoothing: antialiased;
      padding: 40px 20px 80px;
    }}
    .container {{
      max-width: 1120px;
      margin: 0 auto;
    }}
    .hero {{
      text-align: center;
      padding: 48px 0 34px;
    }}
    .hero-label {{
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 6px;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 24px;
    }}
    h1 {{
      font-family: 'Playfair Display', serif;
      font-size: clamp(42px, 8vw, 72px);
      font-weight: 400;
      line-height: 1.04;
      margin-bottom: 18px;
    }}
    h1 em {{
      font-style: italic;
      color: var(--accent);
    }}
    .hero-sub {{
      max-width: 640px;
      margin: 0 auto;
      color: var(--text-secondary);
      font-size: 16px;
      font-weight: 300;
    }}
    .panel {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius);
      padding: 28px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 26px;
    }}
    .card {{
      display: block;
      text-decoration: none;
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius);
      padding: 22px 20px;
      transition: all 0.25s ease;
    }}
    .card:hover {{
      background: var(--surface-hover);
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-glow);
      transform: translateY(-1px);
    }}
    .card-name {{
      display: block;
      font-family: 'Playfair Display', serif;
      font-size: 30px;
      color: var(--text);
      line-height: 1.1;
    }}
    .card-meta {{
      display: block;
      color: var(--text-secondary);
      font-size: 13px;
      margin-top: 8px;
    }}
    @media (max-width: 900px) {{
      .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 640px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .panel {{ padding: 22px 18px; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="hero-label">High Performance</div>
      <h1>Team <em>Access</em></h1>
      <p class="hero-sub">Командная страница со всеми персональными анкетами. Эту ссылку не пересылаем участницам.</p>
    </div>

    <div class="panel">
      <div class="grid">
{cards_html}
      </div>
    </div>
  </div>
</body>
</html>
"""


def build_admin_page(snapshot_rows: list[dict[str, object]], snapshot_generated_at: str, snapshot_error: str | None) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>HIGH PERFORMANCE — Admin</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    :root {{
      --bg: #0e0e0e;
      --surface: #181818;
      --surface-hover: #1e1e1e;
      --border: #272727;
      --text: #ebebeb;
      --text-secondary: #999;
      --text-muted: #6f6f6f;
      --accent: #c9a96e;
      --accent-glow: rgba(201, 169, 110, 0.12);
      --radius: 16px;
    }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
      -webkit-font-smoothing: antialiased;
      padding: 32px 16px 56px;
    }}
    .container {{
      max-width: 1280px;
      margin: 0 auto;
    }}
    .hero {{
      text-align: center;
      padding: 28px 0 30px;
    }}
    .hero-label {{
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 6px;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 22px;
    }}
    h1 {{
      font-family: 'Playfair Display', serif;
      font-size: clamp(42px, 8vw, 68px);
      font-weight: 400;
      line-height: 1.02;
      margin-bottom: 16px;
    }}
    h1 em {{
      font-style: italic;
      color: var(--accent);
    }}
    .hero-sub {{
      max-width: 760px;
      margin: 0 auto;
      color: var(--text-secondary);
      font-size: 15px;
      font-weight: 300;
    }}
    .panel {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      margin-top: 18px;
    }}
    .snapshot-note {{
      color: var(--text-secondary);
      font-size: 13px;
    }}
    .snapshot-note strong {{
      color: var(--text);
      font-weight: 600;
    }}
    .snapshot-note.is-error {{
      color: #d98274;
    }}
    .input {{
      width: 100%;
      background: #141414;
      border: 1.5px solid var(--border);
      border-radius: var(--radius);
      color: var(--text);
      font: inherit;
      padding: 14px 16px;
      outline: none;
      margin-top: 14px;
    }}
    .input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }}
    .filter-bar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }}
    .button {{
      background: var(--accent);
      color: var(--bg);
      border: none;
      border-radius: 999px;
      padding: 13px 20px;
      font: inherit;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      cursor: pointer;
    }}
    .button.is-secondary {{
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border);
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }}
    .stat-card, .queue-card {{
      background: #141414;
      border: 1.5px solid var(--border);
      border-radius: var(--radius);
      padding: 18px;
    }}
    .stat-label {{
      font-size: 11px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--text-muted);
    }}
    .stat-value {{
      margin-top: 8px;
      font-family: 'Playfair Display', serif;
      font-size: 36px;
      line-height: 1;
      color: var(--text);
    }}
    .queue-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }}
    .queue-title {{
      font-family: 'Playfair Display', serif;
      font-size: 28px;
      line-height: 1.1;
    }}
    .queue-sub {{
      margin-top: 6px;
      color: var(--text-secondary);
      font-size: 13px;
    }}
    .queue-list {{
      margin-top: 18px;
      display: grid;
      gap: 10px;
    }}
    .queue-item {{
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      background: #101010;
    }}
    .queue-name {{
      font-weight: 600;
      color: var(--text);
    }}
    .queue-meta {{
      margin-top: 4px;
      color: var(--text-secondary);
      font-size: 12px;
      line-height: 1.6;
    }}
    .empty-note {{
      color: var(--text-muted);
      font-size: 13px;
    }}
    .table-wrap {{
      overflow-x: auto;
      margin-top: 18px;
      border-radius: var(--radius);
      border: 1.5px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 1080px;
      background: #141414;
    }}
    th, td {{
      padding: 14px 16px;
      text-align: left;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
      font-size: 14px;
    }}
    th {{
      color: var(--accent);
      font-size: 11px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      font-weight: 600;
    }}
    .participant-name {{
      display: block;
      font-weight: 600;
      color: var(--text);
    }}
    .participant-meta {{
      display: block;
      margin-top: 4px;
      color: var(--text-secondary);
      font-size: 12px;
      line-height: 1.5;
    }}
    .link-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 8px;
    }}
    .inline-link, .inline-link:visited {{
      color: var(--accent);
      text-decoration: none;
      font-size: 12px;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 12px;
      border: 1px solid var(--border);
      white-space: nowrap;
    }}
    .pill.needs-pick {{
      color: #f0c36f;
      border-color: rgba(240, 195, 111, 0.4);
      background: rgba(240, 195, 111, 0.08);
    }}
    .pill.ready-open {{
      color: #9fc47b;
      border-color: rgba(159, 196, 123, 0.4);
      background: rgba(159, 196, 123, 0.08);
    }}
    .pill.waiting {{
      color: #999;
      background: transparent;
    }}
    .pill.review {{
      color: #d9a874;
      border-color: rgba(217, 168, 116, 0.4);
      background: rgba(217, 168, 116, 0.08);
    }}
    .action-text {{
      display: block;
      font-weight: 600;
      color: var(--text);
    }}
    .action-note {{
      display: block;
      margin-top: 4px;
      color: var(--text-secondary);
      font-size: 12px;
      line-height: 1.5;
    }}
    .details-btn {{
      background: transparent;
      color: var(--accent);
      border: 1px solid rgba(201, 169, 110, 0.24);
      border-radius: 999px;
      padding: 8px 12px;
      cursor: pointer;
      font: inherit;
      font-size: 12px;
    }}
    .modal {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(8, 8, 8, 0.82);
      padding: 24px;
      z-index: 100;
      overflow: auto;
    }}
    .modal.visible {{ display: block; }}
    .modal-card {{
      max-width: 840px;
      margin: 40px auto;
      background: #111;
      border: 1.5px solid var(--border);
      border-radius: 18px;
      padding: 24px;
    }}
    .modal-header {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
      margin-bottom: 16px;
    }}
    .modal-title {{
      font-family: 'Playfair Display', serif;
      font-size: 32px;
      line-height: 1.1;
    }}
    .close-btn {{
      background: transparent;
      color: var(--text-secondary);
      border: none;
      font: inherit;
      cursor: pointer;
      font-size: 14px;
    }}
    .detail-section {{
      padding-top: 16px;
      margin-top: 16px;
      border-top: 1px solid var(--border);
    }}
    .detail-section h3 {{
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--accent);
      margin-bottom: 10px;
    }}
    .detail-section p, .detail-section li {{
      color: var(--text-secondary);
      font-size: 14px;
      line-height: 1.8;
    }}
    .detail-section ul {{
      padding-left: 18px;
    }}
    @media (max-width: 980px) {{
      .stats-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .queue-grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 640px) {{
      .stats-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="hero-label">High Performance</div>
      <h1>Course <em>dashboard</em></h1>
      <p class="hero-sub">
        Операционный дашборд по анкетам: кто уже выбрал курс, кому нужно открыть доступ и где нужен ручной подбор.
      </p>
    </div>

    <div class="panel">
      <div class="snapshot-note">
        <strong>Снимок данных:</strong> {format_snapshot_time(snapshot_generated_at) or snapshot_generated_at}.
        Страница уже содержит готовые данные и не требует GitHub token.
      </div>
      {"<div class=\"snapshot-note is-error\">Не удалось обновить snapshot из GitHub. Открыта последняя собранная версия без новых данных.</div>" if snapshot_error else ""}
      <input class="input" id="search-input" type="text" placeholder="Поиск по имени, Telegram, email, курсу или slug">
      <div class="filter-bar" id="filter-bar">
        <button class="button" data-filter="all" type="button">Все</button>
        <button class="button is-secondary" data-filter="needs-pick" type="button">Нужно подобрать</button>
        <button class="button is-secondary" data-filter="ready-open" type="button">Нужно открыть</button>
        <button class="button is-secondary" data-filter="review" type="button">Проверить</button>
        <button class="button is-secondary" data-filter="waiting" type="button">Ждём анкету</button>
      </div>
    </div>

    <div class="panel">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Всего участниц</div>
          <div class="stat-value" id="stat-total">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Нужно подобрать</div>
          <div class="stat-value" id="stat-needs-pick">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Нужно открыть</div>
          <div class="stat-value" id="stat-ready-open">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Ждём анкету</div>
          <div class="stat-value" id="stat-waiting">0</div>
        </div>
      </div>
    </div>

    <div class="panel">
      <div class="queue-grid">
        <div class="queue-card">
          <div class="queue-title">Открыть курс</div>
          <div class="queue-sub">Участницы, которые уже выбрали курс и готовы к открытию доступа.</div>
          <div class="queue-list" id="queue-ready-open"></div>
        </div>
        <div class="queue-card">
          <div class="queue-title">Подобрать курс</div>
          <div class="queue-sub">Участницы, где по анкете нужен ручной подбор команды.</div>
          <div class="queue-list" id="queue-needs-pick"></div>
        </div>
      </div>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Участница</th>
              <th>Статус</th>
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
    </div>
  </div>

  <div class="modal" id="details-modal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title" id="modal-title">Анкета</div>
        <button class="close-btn" id="close-modal" type="button">закрыть</button>
      </div>
      <div id="modal-content"></div>
    </div>
  </div>

  <script>
    const ALL_ROWS = {script_json(snapshot_rows)};
    const searchInput = document.getElementById('search-input');
    const filterBar = document.getElementById('filter-bar');
    const resultsBody = document.getElementById('results-body');
    const queueReadyOpen = document.getElementById('queue-ready-open');
    const queueNeedsPick = document.getElementById('queue-needs-pick');
    const statTotal = document.getElementById('stat-total');
    const statNeedsPick = document.getElementById('stat-needs-pick');
    const statReadyOpen = document.getElementById('stat-ready-open');
    const statWaiting = document.getElementById('stat-waiting');
    const detailsModal = document.getElementById('details-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    const closeModalButton = document.getElementById('close-modal');

    let activeFilter = 'all';

    function escapeHtml(value) {{
      return String(value || '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;');
    }}

    function truncateText(value, limit = 72) {{
      const text = String(value || '').trim();
      if (!text) {{
        return '<small>—</small>';
      }}
      return escapeHtml(text.length > limit ? `${{text.slice(0, limit)}}...` : text);
    }}

    function paragraph(value) {{
      if (!value) {{
        return '<p>—</p>';
      }}
      return `<p>${{escapeHtml(String(value)).replaceAll('\\n', '<br>')}}</p>`;
    }}

    function list(values) {{
      if (!values || !values.length) {{
        return '<p>—</p>';
      }}
      return `<ul>${{values.map((value) => `<li>${{escapeHtml(value)}}</li>`).join('')}}</ul>`;
    }}

    function sectionHtml(title, body) {{
      return `
        <div class="detail-section">
          <h3>${{escapeHtml(title)}}</h3>
          ${{body}}
        </div>
      `;
    }}

    function getVisibleRows() {{
      const query = searchInput.value.trim().toLowerCase();
      return ALL_ROWS.filter((row) => {{
        const haystack = [
          row.displayName,
          row.telegramHandle,
          row.slug,
          row.email,
          row.selectedCourse,
          row.selectedCourseLabel,
          row.summary?.personalContext,
          row.summary?.visionFuture
        ].join(' ').toLowerCase();
        const matchesFilter = activeFilter === 'all' ? true : row.statusKey === activeFilter;
        const matchesSearch = !query || haystack.includes(query);
        return matchesFilter && matchesSearch;
      }});
    }}

    function updateStats() {{
      statTotal.textContent = String(ALL_ROWS.length);
      statNeedsPick.textContent = String(ALL_ROWS.filter((row) => row.statusKey === 'needs-pick').length);
      statReadyOpen.textContent = String(ALL_ROWS.filter((row) => row.statusKey === 'ready-open').length);
      statWaiting.textContent = String(ALL_ROWS.filter((row) => row.statusKey === 'waiting').length);
    }}

    function renderQueue(container, rows, emptyMessage) {{
      if (!rows.length) {{
        container.innerHTML = `<div class="empty-note">${{escapeHtml(emptyMessage)}}</div>`;
        return;
      }}

      container.innerHTML = rows.map((row) => `
        <div class="queue-item">
          <div class="queue-name">${{escapeHtml(row.displayName)}}</div>
          <div class="queue-meta">${{escapeHtml(row.telegramHandle)}}${{row.email ? ` · ${{escapeHtml(row.email)}}` : ''}}</div>
          <div class="queue-meta">${{escapeHtml(row.actionTitle)}}${{row.selectedCourseLabel && row.selectedCourseLabel !== '—' ? ` · ${{escapeHtml(row.selectedCourseLabel)}}` : ''}}</div>
        </div>
      `).join('');
    }}

    function renderRows(rows) {{
      if (!rows.length) {{
        resultsBody.innerHTML = '<tr><td colspan="7">Нет записей под текущий фильтр.</td></tr>';
        return;
      }}

      resultsBody.innerHTML = rows.map((row, index) => {{
        return `
          <tr>
            <td>
              <span class="participant-name">${{escapeHtml(row.displayName)}}</span>
              <span class="participant-meta">${{escapeHtml(row.telegramHandle)}}</span>
              <div class="link-list">
                <a class="inline-link" href="${{row.questionnaireUrl}}" target="_blank" rel="noopener noreferrer">анкета</a>
              </div>
            </td>
            <td><span class="pill ${{row.statusKey}}">${{escapeHtml(row.statusLabel)}}</span></td>
            <td>
              <span class="action-text">${{escapeHtml(row.actionTitle)}}</span>
              <span class="action-note">${{escapeHtml(row.actionNote)}}</span>
            </td>
            <td>
              <span class="participant-name">${{escapeHtml(row.selectedCourseLabel || '—')}}</span>
              <span class="participant-meta">Путь: ${{escapeHtml(row.selectedPathLabel || '—')}}</span>
            </td>
            <td>${{truncateText(row.email, 44)}}</td>
            <td>${{escapeHtml(row.updatedAtLabel || '—')}}</td>
            <td><button class="details-btn" type="button" data-index="${{index}}">Открыть</button></td>
          </tr>
        `;
      }}).join('');
    }}

    function openDetails(index) {{
      const row = getVisibleRows()[index];
      if (!row) {{
        return;
      }}

      const summary = row.summary || {{}};
      const body = [
        sectionHtml('Идентификация', paragraph([row.displayName, row.telegramHandle].join('\\n'))),
        sectionHtml('Ссылки', paragraph([row.questionnaireUrl].filter(Boolean).join('\\n'))),
        sectionHtml('Статус', paragraph([row.statusLabel, row.actionTitle, row.actionNote].join('\\n'))),
        sectionHtml('Выбранный путь', paragraph(row.selectedPathLabel)),
        sectionHtml('Выбранный курс', paragraph(row.selectedCourseLabel)),
        sectionHtml('Vision', paragraph(summary.visionFuture)),
        sectionHtml('Personal context', paragraph(summary.personalContext)),
        sectionHtml('Purpose', paragraph(summary.purpose)),
        sectionHtml('Health restrictions', paragraph(summary.healthRestrictions)),
        sectionHtml('Nutrition flags', list(summary.nutritionFlags)),
        sectionHtml('Food habits', paragraph(summary.foodHabits)),
        sectionHtml('Medications', paragraph(summary.medications)),
        sectionHtml('Message for curator', paragraph(summary.curatorMessage))
      ].join('');

      modalTitle.textContent = row.displayName;
      modalContent.innerHTML = body;
      detailsModal.classList.add('visible');
    }}

    function syncPage() {{
      const visibleRows = getVisibleRows();
      renderRows(visibleRows);
      renderQueue(
        queueReadyOpen,
        ALL_ROWS.filter((row) => row.statusKey === 'ready-open'),
        'Сейчас нет участниц, которым нужно открыть курс.'
      );
      renderQueue(
        queueNeedsPick,
        ALL_ROWS.filter((row) => row.statusKey === 'needs-pick'),
        'Сейчас нет участниц, которым нужен ручной подбор.'
      );
      updateStats();
    }}

    resultsBody.addEventListener('click', (event) => {{
      const button = event.target.closest('[data-index]');
      if (!button) {{
        return;
      }}
      openDetails(Number(button.dataset.index));
    }});

    searchInput.addEventListener('input', syncPage);
    filterBar.addEventListener('click', (event) => {{
      const button = event.target.closest('[data-filter]');
      if (!button) {{
        return;
      }}

      activeFilter = button.dataset.filter || 'all';
      [...filterBar.querySelectorAll('[data-filter]')].forEach((item) => {{
        item.classList.toggle('is-secondary', item.dataset.filter !== activeFilter);
      }});
      syncPage();
    }});
    closeModalButton.addEventListener('click', () => detailsModal.classList.remove('visible'));
    detailsModal.addEventListener('click', (event) => {{
      if (event.target === detailsModal) {{
        detailsModal.classList.remove('visible');
      }}
    }});

    syncPage();
  </script>
</body>
</html>
"""


def main() -> None:
    template = load_template()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old_file in OUTPUT_DIR.glob("participant_*_april_2026_v1.html"):
        old_file.unlink()
    for old_file in OUTPUT_DIR.glob("q_*.html"):
        old_file.unlink()
    for stale_name in ("admin.html", "links.txt", "telegram_message.txt"):
        stale_file = OUTPUT_DIR / stale_name
        if stale_file.exists():
            stale_file.unlink()
    for old_team_page in OUTPUT_DIR.glob("team-*.html"):
        old_team_page.unlink()

    entries = []

    for participant in get_participants():
        participant_with_slug = participant
        filename = participant["filename"]
        page_html = build_participant_page(template, participant_with_slug)
        (OUTPUT_DIR / filename).write_text(page_html, encoding="utf-8")
        entries.append({**participant, "filename": filename})

    admin_snapshot_rows, snapshot_generated_at, snapshot_error = build_admin_snapshot(entries)

    (OUTPUT_DIR / "index.html").write_text(build_index_page(), encoding="utf-8")
    (OUTPUT_DIR / f"{TEAM_PAGE_TOKEN}.html").write_text(build_team_page(entries), encoding="utf-8")
    (OUTPUT_DIR / "admin.html").write_text(
        build_admin_page(admin_snapshot_rows, snapshot_generated_at, snapshot_error),
        encoding="utf-8",
    )
    print(f"Generated {len(entries)} participant questionnaires in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
