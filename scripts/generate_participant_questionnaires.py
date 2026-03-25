from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "participant_questionnaires_april_2026"
SOURCE_TEMPLATE_PATH = Path("/Users/olymarkes/Documents/Claude/Projects/High perfomance/anketa.html")
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/participant_questionnaires_april_2026"
PRIVATE_REPO = "OLYMARKES/high-performance-leads"


PARTICIPANTS = [
    {"name": "Оля Маркес", "contact": "@manual-olya-markes", "source": "manual", "token": "q7k2m9b4v8x3"},
    {"name": "Даша Простова", "contact": "@manual-dasha-prostova", "source": "manual", "token": "n4r8t2y6p1c5"},
    {"name": "Яна Федорова", "contact": "@manual-yana-fedorova", "source": "manual", "token": "h8m3q5z7k2w9"},
    {"name": "Лера", "contact": "@lerakurepina", "issue": 26, "token": "d6v9n3k7t2m8"},
    {"name": "Аня", "contact": "@beregukukuhu", "issue": 25, "token": "a7c2r9m4x6p3"},
    {"name": "Viktoria", "contact": "@vpasko", "issue": 23, "token": "p3t8m6k1z9w4"},
    {"name": "Вера", "contact": "@verushkavera", "issue": 22, "token": "u5n2c8r4x7p1"},
    {"name": "Валерия", "contact": "@Valeriia_Tu", "issue": 21, "token": "j4m9v2k6t8q3"},
    {"name": "Olesya Dauptain", "contact": "@aramba_annecy", "issue": 20, "token": "y7p3n8k5c2m6"},
    {"name": "Надежда", "contact": "@moroznb", "issue": 18, "token": "b9t4m7q2x5k8"},
    {"name": "Наташа", "contact": "@Natasha_SHWD", "issue": 17, "token": "r6k2v9p4m8c1"},
    {"name": "Ksu Matusevich", "contact": "@ksumatu", "issue": 16, "token": "s8m3x7q1k5v9"},
    {"name": "Юля Карасик", "contact": "@karasichka", "issue": 14, "token": "e4p7t2m9c6k3"},
    {"name": "Жанар", "contact": "@zhantik87", "issue": 13, "token": "w9k5m2r8x3p6"},
    {"name": "Анна", "contact": "@Jayms17", "issue": 12, "token": "f2v8m4q7k1t5"},
    {"name": "Вика", "contact": "@vikaevdokimova", "issue": 11, "token": "g7m1p6x9c3k4"},
    {"name": "Наташа", "contact": "@nathaliedanz", "issue": 10, "token": "l5q9t3m7v2k8"},
    {"name": "Катя", "contact": "@Ekaterina_Novopashina", "issue": 8, "token": "c3k8p5m1x7t4"},
    {"name": "Екатерина Прозорова", "contact": "@katia_paints", "issue": 6, "token": "z2m7v4k9p6c1"},
]

TEAM_PAGE_TOKEN = "team-vault-7m4k9p2x6c8q"


TRANSLIT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def slugify(value: str) -> str:
    normalized = "".join(TRANSLIT.get(char, char) for char in value.lower())
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-")


