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
    {"name": "Аня", "contact": "@beregukukuhu", "issue": 25},
    {"name": "Viktoria", "contact": "@vpasko", "issue": 23},
    {"name": "Вера", "contact": "@verushkavera", "issue": 22},
    {"name": "Валерия", "contact": "@Valeriia_Tu", "issue": 21},
    {"name": "Olesya Dauptain", "contact": "@aramba_annecy", "issue": 20},
    {"name": "Надежда", "contact": "@moroznb", "issue": 18},
    {"name": "Наташа", "contact": "@Natasha_SHWD", "issue": 17},
    {"name": "Ksu Matusevich", "contact": "@ksumatu", "issue": 16},
    {"name": "Саша", "contact": "@s_dorodenko", "issue": 15},
    {"name": "Юля Карасик", "contact": "@karasichka", "issue": 14},
    {"name": "Жанар", "contact": "@zhantik87", "issue": 13},
    {"name": "Анна", "contact": "@Jayms17", "issue": 12},
    {"name": "Вика", "contact": "@vikaevdokimova", "issue": 11},
    {"name": "Наташа", "contact": "@nathaliedanz", "issue": 10},
    {"name": "Катя", "contact": "@Ekaterina_Novopashina", "issue": 8},
    {"name": "Екатерина Прозорова", "contact": "@katia_paints", "issue": 6},
]


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
    html = html.replace("<div class=\"hero-greeting\">Привет, <em>{Имя}</em></div>", f"<div class=\"hero-greeting\">Привет, <em>{name}</em></div>", 1)
    html = html.replace(
        '<p class="hero-sub">Я очень рада, что ты с нами. Поехали :)</p>',
        '<p class="hero-sub">Я очень рада, что ты с нами. Здесь можно спокойно заполнить всё в своём ритме — черновик сохранится автоматически.</p>',
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
        '<div class="success-overlay" id="success">\n  <h2>Готово</h2>\n  <p id="success-message">Я всё получила и скоро вернусь с рекомендациями.</p>\n</div>',
        1,
    )
    return html


def build_runtime_script(name: str, slug: str) -> str:
    return f"""
<script>
  const FORM_ENDPOINT = 'https://high-performance-leads.markesbootcamp.workers.dev';
  const PARTICIPANT_NAME = {quote_js(name)};
  const PARTICIPANT_SLUG = {quote_js(slug)};
  const DRAFT_KEY = `hp-participant-questionnaire-${{PARTICIPANT_SLUG}}-v1`;
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

  function collectDraftState() {{
    const allFields = [...document.querySelectorAll('select, textarea, input')];
    return allFields.map((field) => {{
      if (field.type === 'checkbox' || field.type === 'radio') {{
        return Boolean(field.checked);
      }}
      return field.value || '';
    }});
  }}

  function restoreDraftState(values) {{
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

    if (document.getElementById('path1-fields').querySelector('select').value) {{
      document.getElementById('path1').classList.add('active');
      document.getElementById('path1-fields').classList.add('visible');
    }}

    if (normalizeValue(document.getElementById('personal-context').value, true)) {{
      document.getElementById('path2').classList.add('active');
      document.getElementById('path2-fields').classList.add('visible');
    }}

    const selectedChildren = document.querySelector('input[name=\"children\"]:checked');
    if (selectedChildren) {{
      document.getElementById('children-detail').style.display = selectedChildren.value === 'yes' ? 'block' : 'none';
      document.getElementById('pregnant-detail').style.display = selectedChildren.value === 'pregnant' ? 'block' : 'none';
    }}
  }}

  function saveDraft() {{
    localStorage.setItem(DRAFT_KEY, JSON.stringify(collectDraftState()));
  }}

  function buildPayload() {{
    const path1Active = document.getElementById('path1').classList.contains('active');
    const path2Active = document.getElementById('path2').classList.contains('active');
    const selectedChildren = document.querySelector('input[name=\"children\"]:checked');

    const responseData = {{
      visionFuture: normalizeValue(document.getElementById('vision-future')?.value || '', true),
      selectedPath: path1Active ? 'short' : path2Active ? 'personal' : '',
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
    const submitButton = document.querySelector('.submit-btn');

    if (!hasMeaningfulValue(payload.responseData)) {{
      alert('Заполни хотя бы один блок анкеты, чтобы мы могли что-то подобрать.');
      return;
    }}

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

      localStorage.setItem(`${{DRAFT_KEY}}:last-submitted`, JSON.stringify(payload));
      localStorage.removeItem(DRAFT_KEY);
      successMessage.textContent = 'Я всё получила и скоро вернусь с рекомендациями.';
      successOverlay.classList.add('visible');
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }} catch (error) {{
      alert('Не удалось отправить анкету. Попробуй ещё раз чуть позже.');
    }} finally {{
      submitButton.disabled = false;
      submitButton.style.opacity = '1';
    }}
  }}

  const savedDraft = localStorage.getItem(DRAFT_KEY);
  if (savedDraft) {{
    try {{
      restoreDraftState(JSON.parse(savedDraft));
    }} catch (error) {{
      localStorage.removeItem(DRAFT_KEY);
    }}
  }}

  document.querySelectorAll('select, textarea, input').forEach((field) => {{
    field.addEventListener('input', saveDraft);
    field.addEventListener('change', saveDraft);
  }});
</script>
"""


