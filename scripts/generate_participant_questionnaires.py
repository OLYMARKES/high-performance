from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "participant_questionnaires_april_2026"
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


def build_questionnaire_html(name: str, slug: str) -> str:
    title = f"High Performance — анкета для {name}"

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Nunito+Sans:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --cream: #fbf7f2;
      --warm-white: rgba(255, 253, 249, 0.88);
      --terracotta: #c8744d;
      --terracotta-soft: #d88d6d;
      --charcoal: #3d3834;
      --warm-gray: #847c74;
      --line: rgba(200, 116, 77, 0.16);
      --shadow: 0 24px 70px rgba(90, 72, 56, 0.08);
      --font-display: "Cormorant Garamond", Georgia, serif;
      --font-body: "Nunito Sans", "Segoe UI", sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(216, 141, 109, 0.14), transparent 34%),
        radial-gradient(circle at bottom right, rgba(239, 229, 216, 0.72), transparent 36%),
        linear-gradient(180deg, #fcf9f5 0%, #f9f4ed 100%);
      color: var(--charcoal);
      font-family: var(--font-body);
      padding: 32px 16px 56px;
      -webkit-font-smoothing: antialiased;
    }}

    .page {{
      max-width: 980px;
      margin: 0 auto;
    }}

    .hero {{
      text-align: center;
      padding: 20px 0 34px;
    }}

    .hero-tag {{
      display: inline-flex;
      padding: 12px 24px;
      border: 1px solid rgba(200, 116, 77, 0.24);
      border-radius: 999px;
      color: var(--terracotta);
      letter-spacing: 0.24em;
      text-transform: uppercase;
      font-size: 0.86rem;
      background: rgba(255, 253, 249, 0.48);
    }}

    h1 {{
      margin-top: 28px;
      font-family: var(--font-display);
      font-size: clamp(4rem, 10vw, 6.2rem);
      font-weight: 400;
      line-height: 0.94;
      letter-spacing: -0.04em;
    }}

    h1 span {{
      display: block;
      color: var(--terracotta);
      font-style: italic;
    }}

    .hero p {{
      max-width: 760px;
      margin: 24px auto 0;
      color: var(--warm-gray);
      font-size: 1.08rem;
      line-height: 1.8;
    }}

    .section {{
      margin-top: 22px;
      padding: 28px;
      border-radius: 28px;
      background: var(--warm-white);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }}

    .section-label {{
      color: var(--terracotta);
      text-transform: uppercase;
      letter-spacing: 0.2em;
      font-size: 0.76rem;
      margin-bottom: 12px;
    }}

    .section h2 {{
      font-family: var(--font-display);
      font-size: 2.3rem;
      font-weight: 500;
      line-height: 1;
      margin-bottom: 14px;
    }}

    .section p {{
      color: var(--warm-gray);
      line-height: 1.75;
      font-size: 1rem;
    }}

    .cards {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
      margin-top: 18px;
    }}

    .card {{
      padding: 20px 18px;
      border-radius: 22px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.52);
    }}

    .card h3 {{
      font-size: 1rem;
      margin-bottom: 10px;
      color: var(--charcoal);
    }}

    .card p {{
      font-size: 0.96rem;
    }}

    .examples {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }}

    .pill {{
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid rgba(200, 116, 77, 0.18);
      color: var(--terracotta);
      font-size: 0.9rem;
      background: rgba(255, 253, 249, 0.76);
    }}

    .form-grid {{
      display: grid;
      gap: 18px;
      margin-top: 18px;
    }}

    .field {{
      display: grid;
      gap: 8px;
    }}

    .label {{
      color: var(--charcoal);
      font-size: 0.95rem;
      font-weight: 600;
    }}

    .label-note {{
      color: #a39a91;
      font-size: 0.86rem;
      line-height: 1.5;
    }}

    .select,
    .input,
    .textarea {{
      width: 100%;
      border-radius: 18px;
      border: 1px solid rgba(200, 116, 77, 0.18);
      background: rgba(255, 255, 255, 0.75);
      color: var(--charcoal);
      font: inherit;
      padding: 14px 16px;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .textarea {{
      min-height: 190px;
      resize: vertical;
      line-height: 1.7;
    }}

    .select:focus,
    .input:focus,
    .textarea:focus {{
      border-color: rgba(200, 116, 77, 0.42);
      box-shadow: 0 0 0 4px rgba(200, 116, 77, 0.08);
    }}

    .textarea::placeholder,
    .input::placeholder {{
      color: #b1a69d;
    }}

    .checkbox {{
      display: grid;
      grid-template-columns: 22px 1fr;
      gap: 12px;
      align-items: start;
      padding: 14px 16px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.52);
    }}

    .checkbox input {{
      margin-top: 3px;
    }}

    .actions {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
      margin-top: 18px;
    }}

    .button {{
      border: none;
      border-radius: 999px;
      background: linear-gradient(135deg, var(--terracotta), var(--terracotta-soft));
      color: white;
      font: inherit;
      padding: 14px 22px;
      cursor: pointer;
      box-shadow: 0 14px 36px rgba(200, 116, 77, 0.18);
    }}

    .status {{
      color: var(--warm-gray);
      font-size: 0.94rem;
      line-height: 1.5;
      min-height: 1.5em;
    }}

    .status.is-error {{
      color: #b1533d;
    }}

    .status.is-success {{
      color: #587249;
    }}

    @media (max-width: 760px) {{
      .cards {{
        grid-template-columns: 1fr;
      }}

      .section {{
        padding: 22px 18px;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="hero-tag">High Performance • анкета</div>
      <h1>{name}<span>для подбора</span></h1>
      <p>
        Привет. Следующий шаг для нас — подобрать для тебя оптимальную спортивную нагрузку,
        питание и параллельный курс Sekta, который будет поддерживать основной ритм апреля.
      </p>
    </section>

    <section class="section">
      <div class="section-label">Что будет</div>
      <h2>Основной ритм</h2>
      <p>
        У нас будет основной план: один день — главная тренировка примерно на 30 минут, на следующий —
        два комплекса на пресс, в сумме тоже около 30 минут. Это интенсивно, но выполнимо и легко встраивается в график.
      </p>
      <div class="cards">
        <article class="card">
          <h3>Основная нагрузка</h3>
          <p>
            Один день — основная тренировка около 30 минут.
            Следующий день — 2 комплекса на пресс, общей длительностью около 30 минут.
          </p>
        </article>
        <article class="card">
          <h3>Параллельный курс Sekta</h3>
          <p>
            Параллельно я предлагаю выбрать второй курс Sekta: что-то поддерживающее,
            специальное или сфокусированное под твои особенности и текущий запрос.
          </p>
        </article>
      </div>
      <div class="examples">
        <span class="pill">короткие зарядки Core</span>
        <span class="pill">Basics</span>
        <span class="pill">функциональные тренировки Superhuman</span>
        <span class="pill">или другой фокусный курс</span>
      </div>
    </section>

    <section class="section">
      <div class="section-label">Питание</div>
      <h2>Первая неделя</h2>
      <p>
        В питании я предлагаю хотя бы на первую неделю делать выбор в сторону простой еды:
        творог со сметаной, кефир, варёные яйца, мясо без жарки, варёные овощи, гречка, рис.
        Сильно сокращаем соусы, хлеб и всё, что быстро сбивает ритм. Но здесь важны твои особенности:
        если есть РПП, ограничения, сильные вкусовые предпочтения или своя специфика, обязательно расскажи.
      </p>
    </section>

    <section class="section">
      <div class="section-label">Ответ для команды</div>
      <h2>Расскажи про себя</h2>
      <p>
        Всё, что нам нужно знать, чтобы подобрать тебе классную нагрузку и питание.
        Если не хочется сильно углубляться, можешь пойти по простому пути и отметить это ниже.
      </p>

      <form id="participant-form" class="form-grid">
        <div class="field">
          <label class="label" for="load-level">Какой формат нагрузки тебе сейчас ближе?</label>
          <select class="select" id="load-level" name="loadLevel">
            <option value="">Выбрать</option>
            <option value="soft-start">Хочу мягко начать и постепенно войти</option>
            <option value="steady">Готова к нормальному стабильному темпу</option>
            <option value="intensive">Готова к интенсивному режиму</option>
            <option value="help-me-choose">Не знаю, помогите подобрать</option>
          </select>
        </div>

        <label class="checkbox">
          <input type="checkbox" id="simple-path" name="simplePath">
          <span>
            <span class="label">Хочу пойти по простому пути</span>
            <span class="label-note">Можно не углубляться в детали. Мы просто откроем базовый оптимальный вариант и начнём с него.</span>
          </span>
        </label>

        <div class="field">
          <label class="label" for="course-choice">Если уже знаешь, какой курс Sekta хочешь параллельно</label>
          <div class="label-note">Например: Basics, Superhuman, Core, или любой другой фокусный/комплексный курс.</div>
          <input class="input" id="course-choice" name="courseChoice" type="text" maxlength="240" placeholder="Напиши название курса, если уже выбрала">
        </div>

        <div class="field">
          <label class="label" for="profile-notes">Что важно знать про твою нагрузку, питание и особенности?</label>
          <div class="label-note">
            Пример ориентира: текущая форма, опыт тренировок, боли/ограничения, что сложно даётся,
            как сейчас устроено питание, есть ли РПП, сильные вкусовые привычки, что тебе помогает или мешает.
            Если не хочешь в это идти — можешь пропустить.
          </div>
          <textarea class="textarea" id="profile-notes" name="profileNotes" maxlength="4000" placeholder="Можно рассказать про тело, энергию, питание, ограничения, режим, цели, что у тебя обычно работает, а что нет."></textarea>
        </div>

        <div class="actions">
          <button class="button" type="submit">Отправить</button>
          <div class="status" id="participant-status" aria-live="polite"></div>
        </div>
      </form>
    </section>
  </main>

  <script>
    const FORM_ENDPOINT = 'https://high-performance-leads.markesbootcamp.workers.dev';
    const PARTICIPANT_NAME = {name!r};
    const PARTICIPANT_SLUG = {slug!r};
    const CONTROL_CHARS_RE = /[\\u0000-\\u0008\\u000B\\u000C\\u000E-\\u001F\\u007F]/g;
    const BIDI_CONTROL_RE = /[\\u202A-\\u202E\\u2066-\\u2069]/g;
    const LIMITS = Object.freeze({{
      courseChoice: 240,
      profileNotes: 4000
    }});

    const form = document.getElementById('participant-form');
    const statusEl = document.getElementById('participant-status');

    const sanitizeField = (value, {{ multiline = false, limit = 240 }} = {{}}) => {{
      const cleaned = String(value || '')
        .replace(/\\r\\n?/g, '\\n')
        .replace(CONTROL_CHARS_RE, '')
        .replace(BIDI_CONTROL_RE, '')
        .trim();

      const normalized = multiline
        ? cleaned
            .split('\\n')
            .map((line) => line.trimEnd())
            .join('\\n')
            .replace(/\\n{{3,}}/g, '\\n\\n')
            .trim()
        : cleaned.replace(/\\s+/g, ' ').trim();

      return normalized.slice(0, limit);
    }};

    form.addEventListener('submit', async (event) => {{
      event.preventDefault();
      statusEl.className = 'status';

      const formData = new FormData(form);
      const payload = {{
        kind: 'participant-profile',
        participantName: PARTICIPANT_NAME,
        participantSlug: PARTICIPANT_SLUG,
        loadLevel: sanitizeField(formData.get('loadLevel'), {{ limit: 80 }}),
        simplePath: formData.get('simplePath') === 'on',
        courseChoice: sanitizeField(formData.get('courseChoice'), {{ limit: LIMITS.courseChoice }}),
        profileNotes: sanitizeField(formData.get('profileNotes'), {{ multiline: true, limit: LIMITS.profileNotes }}),
        source: 'high-performance-participant-profile',
        pageUrl: window.location.href,
        submittedAt: new Date().toISOString()
      }};

      if (!payload.loadLevel && !payload.simplePath && !payload.courseChoice && !payload.profileNotes) {{
        statusEl.textContent = 'Оставь хотя бы один ориентир для подбора или отметь простой путь.';
        statusEl.classList.add('is-error');
        return;
      }}

      const submitButton = form.querySelector('button[type="submit"]');
      submitButton.disabled = true;
      submitButton.textContent = 'Отправляем...';

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

        form.reset();
        statusEl.textContent = 'Спасибо. Всё получили, вернёмся к тебе с подходящим курсом и рекомендацией.';
        statusEl.classList.add('is-success');
      }} catch (error) {{
        statusEl.textContent = 'Не удалось отправить анкету. Попробуй ещё раз чуть позже.';
        statusEl.classList.add('is-error');
      }} finally {{
        submitButton.disabled = false;
        submitButton.textContent = 'Отправить';
      }}
    }});
  </script>
</body>
</html>
"""


def build_index(entries: list[dict[str, str]]) -> str:
    cards = []
    for entry in entries:
        cards.append(
            f"""
          <a class="card" href="{entry['filename']}">
            <span class="card-name">{entry['name']}</span>
            <span class="card-meta">персональная анкета</span>
          </a>"""
        )

    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>High Performance — анкеты участниц</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Nunito+Sans:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --cream: #fbf7f2;
      --warm-white: rgba(255, 253, 249, 0.88);
      --terracotta: #c8744d;
      --charcoal: #3d3834;
      --warm-gray: #847c74;
      --line: rgba(200, 116, 77, 0.16);
      --shadow: 0 24px 70px rgba(90, 72, 56, 0.08);
      --font-display: "Cormorant Garamond", Georgia, serif;
      --font-body: "Nunito Sans", "Segoe UI", sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(216, 141, 109, 0.14), transparent 34%),
        radial-gradient(circle at bottom right, rgba(239, 229, 216, 0.72), transparent 36%),
        linear-gradient(180deg, #fcf9f5 0%, #f9f4ed 100%);
      color: var(--charcoal);
      font-family: var(--font-body);
      padding: 32px 16px 56px;
    }}

    .page {{
      max-width: 1180px;
      margin: 0 auto;
    }}

    .hero {{
      text-align: center;
      padding: 20px 0 30px;
    }}

    .hero-tag {{
      display: inline-flex;
      padding: 12px 24px;
      border: 1px solid rgba(200, 116, 77, 0.24);
      border-radius: 999px;
      color: var(--terracotta);
      letter-spacing: 0.24em;
      text-transform: uppercase;
      font-size: 0.86rem;
      background: rgba(255, 253, 249, 0.48);
    }}

    h1 {{
      margin-top: 28px;
      font-family: var(--font-display);
      font-size: clamp(4rem, 8vw, 6.2rem);
      font-weight: 400;
      line-height: 0.94;
      letter-spacing: -0.04em;
    }}

    h1 span {{
      display: block;
      color: var(--terracotta);
      font-style: italic;
    }}

    .hero p {{
      max-width: 780px;
      margin: 24px auto 0;
      color: var(--warm-gray);
      font-size: 1.05rem;
      line-height: 1.8;
    }}

    .section {{
      margin-top: 22px;
      padding: 28px;
      border-radius: 28px;
      background: var(--warm-white);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }}

    .section-label {{
      color: var(--terracotta);
      text-transform: uppercase;
      letter-spacing: 0.2em;
      font-size: 0.76rem;
      margin-bottom: 12px;
    }}

    .section h2 {{
      font-family: var(--font-display);
      font-size: 2.2rem;
      font-weight: 500;
      line-height: 1;
      margin-bottom: 12px;
    }}

    .section p {{
      color: var(--warm-gray);
      line-height: 1.75;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
      margin-top: 18px;
    }}

    .card {{
      display: block;
      text-decoration: none;
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 20px 18px;
      background: rgba(255, 255, 255, 0.54);
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .card:hover {{
      transform: translateY(-2px);
      border-color: rgba(200, 116, 77, 0.32);
    }}

    .card-name {{
      display: block;
      font-family: var(--font-display);
      font-size: 2rem;
      color: var(--charcoal);
      line-height: 1;
    }}

    .card-meta {{
      display: block;
      margin-top: 8px;
      color: var(--warm-gray);
      font-size: 0.94rem;
    }}

    .admin-grid {{
      display: grid;
      gap: 14px;
      margin-top: 18px;
    }}

    .admin-row {{
      display: grid;
      gap: 8px;
    }}

    .label {{
      color: var(--charcoal);
      font-size: 0.94rem;
      font-weight: 600;
    }}

    .note {{
      color: #a49b92;
      font-size: 0.88rem;
      line-height: 1.5;
    }}

    .input {{
      width: 100%;
      border-radius: 18px;
      border: 1px solid rgba(200, 116, 77, 0.18);
      background: rgba(255, 255, 255, 0.75);
      color: var(--charcoal);
      font: inherit;
      padding: 14px 16px;
      outline: none;
    }}

    .input:focus {{
      border-color: rgba(200, 116, 77, 0.42);
      box-shadow: 0 0 0 4px rgba(200, 116, 77, 0.08);
    }}

    .actions {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .button {{
      border: none;
      border-radius: 999px;
      background: linear-gradient(135deg, var(--terracotta), #d88d6d);
      color: white;
      font: inherit;
      padding: 13px 20px;
      cursor: pointer;
    }}

    .status {{
      color: var(--warm-gray);
      font-size: 0.94rem;
      line-height: 1.5;
      min-height: 1.5em;
    }}

    .status.is-error {{
      color: #b1533d;
    }}

    .table-wrap {{
      overflow-x: auto;
      margin-top: 18px;
      border-radius: 20px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.6);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 880px;
    }}

    th,
    td {{
      padding: 14px 16px;
      text-align: left;
      border-bottom: 1px solid rgba(200, 116, 77, 0.12);
      vertical-align: top;
      font-size: 0.95rem;
      line-height: 1.5;
    }}

    th {{
      color: var(--terracotta);
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      background: rgba(255, 253, 249, 0.84);
    }}

    td small {{
      color: var(--warm-gray);
    }}

    td a {{
      color: var(--terracotta);
    }}

    @media (max-width: 900px) {{
      .grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
    }}

    @media (max-width: 640px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}

      .section {{
        padding: 22px 18px;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="hero-tag">High Performance • анкеты участниц</div>
      <h1>High <span>Performance</span></h1>
      <p>
        Здесь собраны персональные анкеты для подбора параллельного курса Sekta
        и единая таблица ответов команды.
      </p>
    </section>

    <section class="section">
      <div class="section-label">Персональные ссылки</div>
      <h2>Анкеты участниц</h2>
      <p>Открывай нужную страницу и отправляй её конкретной участнице.</p>
      <div class="grid">
{cards_html}
      </div>
    </section>

    <section class="section">
      <div class="section-label">Командная таблица</div>
      <h2>Ответы участниц</h2>
      <p>
        Таблица читает private GitHub issues из <code>{PRIVATE_REPO}</code>.
        Чтобы увидеть ответы, вставь GitHub token с доступом <strong>Issues: Read</strong> для этого репозитория.
      </p>

      <div class="admin-grid">
        <div class="admin-row">
          <label class="label" for="gh-token">GitHub token</label>
          <div class="note">Токен хранится только в localStorage этого браузера и нужен, потому что репозиторий с ответами закрытый.</div>
          <input class="input" id="gh-token" type="password" placeholder="github_pat_...">
        </div>
        <div class="actions">
          <button class="button" id="load-table" type="button">Загрузить таблицу</button>
          <button class="button" id="clear-token" type="button">Очистить token</button>
          <div class="status" id="table-status" aria-live="polite"></div>
        </div>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Участница</th>
              <th>Дата</th>
              <th>Нагрузка</th>
              <th>Простой путь</th>
              <th>Курс</th>
              <th>Ответ</th>
              <th>Issue</th>
            </tr>
          </thead>
          <tbody id="table-body">
            <tr>
              <td colspan="7">Пока данных нет. Вставь GitHub token и нажми «Загрузить таблицу».</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>

  <script>
    const STORAGE_KEY = 'hp-participant-table-github-token';
    const REPO_ISSUES_URL = 'https://api.github.com/repos/{PRIVATE_REPO}/issues?state=all&per_page=100';
    const tableBody = document.getElementById('table-body');
    const tableStatus = document.getElementById('table-status');
    const tokenInput = document.getElementById('gh-token');
    const loadButton = document.getElementById('load-table');
    const clearButton = document.getElementById('clear-token');

    tokenInput.value = localStorage.getItem(STORAGE_KEY) || '';

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

    function escapeHtml(value) {{
      return String(value || '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;');
    }}

    function renderRows(records) {{
      if (!records.length) {{
        tableBody.innerHTML = '<tr><td colspan="7">Пока нет анкет этого типа.</td></tr>';
        return;
      }}

      tableBody.innerHTML = records.map((record) => {{
        const submittedAt = record.submittedAt ? new Date(record.submittedAt).toLocaleString('ru-RU') : '-';
        const notes = record.profileNotes
          ? escapeHtml(record.profileNotes).replaceAll('\\n', '<br>')
          : '<small>без подробностей</small>';
        const course = escapeHtml(record.courseChoice || '—');
        const loadLevel = escapeHtml(record.loadLevel || '—');
        const simplePath = record.simplePath ? 'да' : '—';
        const issueLink = record.issueUrl
          ? `<a href="${{record.issueUrl}}" target="_blank" rel="noopener noreferrer">issue</a>`
          : '—';

        return `
          <tr>
            <td>${{escapeHtml(record.participantName || '—')}}</td>
            <td>${{submittedAt}}</td>
            <td>${{loadLevel}}</td>
            <td>${{simplePath}}</td>
            <td>${{course}}</td>
            <td>${{notes}}</td>
            <td>${{issueLink}}</td>
          </tr>
        `;
      }}).join('');
    }}

    async function loadTable() {{
      const token = tokenInput.value.trim();
      if (!token) {{
        tableStatus.textContent = 'Вставь GitHub token с доступом Issues: Read.';
        tableStatus.className = 'status is-error';
        return;
      }}

      localStorage.setItem(STORAGE_KEY, token);
      tableStatus.textContent = 'Загружаем...';
      tableStatus.className = 'status';

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
        const records = issues
          .map((issue) => {{
            const record = decodeRecordFromBody(issue.body || '');
            if (!record || record.kind !== 'high-performance-participant-profile') {{
              return null;
            }}

            return {{
              ...record,
              issueUrl: issue.html_url
            }};
          }})
          .filter(Boolean)
          .sort((a, b) => (b.submittedAt || '').localeCompare(a.submittedAt || ''));

        renderRows(records);
        tableStatus.textContent = `Готово. Загружено анкет: ${{records.length}}.`;
        tableStatus.className = 'status is-success';
      }} catch (error) {{
        tableStatus.textContent = 'Не удалось загрузить таблицу. Проверь token и доступ к private repo.';
        tableStatus.className = 'status is-error';
      }}
    }}

    loadButton.addEventListener('click', loadTable);
    clearButton.addEventListener('click', () => {{
      localStorage.removeItem(STORAGE_KEY);
      tokenInput.value = '';
      tableStatus.textContent = 'Token очищен.';
      tableStatus.className = 'status';
      tableBody.innerHTML = '<tr><td colspan="7">Пока данных нет. Вставь GitHub token и нажми «Загрузить таблицу».</td></tr>';
    }});
  </script>
</body>
</html>
"""


def build_links(entries: list[dict[str, str]]) -> str:
    lines = ["High Performance participant questionnaires", ""]
    for entry in entries:
        lines.append(f"{entry['name']}: {PUBLIC_BASE_URL}/{entry['filename']}")
    return "\n".join(lines) + "\n"


def main() -> None:
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

        filename = f"participant_{slug}_april_2026_v1.html"
        html = build_questionnaire_html(participant["name"], slug)
        (OUTPUT_DIR / filename).write_text(html, encoding="utf-8")
        entries.append({"name": participant["name"], "filename": filename})

    (OUTPUT_DIR / "index.html").write_text(build_index(entries), encoding="utf-8")
    (OUTPUT_DIR / "links.txt").write_text(build_links(entries), encoding="utf-8")
    print(f"Generated {len(entries)} participant questionnaires in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
