from __future__ import annotations

import json
from pathlib import Path

from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "week_1_trackers_april_2026"
SOURCE_TEMPLATE_PATH = Path("/Users/olymarkes/Documents/Claude/Projects/High perfomance/week-1-tracker.html")
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/week_1_trackers_april_2026"
TEAM_PAGE_TOKEN = "week1-vault-t8m4q2c7k9p5"
TRACKER_VERSION_QUERY = "v=materials-pdf-v9"
HABITS_PDF = "../habit-sheet.pdf?v=materials-pdf-v9"
NUTRITION_PDF = "../nutrition-guide.pdf?v=materials-pdf-v9"
SEKTA_CABINET_URL = "https://sektaschool.ru"
MAIN_PROGRAM_PDF = "../main-program.pdf?v=materials-pdf-v9"
MAIN_PROGRAM_PDF_OPEN = "../main-program.pdf?v=materials-pdf-v9#page=999"
CHAT_URL = "https://t.me/+UQzb3a_ohdliMTEy"
LOOM_URL = "https://www.loom.com/share/7c09b8ca1c0f44708bcda671c35a15d3"
DAY_WORKOUT_LINKS = [
    [
        {
            "label": "Тренировка дня",
            "url": "https://kinescope.io/et2qFrFvqZ5oohxazHhCHn",
        }
    ]
]