def quote_js(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def load_template() -> str:
    return SOURCE_TEMPLATE_PATH.read_text(encoding="utf-8")


def add_personalization(template: str, name: str) -> str:
    html = template
    html = html.replace("<title>HIGH PERFORMANCE — Анкета</title>", f"<title>HIGH PERFORMANCE — Анкета для {name}</title>", 1)
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
  const CONTROL_CHARS_RE = /[\\u0000-\\u0008\\u000B\\u000C\\u000E-\\u001F\\u007F]/g;
  const BIDI_CONTROL_RE = /[\\u202A-\\u202E\\u2066-\\u2069]/g;

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
    const allFields = [...document.querySelectorAll('select, textarea, input')];
    return {{
      selectedPath: getSelectedPath(),
      fields: allFields.map((field) => {{
        if (field.type === 'checkbox' || field.type === 'radio') {{
          return Boolean(field.checked);
        }}
        return field.value || '';
      }})
    }};
  }}

  function restoreDraftState(state) {{
    const values = Array.isArray(state) ? state : state?.fields || [];
    const selectedPath = !Array.isArray(state) ? normalizeValue(state?.selectedPath || '') : '';
    const allFields = [...document.querySelectorAll('select, textarea, input')];
    allFields.forEach((field, index) => {{
      const saved = values[index];
      if (saved === undefined) {{
        return;
      }}

      if (field.type === 'checkbox' || field.type === 'radio') {{
        field.checked = Boolean(saved);
      }} else {{
        field.value = saved;
      }}
    }});

    syncConditionalState(selectedPath);
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

      if (result.record.draftState?.fields?.length || Array.isArray(result.record.draftState)) {{
        restoreDraftState(result.record.draftState);
      }} else {{
        applySavedRecord(result.record);
      }}
      const savedAt = formatDate(result.record.submittedAt || result.updatedAt);
      setSaveNote(savedAt ? `Открыта сохранённая версия от ${{savedAt}}.` : 'Открыта последняя сохранённая версия анкеты.');
      localStorage.setItem(LAST_SAVED_KEY, result.record.submittedAt || result.updatedAt || '');
      return true;
    }} catch (error) {{
      setSaveNote('Не удалось загрузить сохранённую версию. Можно продолжить с локальным черновиком и сохранить позже.');
      return false;
    }}
  }}

  function restoreLocalDraft() {{
    const savedDraft = localStorage.getItem(DRAFT_KEY);
    if (!savedDraft) {{
      return false;
    }}

    try {{
      restoreDraftState(JSON.parse(savedDraft));
      setSaveNote('Восстановлен локальный черновик из этого браузера.');
      return true;
    }} catch (error) {{
      localStorage.removeItem(DRAFT_KEY);
      return false;
    }}
  }}

  function buildPayload() {{
    const selectedPath = getSelectedPath();
    const selectedChildren = document.querySelector('input[name=\"children\"]:checked');
    const participantEmail = normalizeValue(document.getElementById('participant-email')?.value || '');

    const responseData = {{
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

      if (!response.ok) {{
        throw new Error('request_failed');
      }}

      const result = await response.json();
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
      setSaveNote('Не удалось сохранить анкету. Локальный черновик остался в браузере.');
      alert('Не удалось сохранить анкету. Попробуй ещё раз чуть позже.');
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
    await loadSavedVersion();
    restoreLocalDraft();
    syncConditionalState();
  }})();
</script>
"""


def build_participant_page(template: str, participant: dict[str, str]) -> str:
    slug = participant["slug"]
    html = add_personalization(template, participant["name"])
    html = html.replace("</body>\n</html>", f"{build_runtime_script(participant['name'], slug)}\n</body>\n</html>", 1)
    if participant.get("issue"):
        source_comment = (
            f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['name']} "
            f"from GitHub issue #{participant['issue']}: https://github.com/OLYMARKES/high-performance-leads/issues/{participant['issue']} -->\n"
        )
    else:
        source_comment = (
            f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['name']} "
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
            <span class="card-name">{entry['name']}</span>
            <span class="card-meta">персональная анкета</span>
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


def build_admin_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
      --radius: 14px;
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
      max-width: 1240px;
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
      max-width: 700px;
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
    .row {{
      display: grid;
      gap: 8px;
      margin-bottom: 16px;
    }}
    .label {{
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
    }}
    .note {{
      color: var(--text-muted);
      font-size: 13px;
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
    }}
    .input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }}
    .actions {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
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
    .status {{
      min-height: 1.4em;
      color: var(--text-secondary);
      font-size: 13px;
    }}
    .status.is-error {{ color: #d98274; }}
    .status.is-success {{ color: #9fc47b; }}
    .table-wrap {{
      overflow-x: auto;
      margin-top: 18px;
      border-radius: var(--radius);
      border: 1.5px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 1120px;
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
    td small {{
      color: var(--text-muted);
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
      max-width: 880px;
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
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="hero-label">High Performance</div>
      <h1>Admin <em>results</em></h1>
      <p class="hero-sub">
        Эта страница читает ответы из private GitHub repo <code>{PRIVATE_REPO}</code>.
        Для просмотра нужен GitHub token с доступом <strong>Issues: Read</strong>.
      </p>
    </div>

    <div class="panel">
      <div class="row">
        <label class="label" for="gh-token">GitHub token</label>
        <div class="note">Токен хранится только в localStorage этого браузера. Публично он никуда не вставляется, кроме запроса к GitHub API из этой страницы.</div>
        <input class="input" id="gh-token" type="password" placeholder="github_pat_...">
      </div>
      <div class="actions">
        <button class="button" id="load-results" type="button">Load results</button>
        <button class="button" id="clear-token" type="button">Clear token</button>
        <div class="status" id="load-status" aria-live="polite"></div>
      </div>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Участница</th>
              <th>Email</th>
              <th>Дата</th>
              <th>Путь</th>
              <th>Курс</th>
              <th>Вижен</th>
              <th>Персональный контекст</th>
              <th>Детали</th>
              <th>Issue</th>
            </tr>
          </thead>
          <tbody id="results-body">
            <tr><td colspan="9">Пока нет данных. Вставь token и нажми Load results.</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="modal" id="details-modal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title" id="modal-title">Ответ</div>
        <button class="close-btn" id="close-modal" type="button">закрыть</button>
      </div>
      <div id="modal-content"></div>
    </div>
  </div>

  <script>
    const STORAGE_KEY = 'hp-participant-admin-github-token-v1';
    const REPO_ISSUES_URL = 'https://api.github.com/repos/{PRIVATE_REPO}/issues?state=all&per_page=100';
    const tokenInput = document.getElementById('gh-token');
    const loadButton = document.getElementById('load-results');
    const clearButton = document.getElementById('clear-token');
    const loadStatus = document.getElementById('load-status');
    const resultsBody = document.getElementById('results-body');
    const detailsModal = document.getElementById('details-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    const closeModalButton = document.getElementById('close-modal');

    let currentRecords = [];

    tokenInput.value = localStorage.getItem(STORAGE_KEY) || '';

    function escapeHtml(value) {{
      return String(value || '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;');
    }}

    function decodeRecordFromBody(body) {{
      const match = body.match(/<!-- lead-data:v1:([^>]+) -->/);
      if (!match) {{
        return null;
      }}

      try {{
        const json = atob(match[1]);
        return JSON.parse(json);
      }} catch (error) {{
        return null;
      }}
    }}

    function truncateText(value, limit = 110) {{
      const text = String(value || '').trim();
      if (!text) {{
        return '<small>—</small>';
      }}
      return escapeHtml(text.length > limit ? `${{text.slice(0, limit)}}…` : text);
    }}

    function labelForPath(value) {{
      if (value === 'short') return 'Короткий';
      if (value === 'personal') return 'Персональный';
      return '—';
    }}

    function renderRows(records) {{
      if (!records.length) {{
        resultsBody.innerHTML = '<tr><td colspan="9">Пока нет анкет этого типа.</td></tr>';
        return;
      }}

      resultsBody.innerHTML = records.map((record, index) => {{
        const responseData = record.responseData || {{}};
        const vision = responseData.visionFuture || '';
        const context = record.personalContext || responseData.personalContext || '';
        const email = record.email || responseData.participantEmail || '';
        const submittedAt = record.submittedAt ? new Date(record.submittedAt).toLocaleString('ru-RU') : '-';

        return `
          <tr>
            <td>${{escapeHtml(record.participantName || '—')}}</td>
            <td>${{truncateText(email, 46)}}</td>
            <td>${{submittedAt}}</td>
            <td>${{escapeHtml(labelForPath(record.selectedPath || responseData.selectedPath))}}</td>
            <td>${{truncateText(record.courseChoice || responseData.courseChoice || '', 70)}}</td>
            <td>${{truncateText(vision, 90)}}</td>
            <td>${{truncateText(context, 90)}}</td>
            <td><button class="details-btn" type="button" data-index="${{index}}">Открыть</button></td>
            <td><a href="${{record.issueUrl}}" target="_blank" rel="noopener noreferrer">issue</a></td>
          </tr>
        `;
      }}).join('');
    }}

    function sectionHtml(title, body) {{
      return `
        <div class="detail-section">
          <h3>${{escapeHtml(title)}}</h3>
          ${{body}}
        </div>
      `;
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

    function openDetails(index) {{
      const record = currentRecords[index];
      if (!record) {{
        return;
      }}

      const responseData = record.responseData || {{}};
      const vip = responseData.vip || {{}};
      const body = [
        sectionHtml('Email', paragraph(record.email || responseData.participantEmail)),
        sectionHtml('Вижен недалёкого будущего', paragraph(responseData.visionFuture)),
        sectionHtml('Выбранный путь', paragraph(labelForPath(record.selectedPath || responseData.selectedPath))),
        sectionHtml('Выбранный курс', paragraph(record.courseChoice || responseData.courseChoice)),
        sectionHtml('Персональный контекст', paragraph(record.personalContext || responseData.personalContext)),
        sectionHtml('Я здесь, чтобы...', paragraph(vip.purpose)),
        sectionHtml('Возраст / Рост / Вес', paragraph([vip.age, vip.height, vip.weight].filter(Boolean).join(' / '))),
        sectionHtml('Дети / беременность', paragraph([vip.childrenStatus, vip.childrenDetail, vip.pregnantDetail].filter(Boolean).join(' / '))),
        sectionHtml('Здоровье и ограничения', paragraph(vip.healthRestrictions)),
        sectionHtml('Диастаз', paragraph(vip.diastasis)),
        sectionHtml('Актуально по тазовому дну', list(vip.pelvicFloorFlags)),
        sectionHtml('Отношение к питанию', list(vip.nutritionFlags)),
        sectionHtml('Твой обычный день', paragraph(vip.typicalDay)),
        sectionHtml('Питание и привычки', paragraph(vip.foodHabits)),
        sectionHtml('Препараты', paragraph(vip.medications)),
        sectionHtml('Сообщение для куратора', paragraph(vip.curatorMessage))
      ].join('');

      modalTitle.textContent = record.participantName || 'Ответ';
      modalContent.innerHTML = body;
      detailsModal.classList.add('visible');
    }}

    async function loadResults() {{
      const token = tokenInput.value.trim();
      if (!token) {{
        loadStatus.textContent = 'Вставь GitHub token с доступом Issues: Read.';
        loadStatus.className = 'status is-error';
        return;
      }}

      localStorage.setItem(STORAGE_KEY, token);
      loadStatus.textContent = 'Загружаем...';
      loadStatus.className = 'status';

      try {{
        const response = await fetch(REPO_ISSUES_URL, {{
          headers: {{
            Accept: 'application/vnd.github+json',
            Authorization: `Bearer ${{token}}`
          }}
        }});

        if (!response.ok) {{
          throw new Error('github_request_failed');
        }}

        const issues = await response.json();
        currentRecords = issues
          .map((issue) => {{
            const record = decodeRecordFromBody(issue.body || '');
            if (!record || record.kind !== 'high-performance-participant-questionnaire') {{
              return null;
            }}
            return {{ ...record, issueUrl: issue.html_url }};
          }})
          .filter(Boolean)
          .sort((a, b) => (b.submittedAt || '').localeCompare(a.submittedAt || ''));

        renderRows(currentRecords);
        loadStatus.textContent = `Готово. Загружено ответов: ${{currentRecords.length}}.`;
        loadStatus.className = 'status is-success';
      }} catch (error) {{
        loadStatus.textContent = 'Не удалось загрузить результаты. Проверь token и доступ к private repo.';
        loadStatus.className = 'status is-error';
      }}
    }}

    resultsBody.addEventListener('click', (event) => {{
      const button = event.target.closest('[data-index]');
      if (!button) {{
        return;
      }}

      openDetails(Number(button.dataset.index));
    }});

    closeModalButton.addEventListener('click', () => detailsModal.classList.remove('visible'));
    detailsModal.addEventListener('click', (event) => {{
      if (event.target === detailsModal) {{
        detailsModal.classList.remove('visible');
      }}
    }});
    loadButton.addEventListener('click', loadResults);
    clearButton.addEventListener('click', () => {{
      localStorage.removeItem(STORAGE_KEY);
      tokenInput.value = '';
      currentRecords = [];
      resultsBody.innerHTML = '<tr><td colspan="8">Пока нет данных. Вставь token и нажми Load results.</td></tr>';
      loadStatus.textContent = 'Token очищен.';
      loadStatus.className = 'status';
    }});
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
    used_slugs = set()

    for participant in PARTICIPANTS:
        base_slug = slugify(participant["name"])
        contact_slug = slugify(participant["contact"].replace("@", ""))
        slug = base_slug if base_slug not in used_slugs else f"{base_slug}-{contact_slug}"
        used_slugs.add(slug)

        participant_with_slug = {**participant, "slug": slug}
        filename = f"q_{participant['token']}.html"
        page_html = build_participant_page(template, participant_with_slug)
        (OUTPUT_DIR / filename).write_text(page_html, encoding="utf-8")
        entries.append({"name": participant["name"], "filename": filename})

    (OUTPUT_DIR / "index.html").write_text(build_index_page(), encoding="utf-8")
    (OUTPUT_DIR / f"{TEAM_PAGE_TOKEN}.html").write_text(build_team_page(entries), encoding="utf-8")
    print(f"Generated {len(entries)} participant questionnaires in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
