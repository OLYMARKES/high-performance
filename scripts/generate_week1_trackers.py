from __future__ import annotations

import json
from pathlib import Path

from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "week_1_trackers_april_2026"
SOURCE_TEMPLATE_PATH = Path("/Users/olymarkes/Documents/Claude/Projects/High perfomance/week-1-tracker.html")
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/week_1_trackers_april_2026"
TEAM_PAGE_TOKEN = "week1-vault-t8m4q2c7k9p5"
TRACKER_VERSION_QUERY = "v=materials-pdf-v23"
HABITS_PDF = "../habit-sheet.pdf?v=materials-pdf-v23"
NUTRITION_PDF = "../nutrition-guide.pdf?v=materials-pdf-v23"
SEKTA_CABINET_URL = "https://sektaschool.ru"
MAIN_PROGRAM_PDF = "../main-program.pdf?v=materials-pdf-v23"
MAIN_PROGRAM_PDF_OPEN = "../main-program.pdf?v=materials-pdf-v23#page=999"
CHAT_URL = "https://t.me/+UQzb3a_ohdliMTEy"
LOOM_URL = "https://www.loom.com/share/7c09b8ca1c0f44708bcda671c35a15d3"
DAY_WORKOUT_LINKS = [
    [
        {
            "label": "Тренировка дня",
            "url": "https://kinescope.io/6PmxVSfi4BYsarEmW2XRrZ",
        }
    ],
    [
        {
            "label": "Тренировка утра",
            "url": "https://kinescope.io/vfoVu9d7q1wSYKdK5qpo2t",
        },
        {
            "label": "Основная тренировка",
            "url": "https://kinescope.io/k3554A5VX2cGM2p2NzBXgp",
        }
    ],
    [
        {
            "label": "Тренировка дня",
            "url": "https://kinescope.io/4k83NSdtZyhTWaKEcYGY6f",
        }
    ],
    [
        {
            "label": "Тренировка 1",
            "url": "https://kinescope.io/dJuYS7wUg6jLdC7Wn4WHEe",
        },
        {
            "label": "Тренировка 2",
            "url": "https://kinescope.io/bnyKxZVoQBBgRdd9a6v5be",
        }
    ],
    [
        {
            "label": "Тренировка дня",
            "url": "https://kinescope.io/dg41DeFZiV3bestR5vsgNT",
        }
    ],
    [
        {
            "label": "Тренировка 1",
            "url": "https://kinescope.io/8bNzN33rMMc5F289UnjDYn",
        },
        {
            "label": "Тренировка 2",
            "url": "https://kinescope.io/et2qFrFvqZ5oohxazHhCHn",
        }
    ],
    [],
]


def build_workout_day_buttons_shell() -> str:
    return """              <div class="material-actions" id="workoutDayButtons"></div>"""


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
.save-panel-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 12px;
  flex-shrink: 0;
}
.save-secondary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: auto;
  min-width: 170px;
  min-height: 56px;
  padding: 12px 18px;
  border: 1px solid rgba(122, 116, 109, 0.22);
  border-radius: 999px;
  background: transparent;
  color: var(--charcoal);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}
.generated-story-card {
  margin-top: 16px;
  padding: 22px 24px;
  border: 1px solid var(--sand);
  border-radius: 20px;
  background: rgba(255, 253, 249, 0.92);
}
.generated-story-card[hidden] {
  display: none;
}
.generated-story-kicker {
  color: var(--terracotta);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 11px;
  font-weight: 700;
}
.generated-story-head {
  margin-top: 10px;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
}
.generated-story-title {
  font-family: var(--font-display);
  font-size: 28px;
  line-height: 1.05;
  color: var(--charcoal);
}
.generated-story-day {
  color: var(--warm-gray);
  font-size: 14px;
}
.generated-story-controls {
  margin-top: 18px;
  padding: 16px;
  border-radius: 18px;
  border: 1px solid rgba(226, 213, 195, 0.9);
  background: rgba(255, 255, 255, 0.56);
}
.generated-story-controls[hidden] {
  display: none;
}
.generated-story-controls-title {
  color: var(--charcoal);
  font-size: 14px;
  font-weight: 700;
}
.generated-story-controls-copy {
  margin-top: 6px;
  color: var(--warm-gray);
  font-size: 14px;
  line-height: 1.65;
}
.generated-story-angle-grid {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.generated-story-angle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 9px 14px;
  border-radius: 999px;
  border: 1px solid rgba(122, 116, 109, 0.22);
  background: rgba(255, 253, 249, 0.9);
  color: var(--charcoal);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}