def quote_js(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def add_personalization(template: str, name: str, for_name: str, slug: str) -> str:
    html = template
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots" content="noindex, nofollow, noarchive">',
        1,
    )
    html = html.replace("<title>Трекер недели 1 — High Performance</title>", f"<title>Трекер недели 1 — {name}</title>", 1)
    html = html.replace(
        '<div class="hero-tag">High Performance · Трекер · Апрель 2026</div>',
        f'<div class="hero-tag">High Performance · {name} · Неделя 1</div>',
        1,
    )
    html = html.replace(
        '<p class="hero-sub">Твой ежедневный трекер привычек. Отмечай, наблюдай, двигайся вперёд.</p>',
        f'<p class="hero-sub">Персональный трекер первой недели для {for_name}. Здесь один экран с манифестом и трекером дня, который можно сохранять и дополнять по этой же ссылке.</p>',
        1,
    )
    html = html.replace(
        "Оля Маркес · High Performance · Трекер недели 1 · Апрель 2026",
        f"{name} · High Performance · Трекер недели 1 · Апрель 2026",
        1,
    )
    html = html.replace("'hp_week1_tracker'", f"'hp_week1_tracker_{slug}'", 2)
    html = html.replace(
        "/* ── Footer ── */",
        """/* ── Materials block ── */
.materials-shell {
  background: linear-gradient(180deg, rgba(255, 253, 249, 0.98) 0%, rgba(250, 244, 238, 0.92) 100%);
  border: 1px solid var(--sand);
  border-radius: 24px;
  padding: 34px 32px 24px;
  margin-bottom: 28px;
  box-shadow: 0 18px 44px rgba(58, 54, 50, 0.06);
  position: relative;
  z-index: 4;
}
.materials-topline {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 18px;
}
.materials-title {
  font-family: var(--font-display);
  font-size: clamp(32px, 4vw, 42px);
  font-weight: 500;
  line-height: 1.05;
}
.materials-title em {
  color: var(--terracotta);
  font-style: italic;
}
.materials-note {
  max-width: 250px;
  padding: 10px 14px;
  border-radius: 16px;
  background: rgba(196, 112, 75, 0.08);
  color: var(--terracotta);
  font-size: 13px;
  line-height: 1.45;
}
.materials-toggle {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 11px 14px;
  border-radius: 14px;
  border: 1px solid rgba(226, 213, 195, 0.9);
  background: rgba(255, 255, 255, 0.72);
  color: var(--charcoal);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.3px;
  cursor: pointer;
}
.materials-toggle svg {
  transition: transform 0.25s ease;
}
.materials-shell.is-collapsed .materials-toggle svg {
  transform: rotate(-180deg);
}
.materials-intro {
  max-width: 640px;
  color: var(--warm-gray);
  margin-bottom: 24px;
}
.materials-collapsed-note {
  display: none;
  margin-top: 8px;
  color: var(--warm-gray);
  font-size: 14px;
}
.materials-shell.is-collapsed .materials-collapsed-note {
  display: block;
}
.materials-content {
  display: block;
  position: relative;
  z-index: 5;
}
.materials-shell.is-collapsed .materials-content {
  display: none;
}
.materials-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}
.material-card {
  background: rgba(255, 255, 255, 0.65);
  border: 1px solid rgba(226, 213, 195, 0.9);
  border-radius: 20px;
  padding: 22px 20px 20px;
  min-height: 100%;
  position: relative;
  z-index: 6;
}
.material-kicker {
  color: var(--terracotta);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 10px;
  font-weight: 700;
  margin-bottom: 10px;
}
.material-card h3 {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 500;
  line-height: 1.05;
  margin-bottom: 10px;
}
.material-card p {
  color: var(--warm-gray);
  font-size: 15px;
  line-height: 1.65;
}
.material-actions {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
  z-index: 7;
}
.material-resource-list {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.material-resource {
  padding: 14px;
  border-radius: 16px;
  border: 1px solid rgba(226, 213, 195, 0.9);
  background: rgba(255, 253, 249, 0.84);
}
.material-resource-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
}
.material-resource-title {
  color: var(--charcoal);
  font-size: 16px;
  font-weight: 700;
}
.material-resource-type {
  color: var(--light-gray);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.material-resource p {
  margin-top: 8px;
  font-size: 14px;
  line-height: 1.6;
}
.material-link-row {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  position: relative;
  z-index: 7;
}
.material-link-row .material-btn {
  width: auto;
  min-width: 0;
  flex: 1 1 180px;
}
.material-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 48px;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid var(--charcoal);
  background: var(--charcoal);
  color: var(--warm-white);
  text-decoration: none;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  position: relative;
  z-index: 8;
  pointer-events: auto;
}
.material-btn.secondary {
  background: transparent;
  color: var(--charcoal);
  border-color: rgba(122, 116, 109, 0.22);
}
.summary-snippet {
  display: none;
  margin-top: 14px;
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 253, 249, 0.9);
  border: 1px solid rgba(226, 213, 195, 0.8);
}
.summary-snippet.is-open {
  display: block;
}
.summary-snippet-title {
  margin-bottom: 10px;
  color: var(--charcoal);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.summary-snippet p + p {
  margin-top: 10px;
}
.material-meta {
  margin-top: 16px;
  color: var(--light-gray);
  font-size: 13px;
  line-height: 1.55;
}
.duplication-note {
  margin-top: 18px;
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(122, 139, 111, 0.08);
  color: var(--warm-gray);
  font-size: 14px;
  line-height: 1.65;
}

/* ── Single-day view ── */
.day-nav {
  display: none;
}

/* ── Save panel ── */
.save-panel {
  margin-top: 40px;
  margin-bottom: 12px;
}
.save-panel-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 22px 24px;
  border: 1px solid var(--sand);
  border-radius: 20px;
  background: var(--warm-white);
}
.save-panel-copy {
  min-width: 0;
}
.save-panel-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 500;
  color: var(--charcoal);
}
.save-panel-status {
  margin-top: 4px;
  font-size: 14px;
  color: var(--warm-gray);
  line-height: 1.6;
}
.save-progress-btn {
  width: auto;
  min-width: 230px;
  margin-top: 0;
  flex-shrink: 0;
}

.day-workouts-card {
  margin-top: 18px;
  padding: 18px 18px 16px;
  border-radius: 18px;
  border: 1px solid rgba(226, 213, 195, 0.95);
  background: rgba(255, 253, 249, 0.9);
}
.day-workouts-kicker {
  color: var(--terracotta);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 11px;
  font-weight: 700;
}
.day-workouts-title {
  margin-top: 8px;
  font-family: var(--font-display);
  font-size: 24px;
  line-height: 1.05;
  color: var(--charcoal);
}
.day-workouts-copy {
  margin-top: 8px;
  color: var(--warm-gray);
  font-size: 14px;
  line-height: 1.6;
}
.day-workouts-links {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.day-workout-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 11px 14px;
  border-radius: 14px;
  border: 1px solid var(--charcoal);
  background: var(--charcoal);
  color: var(--warm-white);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.02em;
  flex: 1 1 180px;
}

/* ── Footer ── */""",
        1,
    )
    html = html.replace(
        "@media (max-width: 600px) {\n  .hero { min-height: 36vh; }",
        """@media (max-width: 600px) {
  .materials-shell {
    padding: 24px 20px 18px;
  }
  .materials-topline {
    flex-direction: column;
    align-items: stretch;
  }
  .materials-note {
    max-width: none;
  }
  .materials-grid {
    grid-template-columns: 1fr;
  }
  .save-panel-inner {
    flex-direction: column;
    align-items: stretch;
  }
  .save-progress-btn {
    width: 100%;
    min-width: 0;
  }
  .hero { min-height: 36vh; }""",
        1,
    )
    html = html.replace(
        """    <!-- Day sections will be generated by JS -->
    <div id="daysContainer"></div>

  </div>
</section>""",
        """    <!-- Day sections will be generated by JS -->
    <section class="materials-shell reveal" id="materialsShell">
      <div class="materials-topline">
        <div>
          <h2 class="materials-title">Материалы <em>внутри трекера</em></h2>
        </div>
        <div style="display:flex; flex-direction:column; align-items:flex-end; gap:10px;">
          <div class="materials-note">Здесь лежат общие материалы программы: рекомендации и тренировочный план. Их не нужно искать в чате.</div>
          <button class="materials-toggle" id="materialsToggle" type="button" aria-expanded="true" aria-controls="materialsContent">
            <span id="materialsToggleText">Свернуть материалы</span>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="4 10 8 6 12 10"></polyline>
            </svg>
          </button>
        </div>
      </div>
      <div class="materials-collapsed-note" id="materialsCollapsedNote">Материалы недели скрыты. Нажми «Развернуть материалы», чтобы снова увидеть рекомендации и план тренировок.</div>

      <div class="materials-content" id="materialsContent">
        <p class="materials-intro">Это общий слой материалов для всей группы. Персональная часть остаётся ниже: манифест, трекер дня и сохранение прогресса по этой же ссылке.</p>

        <div class="materials-grid">
          <article class="material-card">
            <div class="material-kicker">Рекомендации</div>
            <h3>Привычки и питание</h3>
            <p>Здесь лежат два базовых PDF, чтобы участнице не приходилось искать материалы по переписке: отдельный лист привычек и отдельный документ по питанию.</p>
            <div class="material-resource-list">
              <div class="material-resource">
                <div class="material-resource-head">
                  <div class="material-resource-title">Лист привычек</div>
                  <div class="material-resource-type">PDF</div>
                </div>
                <p>Опорный лист на неделю: на что смотреть каждый день, как не распыляться и как держать повторяемость без идеальности.</p>
                <div class="material-link-row">
                  <a class="material-btn" href="{HABITS_PDF}" target="_blank" rel="noopener noreferrer">Открыть PDF</a>
                  <a class="material-btn secondary" href="{HABITS_PDF}" download="habit-sheet.pdf">Скачать на компьютер</a>
                </div>
              </div>
              <div class="material-resource">
                <div class="material-resource-head">
                  <div class="material-resource-title">Питание</div>
                  <div class="material-resource-type">PDF</div>
                </div>
                <p>Краткая логика питания внутри программы: как собирать приёмы пищи, заранее упростить выбор и снизить хаос вокруг еды.</p>
                <div class="material-link-row">
                  <a class="material-btn" href="{NUTRITION_PDF}" target="_blank" rel="noopener noreferrer">Открыть PDF</a>
                  <a class="material-btn secondary" href="{NUTRITION_PDF}" download="nutrition-guide.pdf">Скачать на компьютер</a>
                </div>
              </div>
            </div>
            <div class="material-actions">
              <button class="material-btn secondary" id="summaryToggle" type="button" aria-expanded="false" aria-controls="nutritionSummary">Открыть краткое содержание</button>
            </div>
            <div class="summary-snippet" id="nutritionSummary">
              <div class="summary-snippet-title">Коротко, что внутри</div>
              <p><strong>Лист привычек:</strong> базовые опоры на день, минимум действий, повторяемость и фокус не на идеальности, а на устойчивом ритме.</p>
              <p><strong>Питание:</strong> простая логика тарелки, регулярность, понятные закупки и решения, которые снижают импульсивные перекусы и хаос вокруг еды.</p>
              <p><strong>Смысл первой недели:</strong> не усложнять себе жизнь, а собрать рабочую базу из сна, еды, движения и внимания к своему состоянию.</p>
            </div>
            <div class="material-meta">Материалы общие для всей группы и лежат прямо в трекере, чтобы не зависеть от закрепов и пересланных файлов.</div>
          </article>

          <article class="material-card">
            <div class="material-kicker">Практика</div>
            <h3>Тренировки</h3>
            <p>Здесь лежит основная программа в PDF. Если удобнее, ниже оставляю и бэкап-вариант: личный кабинет на SektaSchool.ru.</p>
            <div class="material-actions">
              <a class="material-btn" href="{MAIN_PROGRAM_PDF_OPEN}" target="_blank" rel="noopener noreferrer">Открыть PDF</a>
              <a class="material-btn secondary" href="{MAIN_PROGRAM_PDF}" download="main-program.pdf">Скачать на компьютер</a>
              <a class="material-btn secondary" href="{SEKTA_CABINET_URL}" target="_blank" rel="noopener noreferrer">Бэкап-программа на SektaSchool.ru</a>
            </div>
            <div class="material-meta">Сначала даю основной файл, а личный кабинет оставляю как запасной вариант доступа.</div>
          </article>
        </div>

        <div class="duplication-note">
          <strong>Логика доступа:</strong> ссылка на трекер индивидуальная, а материалы общие. Поэтому правильнее держать материалы внутри трекера, а в чате при желании только дублировать PDF.
        </div>
      </div>
    </section>

    <div id="daysContainer"></div>

    <div class="save-panel reveal" id="savePanel">
      <div class="save-panel-inner">
        <div class="save-panel-copy">
          <div class="save-panel-title">Сохраняй прогресс</div>
          <div class="save-panel-status" id="saveStatus">По этой ссылке всегда будет открываться актуальная сохранённая версия трекера.</div>
        </div>
        <button class="manifesto-btn save-progress-btn" id="saveTrackerBtn" type="button">Сохранить трекер</button>
      </div>
    </div>

  </div>
</section>""",
        1,
    )
    html = html.replace(
        "const DAY_NAMES = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];",
        "const DAY_NAMES = ['День 1'];",
        1,
    )
    html = html.replace(
        '<h1>Неделя <em>1</em></h1>',
        '<h1>Неделя <em>1</em> · День <em>1</em></h1>',
        1,
    )
    html = html.replace(
        '<div class="day-date">День ${currentDay + 1} из 7</div>',
        '<div class="day-date">День ${currentDay + 1}</div>',
        1,
    )
    html = html.replace(
        """function renderDay() {
  const day = state.days[currentDay];
  const total = day.items.length;
  const done = day.items.filter(it => it.checked).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  daysContainer.innerHTML = `
    <div class="day-section active">
      <div class="day-header">
        <h2>${day.name}</h2>
        <div class="day-date">День ${currentDay + 1}</div>
        <div class="day-progress">
          <div class="day-progress-bar">
            <div class="day-progress-bar-fill" style="width:${pct}%"></div>
          </div>
          <div class="day-progress-text">${pct}%</div>
        </div>
      </div>
      <div class="tracker-list" id="trackerList"></div>
      <button class="add-item-btn" onclick="openAddItem()">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="2"><line x1="9" y1="3" x2="9" y2="15"/><line x1="3" y1="9" x2="15" y2="9"/></svg>
        Добавить пункт
      </button>
    </div>
  `;
""",
        """function renderDay() {
  const day = state.days[currentDay];
  const total = day.items.length;
  const done = day.items.filter(it => it.checked).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const workoutLinks = Array.isArray(window.DAY_WORKOUT_LINKS?.[currentDay]) ? window.DAY_WORKOUT_LINKS[currentDay] : [];
  const workoutLinksHtml = workoutLinks.length
    ? `
      <div class="day-workouts-card">
        <div class="day-workouts-kicker">Практика дня</div>
        <div class="day-workouts-title">Тренировки</div>
        <div class="day-workouts-copy">${workoutLinks.length > 1 ? 'Здесь собраны прямые ссылки на сегодняшние тренировки, чтобы не искать их внутри PDF.' : 'Здесь лежит прямая ссылка на сегодняшнюю тренировку, чтобы можно было открыть её сразу из трекера.'}</div>
        <div class="day-workouts-links">
          ${workoutLinks.map((link) => `<a class="day-workout-link" href="${link.url}" target="_blank" rel="noopener noreferrer">${link.label}</a>`).join('')}
        </div>
      </div>
    `
    : '';

  daysContainer.innerHTML = `
    <div class="day-section active">
      <div class="day-header">
        <h2>${day.name}</h2>
        <div class="day-date">День ${currentDay + 1}</div>
        <div class="day-progress">
          <div class="day-progress-bar">
            <div class="day-progress-bar-fill" style="width:${pct}%"></div>
          </div>
          <div class="day-progress-text">${pct}%</div>
        </div>
      </div>
      ${workoutLinksHtml}
      <div class="tracker-list" id="trackerList"></div>
      <button class="add-item-btn" onclick="openAddItem()">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="2"><line x1="9" y1="3" x2="9" y2="15"/><line x1="3" y1="9" x2="15" y2="9"/></svg>
        Добавить пункт
      </button>
    </div>
  `;
""",
        1,
    )
    html = html.replace(
        """// Show overlay on load if no manifesto yet
if (!state.manifesto) {
  setTimeout(() => overlay.classList.add('active'), 600);
} else {
  renderManifestoBanner();
}""",
        """function syncManifestoVisibility() {
  if (!state.manifesto) {
    setTimeout(() => {
      if (!state.manifesto) overlay.classList.add('active');
    }, 600);
  } else {
    renderManifestoBanner();
    overlay.classList.remove('active');
  }
}

syncManifestoVisibility();""",
        1,
    )
    html = html.replace("{HABITS_PDF}", HABITS_PDF)
    html = html.replace("{NUTRITION_PDF}", NUTRITION_PDF)
    html = html.replace("{SEKTA_CABINET_URL}", SEKTA_CABINET_URL)
    html = html.replace("{MAIN_PROGRAM_PDF}", MAIN_PROGRAM_PDF)
    html = html.replace("{MAIN_PROGRAM_PDF_OPEN}", MAIN_PROGRAM_PDF_OPEN)
    return html