def build_participant_page(template: str, participant: dict[str, str]) -> str:
    slug = participant["slug"]
    html = add_personalization(template, participant["name"])
    html = html.replace("</body>\n</html>", f"{build_runtime_script(participant['name'], slug)}\n</body>\n</html>", 1)
    source_comment = (
        f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['name']} "
        f"from GitHub issue #{participant['issue']}: https://github.com/OLYMARKES/high-performance-leads/issues/{participant['issue']} -->\n"
    )
    return source_comment + html


def build_index_page(entries: list[dict[str, str]]) -> str:
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
  <title>HIGH PERFORMANCE — Анкеты участниц</title>
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
    .admin-note {{
      margin-top: 24px;
      color: #6e6e6e;
      font-size: 13px;
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
      <h1>Персональные <em>анкеты</em></h1>
      <p class="hero-sub">Отсюда можно открыть личную страницу каждой участницы. Админка с результатами вынесена отдельно.</p>
    </div>

    <div class="panel">
      <div class="grid">
{cards_html}
      </div>
      <div class="admin-note">Отдельная админка не привязана к этому публичному индексу и должна открываться только командой.</div>
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
            <tr><td colspan="8">Пока нет данных. Вставь token и нажми Load results.</td></tr>
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
        resultsBody.innerHTML = '<tr><td colspan="8">Пока нет анкет этого типа.</td></tr>';
        return;
      }}

      resultsBody.innerHTML = records.map((record, index) => {{
        const responseData = record.responseData || {{}};
        const vision = responseData.visionFuture || '';
        const context = record.personalContext || responseData.personalContext || '';
        const submittedAt = record.submittedAt ? new Date(record.submittedAt).toLocaleString('ru-RU') : '-';

        return `
          <tr>
            <td>${{escapeHtml(record.participantName || '—')}}</td>
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


def build_links_text(entries: list[dict[str, str]]) -> str:
    lines = ["High Performance participant questionnaires", ""]
    for entry in entries:
        lines.append(f"{entry['name']}: {PUBLIC_BASE_URL}/{entry['filename']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    template = load_template()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old_file in OUTPUT_DIR.glob("participant_*_april_2026_v1.html"):
        old_file.unlink()

    entries = []
    used_slugs = set()

    for participant in PARTICIPANTS:
        base_slug = slugify(participant["name"])
        contact_slug = slugify(participant["contact"].replace("@", ""))
        slug = base_slug if base_slug not in used_slugs else f"{base_slug}-{contact_slug}"
        used_slugs.add(slug)

        participant_with_slug = {**participant, "slug": slug}
        filename = f"participant_{slug}_april_2026_v1.html"
        page_html = build_participant_page(template, participant_with_slug)
        (OUTPUT_DIR / filename).write_text(page_html, encoding="utf-8")
        entries.append({"name": participant["name"], "filename": filename})

    (OUTPUT_DIR / "index.html").write_text(build_index_page(entries), encoding="utf-8")
    (OUTPUT_DIR / "admin.html").write_text(build_admin_page(), encoding="utf-8")
    (OUTPUT_DIR / "links.txt").write_text(build_links_text(entries), encoding="utf-8")
    print(f"Generated {len(entries)} participant questionnaires in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