.generated-story-angle.is-active {
  background: var(--charcoal);
  color: var(--warm-white);
  border-color: var(--charcoal);
}
.generated-story-input {
  width: 100%;
  margin-top: 14px;
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px solid rgba(122, 116, 109, 0.22);
  background: rgba(255, 253, 249, 0.96);
  color: var(--charcoal);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.6;
  resize: vertical;
  min-height: 96px;
}
.generated-story-body {
  margin-top: 16px;
  color: var(--charcoal);
  font-size: 16px;
  line-height: 1.75;
  white-space: pre-wrap;
}
.generated-story-actions {
  margin-top: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.generated-story-note {
  margin-top: 12px;
  color: var(--light-gray);
  font-size: 13px;
  line-height: 1.6;
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
  .save-panel-actions {
    justify-content: stretch;
  }
  .save-progress-btn {
    width: 100%;
    min-width: 0;
  }
  .save-secondary-btn {
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
    <section class="materials-shell reveal is-collapsed" id="materialsShell">
      <div class="materials-topline">
        <div>
          <h2 class="materials-title">Материалы <em>внутри трекера</em></h2>
        </div>
        <div style="display:flex; flex-direction:column; align-items:flex-end; gap:10px;">
          <div class="materials-note">Здесь лежат общие материалы программы: рекомендации и тренировочный план. Их не нужно искать в чате.</div>
          <button class="materials-toggle" id="materialsToggle" type="button" aria-expanded="false" aria-controls="materialsContent">
            <span id="materialsToggleText">Развернуть материалы</span>
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
            <p>Здесь лежат прямая ссылка на тренировку дня, PDF основной программы и бэкап-вариант в личном кабинете SektaSchool.ru.</p>
{WORKOUT_DAY_BUTTONS_SHELL}
            <div class="material-actions">
              <a class="material-btn secondary" href="{MAIN_PROGRAM_PDF}" download="main-program.pdf">Скачать PDF с тренировками основной программы</a>
              <a class="material-btn secondary" href="{SEKTA_CABINET_URL}" target="_blank" rel="noopener noreferrer">Ссылка на SektaSchool.ru с бэкап-программой</a>
            </div>
            <div class="material-meta">Сначала даю прямой вход в тренировку дня, затем основной PDF, а личный кабинет оставляю как запасной вариант доступа.</div>
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
          <div class="save-panel-status" id="saveStatus">По этой ссылке всегда будет открываться актуальная сохранённая версия трекера. Можно сразу собрать короткий рассказ по текущему дню.</div>
        </div>
        <div class="save-panel-actions">
          <button class="manifesto-btn save-progress-btn" id="generateStoryBtn" type="button">Сгенерировать рассказ</button>
          <button class="save-secondary-btn" id="saveTrackerBtn" type="button">Просто сохранить</button>
        </div>
      </div>
    </div>

    <div class="generated-story-card reveal" id="generatedStoryCard" hidden>
      <div class="generated-story-kicker">Тестовая версия</div>
      <div class="generated-story-head">
        <div class="generated-story-title">Рассказ о твоём дне</div>
        <div class="generated-story-day" id="generatedStoryDay">День 1</div>
      </div>
      <div class="generated-story-body" id="generatedStoryBody"></div>
      <div class="generated-story-controls" id="generatedStoryControls" hidden>
        <div class="generated-story-controls-title">Перед «Уточнить рассказ» можно подсветить важные углы</div>
        <div class="generated-story-controls-copy">Отметь, что особенно хочется услышать в тексте, или добавь свои правки. Тогда рассказ перестроится уже с этим акцентом.</div>
        <div class="generated-story-angle-grid" id="generatedStoryAngleGrid"></div>
        <textarea class="generated-story-input" id="generatedStoryPrompt" placeholder="Например: хочу, чтобы сильнее прозвучали дисциплина, радость и связь с телом. Или: добавь больше мотивации и ощущение прорыва."></textarea>
        <div class="generated-story-actions">
          <button class="manifesto-btn" id="applyStoryPreferencesBtn" type="button">Пересобрать рассказ</button>
        </div>
      </div>
      <div class="generated-story-actions">
        <button class="manifesto-btn" id="copyGeneratedStoryBtn" type="button">Скопировать текст</button>
        <button class="save-secondary-btn" id="regenerateStoryBtn" type="button">Уточнить рассказ</button>
      </div>
      <div class="generated-story-note">Пока это локальная тестовая функция: трекер сначала сохраняется, а затем текст собирается прямо из текущего дня без изменения твоих данных.</div>
    </div>

  </div>
</section>""",
        1,
    )
    html = html.replace(
        "const DAY_NAMES = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];",
        "const DAY_NAMES = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];",
        1,
    )
    html = html.replace(
        '<h1>Неделя <em>1</em></h1>',
        '<h1>Неделя <em>1</em></h1>',
        1,
    )
    html = html.replace(
        '<div class="day-date">День ${currentDay + 1} из 7</div>',
        '<div class="day-date">День ${currentDay + 1} из 7</div>',
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
        1,
    )
    html = html.replace(
        """function switchDay(index) {
  currentDay = index;
  renderDayNav();
  renderDay();
}""",
        """function switchDay(index) {
  currentDay = index;
  renderWorkoutMaterialButtons();
  renderDayNav();
  renderDay();
}""",
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
    html = html.replace("{WORKOUT_DAY_BUTTONS_SHELL}", build_workout_day_buttons_shell())
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
  const MATERIALS_COLLAPSED_KEY = `${{LOCAL_KEY}}:materials-collapsed`;
  const STORY_PREFERENCES_KEY = `${{LOCAL_KEY}}:story-preferences`;
  const DAY_WORKOUT_LINKS = {quote_js(DAY_WORKOUT_LINKS)};
  const STORY_ANGLE_OPTIONS = ['фокус', 'энергия', 'тело', 'дисциплина', 'мягкость', 'смелость', 'радость', 'контакт с собой'];
  function getDefaultDayItems() {{
    return DEFAULT_ITEMS.map((item, index) => ({{
      ...item,
      id: item.id + '_' + index,
      checked: false,
      inputValue: ''
    }}));
  }}

  function normalizeTrackerState(rawState) {{
    const baseDays = DAY_NAMES.map((name) => ({{
      name,
      items: getDefaultDayItems()
    }}));

    if (!rawState || typeof rawState !== 'object') {{
      return {{
        manifesto: '',
        days: baseDays
      }};
    }}

    const rawDays = Array.isArray(rawState.days) ? rawState.days : [];
    const normalizedDays = baseDays.map((baseDay, dayIndex) => {{
      const incomingDay = rawDays[dayIndex] && typeof rawDays[dayIndex] === 'object'
        ? rawDays[dayIndex]
        : dayIndex === 0 && rawDays[0] && typeof rawDays[0] === 'object'
          ? rawDays[0]
          : null;

      const normalizedItems = Array.isArray(incomingDay?.items)
        ? incomingDay.items.map((item, index) => ({{
            ...item,
            id: item?.id || `item_${{dayIndex}}_${{index}}`,
            checked: Boolean(item?.checked),
            inputValue: typeof item?.inputValue === 'string' ? item.inputValue : ''
          }}))
        : baseDay.items;

      return {{
        ...baseDay,
        ...incomingDay,
        name: baseDay.name,
        items: normalizedItems
      }};
    }});

    return {{
      ...rawState,
      manifesto: typeof rawState.manifesto === 'string' ? rawState.manifesto : '',
      days: normalizedDays
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

  function setButtonBusy(button, busy, busyLabel) {{
    if (!button) {{
      return;
    }}
    if (!button.dataset.defaultLabel) {{
      button.dataset.defaultLabel = button.textContent || '';
    }}
    button.disabled = busy;
    button.style.opacity = busy ? '0.7' : '1';
    button.textContent = busy ? busyLabel : button.dataset.defaultLabel;
  }}

  function cropText(value, limit = 140) {{
    const text = String(value || '').replace(/\s+/g, ' ').trim();
    if (!text) {{
      return '';
    }}
    return text.length > limit ? text.slice(0, limit - 1).trimEnd() + '…' : text;
  }}

  function joinHumanList(items) {{
    const filtered = items.filter(Boolean);
    if (!filtered.length) {{
      return '';
    }}
    if (filtered.length === 1) {{
      return filtered[0];
    }}
    if (filtered.length === 2) {{
      return `${{filtered[0]}} и ${{filtered[1]}}`;
    }}
    return `${{filtered.slice(0, -1).join(', ')}} и ${{filtered[filtered.length - 1]}}`;
  }}

  function normalizeStoryPreferences(raw) {{
    const base = raw && typeof raw === 'object' ? raw : {{}};
    const rawAngles = Array.isArray(base.angles) ? base.angles : [];
    const angles = rawAngles
      .map((value) => String(value || '').trim().toLowerCase())
      .filter((value, index, list) => value && STORY_ANGLE_OPTIONS.includes(value) && list.indexOf(value) === index);
    return {{
      angles,
      customPrompt: typeof base.customPrompt === 'string' ? base.customPrompt : ''
    }};
  }}

  function readStoryPreferences() {{
    try {{
      const saved = localStorage.getItem(STORY_PREFERENCES_KEY);
      if (!saved) {{
        return normalizeStoryPreferences(null);
      }}
      return normalizeStoryPreferences(JSON.parse(saved));
    }} catch (error) {{
      return normalizeStoryPreferences(null);
    }}
  }}

  function persistStoryPreferences(preferences) {{
    try {{
      localStorage.setItem(STORY_PREFERENCES_KEY, JSON.stringify(normalizeStoryPreferences(preferences)));
    }} catch (error) {{
      // Ignore local preference storage failures.
    }}
  }}

  function toggleStoryAngle(angle) {{
    const preferences = readStoryPreferences();
    const angles = preferences.angles.includes(angle)
      ? preferences.angles.filter((item) => item !== angle)
      : [...preferences.angles, angle];
    persistStoryPreferences({{
      ...preferences,
      angles
    }});
    renderStoryControls();
  }}

  function renderStoryControls() {{
    const grid = document.getElementById('generatedStoryAngleGrid');
    const input = document.getElementById('generatedStoryPrompt');
    const preferences = readStoryPreferences();
    if (grid) {{
      grid.innerHTML = STORY_ANGLE_OPTIONS.map((angle) => `
        <button class="generated-story-angle${{preferences.angles.includes(angle) ? ' is-active' : ''}}" type="button" data-angle="${{angle}}">${{angle}}</button>
      `).join('');
      grid.querySelectorAll('[data-angle]').forEach((button) => {{
        button.addEventListener('click', () => toggleStoryAngle(button.dataset.angle || ''));
      }});
    }}
    if (input && input.value !== preferences.customPrompt) {{
      input.value = preferences.customPrompt;
    }}
  }}

  function buildAngleFocusParagraph(angles) {{
    const map = {{
      'фокус': 'Сегодня мне важно услышать, что через этот день у меня собирается фокус и я перестаю распыляться.',
      'энергия': 'Я хочу отдельно отметить, что такими шагами я возвращаю себе энергию и внутренний огонь.',
      'тело': 'Мне важно почувствовать, что тело здесь не фон, а моя реальная опора и точка силы.',
      'дисциплина': 'Хочу удержать мысль, что дисциплина в этом дне — не наказание, а форма любви и уважения к себе.',
      'мягкость': 'Мне нравится, что я могу двигаться мягко, без жёсткости к себе, и всё равно не выпадать из процесса.',
      'смелость': 'Я хочу видеть в этом дне свою смелость: не ждать идеального состояния, а всё равно выбирать движение.',
      'радость': 'Для меня важно не только сделать, но и порадоваться себе, заметить живую радость от того, что получается.',
      'контакт с собой': 'Больше всего мне хочется слышать, что через этот день я возвращаюсь в контакт с собой и яснее чувствую, что для меня важно.'
    }};
    return angles.map((angle) => map[angle]).filter(Boolean).slice(0, 3).join(' ');
  }}

  function manifestoLead() {{
    const text = String(state.manifesto || '').replace(/\s+/g, ' ').trim();
    if (!text) {{
      return '';
    }}
    const sentence = text.split(/[.!?]+/).map((part) => part.trim()).find(Boolean) || text;
    return cropText(sentence, 140);
  }}

  function manifestoSpark() {{
    const current = manifestoLead();
    if (current) {{
      return current;
    }}
    return 'Сегодня я выбираю ясность, фокус, смелость, энергию и огонь. Мои ценности важнее хаоса, а дисциплина — это форма заботы о себе';
  }}

  function getDayItemById(day, itemId) {{
    const items = Array.isArray(day?.items) ? day.items : [];
    return items.find((item) => item && item.id === itemId) || null;
  }}

  function getFilledValue(item) {{
    return cropText(item?.inputValue || '', 180);
  }}

  function joinSentences(parts) {{
    return parts.filter(Boolean).join(' ');
  }}

  function buildDayFlowParagraph(day) {{
    const flowMap = {{
      sleep: 'дала себе базу сна',
      meditation: 'начала день с короткой медитации',
      breakfast: 'собрала себе завтрак',
      reading: 'выделила время на чтение',
      journaling: 'оставила место для джорналинга',
      workout: 'сделала тренировку',
      lunch: 'не пропустила полноценный обед',
      hardstop: 'поставила рамку работе',
      qualitytime: 'побыла с близкими по-настоящему',
      dinner: 'собрала ужин',
      bedtime: 'подошла к вечеру с заботой о завтрашнем дне'
    }};
    const morningIds = ['sleep', 'meditation', 'breakfast', 'reading'];
    const dayIds = ['workout', 'lunch', 'hardstop', 'journaling'];
    const eveningIds = ['qualitytime', 'dinner', 'bedtime'];
    const collect = (ids) => ids
      .map((id) => getDayItemById(day, id))
      .filter((item) => item?.checked)
      .map((item) => flowMap[item.id] || item.title?.toLowerCase());

    const morning = collect(morningIds);
    const daytime = collect(dayIds);
    const evening = collect(eveningIds);
    const paragraphs = [];

    if (morning.length) {{
      paragraphs.push(`С утра я ${{joinHumanList(morning)}}, и это задало дню хороший тон.`);
    }}
    if (daytime.length) {{
      paragraphs.push(`Днём у меня получилось ${{joinHumanList(daytime)}}, так что день не рассыпался, а держался на реальных действиях.`);
    }}
    if (evening.length) {{
      paragraphs.push(`К вечеру я ${{joinHumanList(evening)}}, и в этом уже чувствуется не просто выполнение плана, а забота о своей устойчивости.`);
    }}

    if (!paragraphs.length) {{
      return 'Сегодня день пока не сложился в чёткую структуру, но я всё равно смотрю на него честно и собираю из этого материал для следующего шага.';
    }}

    return paragraphs.join(' ');
  }}

  function buildSleepParagraph(day) {{
    const sleepItem = getDayItemById(day, 'sleep');
    const bedtimeItem = getDayItemById(day, 'bedtime');
    const sleepNote = getFilledValue(sleepItem);
    const parts = [];

    if (sleepItem?.checked) {{
      parts.push('По сну я дала себе базу: цель в 7 часов была выдержана, и это уже сильно влияет на то, как я держу фокус и энергию.');
    }} else if (sleepNote) {{
      parts.push(`По сну я пока не дотянула до своей цели, но уже вижу реальность дня без искажений: ${{sleepNote}}. Это не повод давить на себя, а полезная точка для калибровки.`);
    }} else {{
      parts.push('По сну я пока не дотянула до своей опоры в 7 часов, и мне важно это заметить спокойно: без драматизации, но и без попытки обесценить влияние сна на моё состояние.');
    }}

    if (bedtimeItem?.checked) {{
      parts.push('При этом я всё равно стараюсь защитить следующий день и лечь вовремя, а это уже работает на меня в долгую.');
    }} else {{
      parts.push('Значит, мой следующий понятный шаг здесь — мягко вернуть себе вечернюю рамку, чтобы завтра было проще собрать энергию.');
    }}

    return joinSentences(parts);
  }}

  function analyzeMealText(text) {{
    const source = String(text || '').toLowerCase();
    const proteinKeywords = ['яйц', 'кур', 'индейк', 'рыб', 'лосос', 'тун', 'творог', 'йогурт', 'кефир', 'сыр', 'моцарел', 'мяс', 'говяд', 'кревет', 'тофу', 'темпе', 'фасол', 'нут', 'чечев', 'протеин'];
    const fiberKeywords = ['овощ', 'салат', 'зелень', 'огур', 'томат', 'брокк', 'капуст', 'кабач', 'морков', 'свекл', 'ягод', 'фрукт', 'яблок', 'груш', 'авокад', 'греч', 'овсян', 'киноа', 'чечев'];
    const energyKeywords = ['рис', 'карто', 'паста', 'макарон', 'хлеб', 'лаваш', 'круп', 'каша', 'греч', 'булгур', 'киноа', 'банан', 'мюсли', 'гранола'];
    const lightKeywords = ['кофе', 'чай', 'капуч', 'латте', 'печень', 'батончик', 'яблок', 'банан', 'йогурт', 'смузи'];

    const hasKeyword = (keywords) => keywords.some((keyword) => source.includes(keyword));
    return {{
      protein: hasKeyword(proteinKeywords),
      fiber: hasKeyword(fiberKeywords),
      energy: hasKeyword(energyKeywords),
      light: hasKeyword(lightKeywords)
    }};
  }}

  function buildNutritionParagraph(day) {{
    const mealIds = [
      ['breakfast', 'завтрак'],
      ['lunch', 'обед'],
      ['dinner', 'ужин']
    ];
    const mealSummaries = [];
    let proteinCount = 0;
    let fiberCount = 0;
    let energyCount = 0;
    let lightCount = 0;
    let checkedMeals = 0;

    mealIds.forEach(([id, label]) => {{
      const item = getDayItemById(day, id);
      if (!item?.checked && !getFilledValue(item)) {{
        return;
      }}
      checkedMeals += item?.checked ? 1 : 0;
      const note = getFilledValue(item);
      if (note) {{
        mealSummaries.push(`на ${{label}} у меня было ${{note}}`);
        const mealAnalysis = analyzeMealText(note);
        proteinCount += mealAnalysis.protein ? 1 : 0;
        fiberCount += mealAnalysis.fiber ? 1 : 0;
        energyCount += mealAnalysis.energy ? 1 : 0;
        lightCount += mealAnalysis.light ? 1 : 0;
      }} else {{
        mealSummaries.push(`${{label}} я не пропустила`);
      }}
    }});

    if (!mealSummaries.length) {{
      return 'По еде я сегодня почти не оставила следов в трекере, так что в следующий заход мне полезно записать хотя бы пару слов про завтрак, обед или ужин: это сразу даст больше ясности про мой реальный ритм и опоры.';
    }}

    const analysisParts = [];
    if (proteinCount >= 2) {{
      analysisParts.push('По ощущению, сегодня в рационе уже была неплохая опора на белок.');
    }} else if (proteinCount === 1) {{
      analysisParts.push('Белок сегодня, скорее всего, был, но опора на него пока выглядит не очень устойчивой на протяжении дня.');
    }} else {{
      analysisParts.push('По записям кажется, что сегодня рациону не хватило явной опоры на белок.');
    }}

    if (fiberCount >= 2) {{
      analysisParts.push('Плюс в еде уже заметна клетчатка, а это добавляет сытости и устойчивости.');
    }} else if (fiberCount === 0) {{
      analysisParts.push('Ещё я вижу пространство усилить рацион овощами, зеленью или другими источниками клетчатки.');
    }}

    if (checkedMeals <= 1 || (energyCount === 0 && lightCount >= 1)) {{
      analysisParts.push('И по общему ощущению день по калориям мог получиться довольно лёгким, так что здесь важно не остаться на случайных перекусах.');
    }} else if (checkedMeals >= 2 && energyCount >= 1) {{
      analysisParts.push('По энергии день выглядит более собранным: в рационе были не только быстрые решения, но и еда, которая реально поддерживает меня дольше.');
    }}

    return `По еде день выглядел так: ${{joinHumanList(mealSummaries)}}. ${{analysisParts.join(' ')}}`.trim();
  }}

  function buildWinsParagraph(day, checked) {{
    const highlightMap = {{
      sleep: 'не обесценила сон как базу',
      meditation: 'дала себе момент тишины и внутренней настройки',
      workout: 'выбрала тело и движение, а не очередное «потом»',
      breakfast: 'не оставила утро без нормальной еды',
      lunch: 'поддержала себя полноценным обедом',
      dinner: 'не забыла про ужин и завершение дня',
      reading: 'вернула себе внимание через чтение',
      journaling: 'оставила место для честного контакта с собой',
      hardstop: 'поставила границу работе',
      qualitytime: 'сохранила живое присутствие рядом с близкими',
      bedtime: 'защитила свой следующий день'
    }};
    const wins = checked
      .map((item) => highlightMap[item.id] || item.title?.toLowerCase())
      .filter(Boolean)
      .slice(0, 4);
    if (!wins.length) {{
      return 'И всё же даже сегодня у меня есть за что себя поддержать: я не отвернулась от себя и не спряталась от правды про день.';
    }}
    return `Самое классное сегодня — вот это: я ${{joinHumanList(wins)}}. Именно такие штуки и хочется праздновать, потому что из них и собирается моя новая норма.`;
  }}

  function buildProgramLensParagraph(checked) {{
    if (checked.length >= 4) {{
      return 'И я очень чувствую, что именно ради этого и нужен High Performance: не чтобы героически вывозить всё сразу, а чтобы через понятные опоры собрать базу тела, питания, ритма и внимания. Когда у меня появляется такая база, жизнь становится не тяжелее, а легче и чище.';
    }}
    if (checked.length >= 1) {{
      return 'И я вижу, как это встраивается в саму идею High Performance: первая неделя у нас не про идеальность, а про базу. Через такие маленькие шаги я снижаю хаос, убираю лишнюю когнитивную нагрузку и собираю для себя более устойчивый ритм.';
    }}
    return 'И даже такой день всё равно остаётся частью процесса. Здесь задача не в том, чтобы мгновенно стать идеальной версией себя, а в том, чтобы мягко войти в новый ритм и увидеть, какая база действительно помогает мне жить устойчивее.';
  }}

  function buildStoryFromCurrentDay() {{
    const preferences = readStoryPreferences();
    const day = state.days[currentDay] || {{ name: `День ${{currentDay + 1}}`, items: [] }};
    const items = Array.isArray(day.items) ? day.items : [];
    const checked = items.filter((item) => item && item.checked);
    const opening = checked.length >= 5
      ? `Сегодня я правда собрала для себя очень сильный ${{day.name.toLowerCase()}}, и это хочется отпраздновать. Я не просто прошла по списку, а реально выбрала себя, свой ритм и свои опоры.`
      : checked.length >= 3
        ? `Сегодня я удержала важные опоры дня, и это уже очень классный результат. Я двигаюсь не рывком, а повторяемостью, и именно это даёт мне чувство внутренней силы.`
        : checked.length >= 1
          ? `Сегодня я всё равно не выпала из контакта с собой. Даже несколько выполненных опор — это уже движение в сторону моей базы, и я хочу это отметить.`
          : `Сегодня я хотя бы посмотрела на свой день честно, а это уже начало опоры. Иногда мой главный шаг — не сделать идеально, а заметить, где я сейчас, и остаться рядом с собой.`;
    const dayFlow = buildDayFlowParagraph(day);
    const sleep = buildSleepParagraph(day);
    const nutrition = buildNutritionParagraph(day);
    const wins = buildWinsParagraph(day, checked);
    const programLens = buildProgramLensParagraph(checked);
    const manifesto = `И я слышу, как это связано с моим манифестом: «${{manifestoSpark()}}». Когда я выбираю даже маленькие действия в его сторону, мои ценности перестают быть красивыми словами и становятся тем, как я реально проживаю день.`;
    const angleFocus = buildAngleFocusParagraph(preferences.angles);
    const promptLine = preferences.customPrompt.trim()
      ? `И ещё я хочу удержать в этом рассказе вот такой мой акцент: ${{cropText(preferences.customPrompt, 220)}}.`
      : '';
    const closing = checked.length >= 4
      ? 'Я хочу запомнить это состояние: у меня уже получается входить в этот процесс без надрыва и собирать для себя сильную базу. Не через жёсткость, а через повторяемость, внимание к себе и уважение к тому ритму, который я действительно могу удерживать.'
      : 'Мне не нужно впечатлять этот день, чтобы он был важным. Мне важно просто продолжать входить в процесс, замечать, что работает для меня, и шаг за шагом собирать ту базу, на которой потом держатся и энергия, и фокус, и ощущение внутренней силы.';

    return [opening, dayFlow, sleep, nutrition, wins, programLens, manifesto, angleFocus, promptLine, closing].filter(Boolean).join('\\n\\n');
  }}

  function renderGeneratedStory(text) {{
    const card = document.getElementById('generatedStoryCard');
    const body = document.getElementById('generatedStoryBody');
    const dayLabel = document.getElementById('generatedStoryDay');
    if (!card || !body || !dayLabel) {{
      return;
    }}
    dayLabel.textContent = state.days[currentDay]?.name || `День ${{currentDay + 1}}`;
    body.textContent = text;
    card.hidden = false;
  }}

  function toggleStoryControls(forceOpen = null) {{
    const controls = document.getElementById('generatedStoryControls');
    const trigger = document.getElementById('regenerateStoryBtn');
    if (!controls || !trigger) {{
      return;
    }}
    const shouldOpen = forceOpen === null ? controls.hidden : !forceOpen ? false : true;
    controls.hidden = !shouldOpen;
    trigger.textContent = shouldOpen ? 'Скрыть настройки пересборки' : 'Уточнить рассказ';
  }}

  async function copyGeneratedStory() {{
    const body = document.getElementById('generatedStoryBody');
    const copyButton = document.getElementById('copyGeneratedStoryBtn');
    const text = body?.textContent || '';
    if (!text || !copyButton) {{
      return;
    }}
    const original = copyButton.textContent;
    try {{
      await navigator.clipboard.writeText(text);
      copyButton.textContent = 'Скопировано';
    }} catch (error) {{
      copyButton.textContent = 'Не скопировалось';
    }}
    setTimeout(() => {{
      copyButton.textContent = original;
    }}, 1800);
  }}

  function readMaterialsCollapsedState() {{
    try {{
      const saved = localStorage.getItem(MATERIALS_COLLAPSED_KEY);
      if (saved === null) {{
        return true;
      }}
      return saved !== 'false';
    }} catch (error) {{
      return true;
    }}
  }}

  function persistMaterialsCollapsedState(collapsed) {{
    try {{
      localStorage.setItem(MATERIALS_COLLAPSED_KEY, collapsed ? 'true' : 'false');
    }} catch (error) {{
      // Ignore preference storage failures and keep the UI usable.
    }}
  }}

  function renderWorkoutMaterialButtons() {{
    const container = document.getElementById('workoutDayButtons');
    if (!container) {{
      return;
    }}

    const links = Array.isArray(DAY_WORKOUT_LINKS[currentDay]) ? DAY_WORKOUT_LINKS[currentDay] : [];
    if (!links.length) {{
      container.innerHTML = '';
      return;
    }}

    container.innerHTML = links.map((link, index) => `
      <a class="material-btn${{index === 0 ? '' : ' secondary'}}" href="${{link.url}}" target="_blank" rel="noopener noreferrer">${{link.label}}</a>
    `).join('');
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
      renderWorkoutMaterialButtons();
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
      renderWorkoutMaterialButtons();
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

  async function persistTrackerSnapshot(triggerButton, pendingStatus = 'Сохраняю трекер...') {{
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

    const saveButton = document.getElementById('saveTrackerBtn');
    const storyButton = document.getElementById('generateStoryBtn');
    setButtonBusy(saveButton, true, 'Сохраняю...');
    setButtonBusy(storyButton, true, 'Собираю...');
    setSaveStatus(pendingStatus);

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
      return true;
    }} catch (error) {{
      setSaveStatus('Не удалось сохранить серверную версию. Локальный черновик остался в браузере.');
      alert('Не удалось сохранить трекер. Попробуй ещё раз чуть позже.');
      return false;
    }} finally {{
      setButtonBusy(saveButton, false, '');
      setButtonBusy(storyButton, false, '');
    }}
  }}

  async function saveTrackerToServer() {{
    await persistTrackerSnapshot(document.getElementById('saveTrackerBtn'));
  }}

  async function generateStoryFlow() {{
    const persisted = await persistTrackerSnapshot(
      document.getElementById('generateStoryBtn'),
      'Сохраняю трекер и собираю рассказ о дне...'
    );
    if (!persisted) {{
      return;
    }}
    renderGeneratedStory(buildStoryFromCurrentDay());
    setSaveStatus('Трекер сохранён, а короткий рассказ о текущем дне собран ниже.');
  }}

  document.getElementById('saveTrackerBtn')?.addEventListener('click', saveTrackerToServer);
  document.getElementById('generateStoryBtn')?.addEventListener('click', generateStoryFlow);
  document.getElementById('copyGeneratedStoryBtn')?.addEventListener('click', copyGeneratedStory);
  document.getElementById('regenerateStoryBtn')?.addEventListener('click', () => toggleStoryControls());
  document.getElementById('applyStoryPreferencesBtn')?.addEventListener('click', generateStoryFlow);
  document.getElementById('generatedStoryPrompt')?.addEventListener('input', (event) => {{
    const preferences = readStoryPreferences();
    persistStoryPreferences({{
      ...preferences,
      customPrompt: event.target.value
    }});
  }});

  const materialsShell = document.getElementById('materialsShell');
  const materialsToggle = document.getElementById('materialsToggle');
  const materialsToggleText = document.getElementById('materialsToggleText');
  const summaryToggle = document.getElementById('summaryToggle');
  const nutritionSummary = document.getElementById('nutritionSummary');

  function applyMaterialsCollapsedState(collapsed) {{
    if (!materialsShell || !materialsToggle || !materialsToggleText) {{
      return;
    }}
    materialsShell.classList.toggle('is-collapsed', collapsed);
    materialsToggle.setAttribute('aria-expanded', String(!collapsed));
    materialsToggleText.textContent = collapsed ? 'Развернуть материалы' : 'Свернуть материалы';
  }}

  materialsToggle?.addEventListener('click', () => {{
    if (!materialsShell || !materialsToggleText) {{
      return;
    }}
    const collapsed = !materialsShell.classList.contains('is-collapsed');
    applyMaterialsCollapsedState(collapsed);
    persistMaterialsCollapsedState(collapsed);
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
    applyMaterialsCollapsedState(readMaterialsCollapsedState());
    state = normalizeTrackerState(state);
    currentDay = 0;
    await loadSavedTracker();
    restoreLocalState();
    renderStoryControls();
    toggleStoryControls(false);
    renderManifestoBanner();
    renderWorkoutMaterialButtons();
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