def build_runtime_script(name: str, slug: str) -> str:
    return f"""
<script>
  const FORM_ENDPOINT = 'https://high-performance-leads.markesbootcamp.workers.dev';
  const LOAD_ENDPOINT = `${{FORM_ENDPOINT}}/participant-week-tracker?slug=${{encodeURIComponent({quote_js(slug)})}}&weekKey=week-1`;
  const PARTICIPANT_NAME = {quote_js(name)};
  const PARTICIPANT_SLUG = {quote_js(slug)};
  const WEEK_KEY = 'week-1';
  const LOCAL_KEY = `hp_week1_tracker_${{PARTICIPANT_SLUG}}`;
  window.DAY_WORKOUT_LINKS = {quote_js(DAY_WORKOUT_LINKS)};

  function getDefaultDayItems() {{
    return DEFAULT_ITEMS.map((item, index) => ({{
      ...item,
      id: item.id + '_' + index,
      checked: false,
      inputValue: ''
    }}));
  }}

  function normalizeTrackerState(rawState) {{
    const baseDay = {{
      name: 'День 1',
      items: getDefaultDayItems()
    }};

    if (!rawState || typeof rawState !== 'object') {{
      return {{
        manifesto: '',
        days: [baseDay]
      }};
    }}

    const firstDay = Array.isArray(rawState.days) && rawState.days.length > 0 && rawState.days[0] && typeof rawState.days[0] === 'object'
      ? rawState.days[0]
      : null;

    const normalizedItems = Array.isArray(firstDay?.items)
      ? firstDay.items.map((item, index) => ({{
          ...item,
          id: item?.id || `item_${{index}}`,
          checked: Boolean(item?.checked),
          inputValue: typeof item?.inputValue === 'string' ? item.inputValue : ''
        }}))
      : baseDay.items;

    return {{
      ...rawState,
      manifesto: typeof rawState.manifesto === 'string' ? rawState.manifesto : '',
      days: [{{
        ...baseDay,
        ...firstDay,
        name: 'День 1',
        items: normalizedItems
      }}]
    }};
  }}

  function setSaveStatus(message) {{
    const status = document.getElementById('saveStatus');
    if (status) {{
      status.textContent = message;
    }}
  }}

  function cloneState(value) {{
    return JSON.parse(JSON.stringify(value));
  }}

  function saveState() {{
    try {{
      localStorage.setItem(LOCAL_KEY, JSON.stringify(state));
      setSaveStatus('Есть локальные изменения в этом браузере. Нажми «Сохранить трекер», чтобы обновить серверную версию.');
    }} catch (error) {{
      setSaveStatus('Не удалось сохранить локальный черновик в браузере.');
    }}
  }}

  function restoreLocalState() {{
    try {{
      const saved = localStorage.getItem(LOCAL_KEY);
      if (!saved) {{
        return false;
      }}
      state = normalizeTrackerState(JSON.parse(saved));
      currentDay = 0;
      renderManifestoBanner();
      renderDayNav();
      renderDay();
      syncManifestoVisibility();
      setSaveStatus('Восстановлен локальный черновик из этого браузера.');
      return true;
    }} catch (error) {{
      localStorage.removeItem(LOCAL_KEY);
      return false;
    }}
  }}

  async function loadSavedTracker() {{
    setSaveStatus('Загружаю сохранённую версию трекера...');
    try {{
      const response = await fetch(LOAD_ENDPOINT);
      if (!response.ok) {{
        throw new Error('load_failed');
      }}

      const result = await response.json();
      if (!result.ok || !result.found || !result.record?.trackerState) {{
        setSaveStatus('Пока нет сохранённой версии. Можно заполнить трекер и сохранить его по этой же ссылке.');
        return false;
      }}

      state = normalizeTrackerState(result.record.trackerState);
      currentDay = 0;
      localStorage.setItem(LOCAL_KEY, JSON.stringify(state));
      renderManifestoBanner();
      renderDayNav();
      renderDay();
      syncManifestoVisibility();

      const savedAt = result.record.submittedAt || result.updatedAt || '';
      const savedText = savedAt ? new Date(savedAt).toLocaleString('ru-RU') : '';
      setSaveStatus(savedText ? `Открыта сохранённая версия от ${{savedText}}.` : 'Открыта последняя сохранённая версия трекера.');
      return true;
    }} catch (error) {{
      setSaveStatus('Не удалось загрузить сохранённую версию. Можно продолжить с локальным черновиком.');
      return false;
    }}
  }}

  async function saveTrackerToServer() {{
    const button = document.getElementById('saveTrackerBtn');
    if (!button) {{
      return;
    }}

    const payload = {{
      kind: 'participant-week-tracker',
      participantName: PARTICIPANT_NAME,
      participantSlug: PARTICIPANT_SLUG,
      weekKey: WEEK_KEY,
      trackerState: cloneState(state),
      pageUrl: window.location.href,
      source: 'high-performance-week-1-tracker',
      submittedAt: new Date().toISOString()
    }};

    button.disabled = true;
    button.style.opacity = '0.7';
    setSaveStatus('Сохраняю трекер...');

    try {{
      const response = await fetch(FORM_ENDPOINT, {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json'
        }},
        body: JSON.stringify(payload)
      }});

      if (!response.ok) {{
        throw new Error('save_failed');
      }}

      localStorage.setItem(LOCAL_KEY, JSON.stringify(state));
      const savedText = new Date(payload.submittedAt).toLocaleString('ru-RU');
      setSaveStatus(`Сохранено ${{savedText}}. По этой ссылке всегда откроется актуальная версия трекера.`);
    }} catch (error) {{
      setSaveStatus('Не удалось сохранить серверную версию. Локальный черновик остался в браузере.');
      alert('Не удалось сохранить трекер. Попробуй ещё раз чуть позже.');
    }} finally {{
      button.disabled = false;
      button.style.opacity = '1';
    }}
  }}

  document.getElementById('saveTrackerBtn')?.addEventListener('click', saveTrackerToServer);

  const materialsShell = document.getElementById('materialsShell');
  const materialsToggle = document.getElementById('materialsToggle');
  const materialsToggleText = document.getElementById('materialsToggleText');
  const summaryToggle = document.getElementById('summaryToggle');
  const nutritionSummary = document.getElementById('nutritionSummary');

  materialsToggle?.addEventListener('click', () => {{
    if (!materialsShell || !materialsToggleText) {{
      return;
    }}
    const collapsed = materialsShell.classList.toggle('is-collapsed');
    materialsToggle.setAttribute('aria-expanded', String(!collapsed));
    materialsToggleText.textContent = collapsed ? 'Развернуть материалы' : 'Свернуть материалы';
  }});

    summaryToggle?.addEventListener('click', () => {{
      if (!nutritionSummary) {{
        return;
      }}
      const isOpen = nutritionSummary.classList.toggle('is-open');
      summaryToggle.setAttribute('aria-expanded', String(isOpen));
      summaryToggle.textContent = isOpen ? 'Скрыть краткое содержание' : 'Открыть краткое содержание';
    }});

  (async () => {{
    state = normalizeTrackerState(state);
    currentDay = 0;
    await loadSavedTracker();
    restoreLocalState();
    renderManifestoBanner();
    renderDayNav();
    renderDay();
    syncManifestoVisibility();
  }})();
</script>
"""


def build_participant_page(template: str, participant: dict[str, str]) -> str:
    slug = participant["slug"]
    html = add_personalization(template, participant["public_name"], participant["for_name"], slug)
    html = html.replace("</body>\n</html>", f"{build_runtime_script(participant['public_name'], slug)}\n</body>\n</html>", 1)
    if participant.get("issue"):
        source_comment = (
            f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['public_name']} "
            f"from GitHub issue #{participant['issue']}: https://github.com/OLYMARKES/high-performance-leads/issues/{participant['issue']} -->\n"
        )
    else:
        source_comment = f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['public_name']} from manual roster update -->\n"
    return source_comment + html


def build_index_page() -> str:
    return """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>HIGH PERFORMANCE — Private Week 1 Trackers</title>
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
      width: min(720px, 100%);
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
    <h1>Private <em>Week 1 Trackers</em></h1>
    <p>Эта директория не публикует список трекеров. Открыть персональный трекер можно только по личной или командной ссылке.</p>
  </div>
</body>
</html>
"""


def build_team_page(entries: list[dict[str, str]]) -> str:
    cards_html = "\n".join(
        f"""
          <a class="card" href="{entry['filename']}?{TRACKER_VERSION_QUERY}">
            <span class="card-name">{entry['name']}</span>
            <span class="card-meta">трекер недели 1 · {entry['telegram_handle']}</span>
          </a>"""
        for entry in entries
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>HIGH PERFORMANCE — Week 1 Team Access</title>
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
      <h1>Week 1 <em>Team Access</em></h1>
      <p class="hero-sub">Командная страница со всеми персональными трекерами первой недели. Эту ссылку не пересылаем участницам.</p>
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


def build_message_for_participant(participant: dict[str, str]) -> str:
    tracker_url = f"{PUBLIC_BASE_URL}/w1_{participant['token']}.html?{TRACKER_VERSION_QUERY}"
    greeting_name = participant["public_name"]
    return (
        f"=== {participant['display_name']} · {participant['telegram_handle']} ===\n"
        f"Привет, {greeting_name}!\n\n"
        f"Очень рада пригласить тебя в наш чат High Performance:\n"
        f"{CHAT_URL}\n\n"
        f"Я открываю чат и твой личный трекер заранее, чтобы ты могла спокойно войти в процесс в своём темпе, без спешки.\n\n"
        f"Здесь короткое Loom-видео, где я рассказываю, как устроен трекер и как с ним работать:\n"
        f"{LOOM_URL}\n\n"
        f"А вот твой личный трекер:\n"
        f"{tracker_url}\n\n"
        f"Внутри уже есть манифест, материалы по питанию и тренировкам и сам трекер первой недели. "
        f"Первая неделя у нас про базу: тело, питание, тренировки, ритм и снижение лишней когнитивной нагрузки на себя.\n\n"
        f"И там уже есть одна тренировка на завтра, так что если будет желание и ресурс, можно сразу её сделать)\n\n"
        f"Можно просто сначала открыть, осмотреться, почитать, посмотреть видео и постепенно начать входить в процесс. "
        f"Если захочешь, можешь сначала даже взять мой пример манифеста как опору, а потом уже написать свой.\n\n"
        f"Если что-то не открывается или будут вопросы, пиши мне.\n"
    )


def build_telegram_messages(participants: list[dict[str, str]]) -> str:
    blocks = [build_message_for_participant(participant) for participant in participants]
    return "\n\n" + ("\n\n" + ("-" * 72) + "\n\n").join(blocks) + "\n"


def main() -> None:
    template = SOURCE_TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    participants = get_participants()

    for old_file in OUTPUT_DIR.glob("w1_*.html"):
        old_file.unlink()
    for stale_name in ("links.txt", "telegram_message.txt"):
        stale_file = OUTPUT_DIR / stale_name
        if stale_file.exists():
            stale_file.unlink()
    for old_team_page in OUTPUT_DIR.glob("week1-team-*.html"):
        old_team_page.unlink()

    entries = []
    for participant in participants:
        slug = participant["slug"]
        filename = f"w1_{participant['token']}.html"
        page_html = build_participant_page(template, {**participant, "slug": slug})
        (OUTPUT_DIR / filename).write_text(page_html, encoding="utf-8")
        entries.append(
            {
                "name": participant["display_name"],
                "telegram_handle": participant["telegram_handle"],
                "filename": filename,
            }
        )

    (OUTPUT_DIR / "index.html").write_text(build_index_page(), encoding="utf-8")
    (OUTPUT_DIR / f"{TEAM_PAGE_TOKEN}.html").write_text(build_team_page(entries), encoding="utf-8")
    (OUTPUT_DIR / "telegram_message.txt").write_text(build_telegram_messages(participants), encoding="utf-8")
    print(f"Generated {len(entries)} week 1 trackers in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
