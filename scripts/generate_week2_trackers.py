from __future__ import annotations

import json
from pathlib import Path

from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "week_2_trackers_april_2026"
SOURCE_TEMPLATE_PATH = Path("/Users/olymarkes/Documents/Claude/Projects/High perfomance/week-1-tracker.html")
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/week_2_trackers_april_2026"
WEEK2_TRACKER_BASE_URL = "https://olymarkes.github.io/high-performance/week_2_trackers_april_2026"
TEAM_PAGE_TOKEN = "week2-vault-m3q8t4k1v6p2"
TRACKER_VERSION_QUERY = "v=week2-materials-v33"
HABITS_PDF = f"../habit-sheet.pdf?{TRACKER_VERSION_QUERY}"
NUTRITION_PDF = f"../nutrition-guide.pdf?{TRACKER_VERSION_QUERY}"
CHAT_URL = "https://t.me/+UQzb3a_ohdliMTEy"
LOOM_URL = "https://www.loom.com/share/7c09b8ca1c0f44708bcda671c35a15d3"
JOURNEY_LINK_URL = "../journey-link-meditation-journaling.html"
ANXIETY_WHY_URL = "../zachem-rabotat-s-trevogoj.html?v=20260403-1"
ANXIETY_TYPES_URL = "../6-vidov-trevogi.html"
ANXIETY_POSTS_URL = "../12-postov-o-trevoge.html"
UNWINDING_ANXIETY_QUOTE = "You have to know how your mind works, before you can work with it."
DAY_WORKOUT_LINKS = [
    [
        {
            "label": "Основная тренировка · 24 мин",
            "url": "https://kinescope.io/woU5ouQr7kiQEnycQPYXEX",
        }
    ],
    [
        {
            "label": "Утренняя тренировка · 6:33",
            "url": "https://kinescope.io/uaz5nixLrRduo5AmzvoXhW",
        },
        {
            "label": "Основная тренировка · 16 мин",
            "url": "https://kinescope.io/uXu1PEQTWt2sCbKB858GZF",
        },
        {
            "label": "Массаж пресса",
            "url": "https://kinescope.io/5PFiKiBJriPtoZ7ReCqyf5",
        }
    ],
    [
        {
            "label": "Основная тренировка · 38 мин",
            "url": "https://kinescope.io/2HkhvcayLsmVNpgR9jrMbK",
        },
        {
            "label": "Массаж пресса",
            "url": "https://kinescope.io/5PFiKiBJriPtoZ7ReCqyf5",
        }
    ],
    [
        {
            "label": "Утренняя тренировка · 10 мин",
            "url": "https://kinescope.io/ow9ewbHa69dcm4AWvx2XCz",
        },
        {
            "label": "Основная тренировка · 15 мин",
            "url": "https://kinescope.io/qp8RLa4QH6wNXf9whu4q4r",
        }
    ],
    [
        {
            "label": "Основная тренировка · 33:48",
            "url": "https://kinescope.io/58nwQikeU2a2ogVNUH4k6z",
        }
    ],
    [
        {
            "label": "Утренняя тренировка · 8:34",
            "url": "https://kinescope.io/bjFtvWtjjzbFx6Brso3Au3",
        },
        {
            "label": "Основная тренировка · 18:17",
            "url": "https://kinescope.io/6TGpUpaVWmGAKFWHRyythM",
        },
        {
            "label": "Массаж пресса",
            "url": "https://kinescope.io/5PFiKiBJriPtoZ7ReCqyf5",
        }
    ],
    [],
]
CURATOR_TRACKER_PARTICIPANTS = [
    {
        "full_name": "Варя",
        "public_name": "Варя",
        "for_name": "Вари",
        "display_name": "Варя",
        "telegram_handle": "@va_rom",
        "slug": "varya-curator",
        "token": "k7v3m9q2t6p4",
    },
    {
        "full_name": "Таня",
        "public_name": "Таня",
        "for_name": "Тани",
        "display_name": "Таня",
        "telegram_handle": "@tparam",
        "slug": "tanya-curator",
        "token": "p8m4k2v7q6t1",
    },
    {
        "full_name": "Света",
        "public_name": "Света",
        "for_name": "Светы",
        "display_name": "Света",
        "telegram_handle": "@svetlana_saltykova",
        "slug": "sveta-curator",
        "token": "s4v8k2m7q1t5",
    },
    {
        "full_name": "Настя",
        "public_name": "Настя",
        "for_name": "Насти",
        "display_name": "Настя",
        "telegram_handle": "@Nastia_Lee",
        "slug": "nastya-curator",
        "token": "n5t2v8k4q7m1",
    },
]


def build_workout_day_buttons_shell() -> str:
    return """              <div class="material-actions" id="workoutDayButtons"></div>
              <div class="material-empty-state" id="workoutEmptyState">Тренировки для этой недели появятся здесь отдельными кнопками. Пока можно вернуться позже по этой же ссылке.</div>"""


def quote_js(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_week_switch_markup(token: str, active_week: int) -> str:
    week1_class = " is-active" if active_week == 1 else ""
    week2_class = " is-active" if active_week == 2 else ""
    return f"""    <nav class="week-switch reveal" aria-label="Переключение недели">
      <a class="week-switch-btn{week1_class}" href="../week_1_trackers_april_2026/w1_{token}.html?{TRACKER_VERSION_QUERY}">Неделя 1</a>
      <a class="week-switch-btn{week2_class}" href="../week_2_trackers_april_2026/w2_{token}.html?{TRACKER_VERSION_QUERY}">Неделя 2</a>
    </nav>"""


def get_week1_tracker_participants() -> list[dict[str, str]]:
    return [*get_participants(), *CURATOR_TRACKER_PARTICIPANTS]


def add_personalization(template: str, name: str, for_name: str, slug: str, token: str) -> str:
    html = template
    html = html.replace(
        """:root {
  --cream: #FBF7F2;
  --warm-white: #FFFDF9;
  --sand: #F0E8DC;
  --sand-dark: #E2D5C3;
  --terracotta: #C4704B;
  --terracotta-light: #D4896A;
  --terracotta-pale: #F2DDD2;
  --olive: #7A8B6F;
  --olive-light: #A3B396;
  --olive-pale: #E8EDDF;
  --charcoal: #3A3632;
  --warm-gray: #7A746D;
  --light-gray: #B5AFA7;
  --accent-gold: #C6A96C;
  --font-display: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'Nunito Sans', 'Segoe UI', sans-serif;
}""",
        """:root {
  --cream: #edf3f8;
  --warm-white: #f9fcff;
  --sand: #dde6f0;
  --sand-dark: #c8d6e5;
  --terracotta: #587ea6;
  --terracotta-light: #7ea5ce;
  --terracotta-pale: #dce8f5;
  --olive: #6f879d;
  --olive-light: #96aec2;
  --olive-pale: #e4edf4;
  --charcoal: #111111;
  --warm-gray: #111111;
  --light-gray: #384859;
  --accent-gold: #8aa9c6;
  --font-display: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'Nunito Sans', 'Segoe UI', sans-serif;
}""",
        1,
    )
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots" content="noindex, nofollow, noarchive">',
        1,
    )
    html = html.replace("<title>Трекер недели 1 — High Performance</title>", f"<title>Трекер недели 2 — {name}</title>", 1)
    html = html.replace(
        '<div class="hero-tag">High Performance · Трекер · Апрель 2026</div>',
        f'<div class="hero-tag">High Performance · {name} · Неделя 2</div>',
        1,
    )
    html = html.replace(
        '<p class="hero-sub">Твой ежедневный трекер привычек. Отмечай, наблюдай, двигайся вперёд.</p>',
        f'<p class="hero-sub">Персональный трекер второй недели для {for_name}. Здесь остаётся ежедневный трекер, а сверху уже собраны материалы недели 2 и продублированы опоры по привычкам и питанию.</p>',
        1,
    )
    html = html.replace(
        """.manifesto-modal .modal-desc {
  font-size: 15px;
  color: var(--warm-gray);
  line-height: 1.65;
  margin-bottom: 28px;
}

.manifesto-textarea {""",
        """.manifesto-modal .modal-desc {
  font-size: 15px;
  color: var(--warm-gray);
  line-height: 1.65;
  margin-bottom: 28px;
}
.week2-quote {
  background: linear-gradient(135deg, rgba(255,255,255,0.82), rgba(220, 232, 245, 0.92));
  border: 1px solid rgba(88, 126, 166, 0.18);
  border-radius: 18px;
  padding: 18px 20px;
  margin-bottom: 20px;
}
.week2-quote-copy {
  font-family: var(--font-display);
  font-size: 24px;
  line-height: 1.22;
  color: var(--charcoal);
}
.week2-quote-meta {
  margin-top: 10px;
  color: var(--terracotta);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.manifesto-textarea {""",
        1,
    )
    html = html.replace(
        '<div class="modal-tag">Твой манифест</div>',
        '<div class="modal-tag">Неделя 2 · обновление манифеста</div>',
        1,
    )
    html = html.replace(
        '<h2>Ясные ценности <em>&gt; ясные цели</em></h2>',
        '<h2>Замечаю тревогу <em>и не отдаю ей управление</em></h2>',
        1,
    )
    html = html.replace(
        """    <div style="background:var(--cream);border-left:3px solid var(--terracotta);border-radius:0 12px 12px 0;padding:16px 20px;margin-bottom:20px;">
      <div style="font-family:var(--font-display);font-size:17px;font-style:italic;font-weight:400;line-height:1.6;color:var(--charcoal);">&laquo;Ценности — это не то же самое, что цели. Цель — конкретная, конечная вещь. Когда ты её достигаешь — это конечная точка. Ценности нельзя завершить. Ценности — это то, как ты хочешь жить, каким человеком хочешь быть и за какие принципы готова стоять.&raquo;</div>
      <div style="font-size:13px;font-weight:400;color:var(--terracotta);margin-top:10px;">— Доктор Джулия Смит, «Why Has Nobody Told Me This Before?»</div>
    </div>
    <p class="modal-desc">Когда ты каждый день соединяешься со своими ценностями, дисциплина перестаёт быть насилием — она становится выбором. Напиши свои ценности, свой коммитмент и то, что ты больше не готова терпеть.</p>
    <p class="modal-desc" style="margin-top:8px;margin-bottom:24px;color:var(--terracotta);font-weight:400;">Первые два предложения — самые важные. Именно их ты будешь видеть каждый день при открытии трекера.</p>""",
        f"""    <div class="week2-quote">
      <div class="week2-quote-copy">&laquo;{UNWINDING_ANXIETY_QUOTE}&raquo;</div>
      <div class="week2-quote-meta">— Jud Brewer, <em>Unwinding Anxiety</em></div>
    </div>
    <p class="modal-desc">Во второй неделе мы замечаем тревогу раньше и не даём ей превращаться в мысли, нарративы и автоматические привычки, которые захватывают весь день. Когда мы начинаем работать с тревогой, меняются не только мысли, но и еда, фокус, прокрастинация, скроллинг и отношения с собой.</p>
    <p class="modal-desc" style="margin-top:8px;margin-bottom:24px;color:var(--terracotta);font-weight:500;">Твой личный манифест из недели 1 уже перенесён сюда. Мы только предлагаем его усилить под вторую неделю: добавить, как ты замечаешь тревогу в теле, распознаёшь паттерны и возвращаешь себя в ясность и действие.</p>""",
        1,
    )
    html = html.replace(
        """    <div style="background:var(--cream);border:1px solid var(--sand);border-radius:14px;padding:22px 24px;margin-bottom:24px;">
      <div style="font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--terracotta);margin-bottom:14px;">Пример манифеста</div>

      <div style="font-family:var(--font-display);font-size:17px;font-weight:500;color:var(--charcoal);margin-bottom:6px;">Мои ценности</div>
      <div style="font-family:var(--font-body);font-size:15px;font-weight:300;line-height:1.7;color:var(--warm-gray);margin-bottom:16px;">Жить свою жизнь на максимум во всём. Тело — лучшее из возможных для меня. Энергия максимальная. Ясность и фокус на своих проектах. Качественный отдых. Качественное время с близкими. Я это хочу, я это могу, я это делаю и я буду это делать.</div>

      <div style="font-family:var(--font-display);font-size:17px;font-weight:500;color:var(--charcoal);margin-bottom:6px;">Мой коммитмент</div>
      <div style="font-family:var(--font-body);font-size:15px;font-weight:300;line-height:1.7;color:var(--warm-gray);margin-bottom:16px;">НОЛЬ времени и пространства негативным мыслям, самокритике, страху и сомнениям. Я не отдаю ни капли пространства этим паразитам — от них никакой пользы. Я останавливаю это.<br><br>Я даю внимание своей тревоге как ощущению в теле. Я знаю её природу и истоки. Я чувствую её и сижу с ней, не давая превратиться в мысли и нарративы. Я даю ей место, и она не захватывает меня.</div>

      <div style="font-family:var(--font-display);font-size:17px;font-weight:500;color:var(--charcoal);margin-bottom:6px;">Я знаю своих врагов</div>
      <div style="font-family:var(--font-body);font-size:15px;font-weight:300;line-height:1.7;color:var(--warm-gray);margin-bottom:8px;">Время в телефоне как способ убежать от тревоги и страха, что у меня не получится. Сравнение себя с другими, которое приводит к фрустрации. Расфокус. Выпадение из процессов. Желание убежать и отвлечься. Невозможность остановить работу. Засиживание допоздна — я хочу всё это изменить и я сделаю это.</div>

      <div style="font-family:var(--font-display);font-size:19px;font-style:italic;font-weight:500;color:var(--terracotta);margin-top:14px;">Я могу и делаю!</div>
    </div>
""",
        """    <div style="background:var(--warm-white);border:1px solid rgba(88, 126, 166, 0.18);border-radius:14px;padding:18px 20px;margin-bottom:24px;">
      <div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--terracotta);margin-bottom:10px;">Твой текст уже внутри</div>
      <div style="font-size:15px;line-height:1.65;color:var(--charcoal);">Поле ниже уже заполнено твоим личным манифестом из первой недели. Можешь оставить его как есть или добавить одну-две строки про то, как ты замечаешь тревогу и не позволяешь ей управлять днём.</div>
    </div>
""",
        1,
    )
    html = html.replace(
        '<textarea class="manifesto-textarea" id="manifestoInput" placeholder="Мои ценности: ...&#10;&#10;Мой коммитмент: ...&#10;&#10;Я знаю своих врагов: ..."></textarea>',
        '<textarea class="manifesto-textarea" id="manifestoInput" placeholder="Мои ценности: ...&#10;&#10;Когда тревога поднимается, я сначала замечаю: ...&#10;&#10;Мой коммитмент на неделю 2: ...&#10;&#10;Я не даю тревоге превращаться в: ..."></textarea>',
        1,
    )
    html = html.replace(
        '<button class="manifesto-btn" id="manifestoSave">Начать неделю</button>',
        '<button class="manifesto-btn" id="manifestoSave">Обновить манифест и войти в неделю 2</button>',
        1,
    )
    html = html.replace(
        """.hero-sub {
  font-size: 17px;
  color: var(--warm-gray);
  max-width: 480px;
  margin: 0 auto;
  line-height: 1.65;
}

/* ══════════════════════════════════
   DAY NAV
   ══════════════════════════════════ */""",
        """.hero-sub {
  font-size: 17px;
  color: var(--warm-gray);
  max-width: 480px;
  margin: 0 auto;
  line-height: 1.65;
}

.week-switch {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 26px;
}
.week-switch-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 10px 18px;
  border-radius: 999px;
  border: 1px solid rgba(122, 116, 109, 0.18);
  background: rgba(255, 255, 255, 0.7);
  color: var(--warm-gray);
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.24s ease;
}
.week-switch-btn:hover {
  color: var(--terracotta);
  border-color: rgba(196, 112, 75, 0.34);
}
.week-switch-btn.is-active {
  background: var(--charcoal);
  color: var(--warm-white);
  border-color: var(--charcoal);
}

/* ══════════════════════════════════
   DAY NAV
   ══════════════════════════════════ */""",
        1,
    )
    html = html.replace(
        "Оля Маркес · High Performance · Трекер недели 1 · Апрель 2026",
        f"{name} · High Performance · Трекер недели 2 · Апрель 2026",
        1,
    )
    html = html.replace(
        "    <!-- Day navigation -->",
        f"{build_week_switch_markup(token, 2)}\n\n    <!-- Day navigation -->",
        1,
    )
    html = html.replace(
        """.tracker-subtitle {
  font-size: 14px;
  color: var(--warm-gray);
  line-height: 1.55;
}

/* Input fields inside tracker items */""",
        """.tracker-subtitle {
  font-size: 14px;
  color: var(--warm-gray);
  line-height: 1.55;
}
.tracker-helper-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  color: var(--terracotta);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
}
.tracker-helper-link:hover {
  color: var(--terracotta-light);
}

/* Input fields inside tracker items */""",
        1,
    )
    html = html.replace("'hp_week1_tracker'", f"'hp_week2_tracker_{slug}'", 2)
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
.material-empty-state {
  display: none;
  margin-top: 14px;
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px dashed rgba(122, 116, 109, 0.28);
  background: rgba(255, 253, 249, 0.7);
  color: var(--warm-gray);
  font-size: 14px;
  line-height: 1.6;
}
.material-empty-state.is-visible {
  display: block;
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
  transition: box-shadow 0.32s ease, border-color 0.32s ease, transform 0.32s ease;
}
.generated-story-card[hidden] {
  display: none;
}
.generated-story-card.is-refreshed {
  border-color: rgba(196, 112, 75, 0.55);
  box-shadow: 0 0 0 4px rgba(196, 112, 75, 0.12), 0 16px 36px rgba(58, 54, 50, 0.08);
  transform: translateY(-2px);
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
          <div class="materials-note">Здесь лежат материалы недели 2, плюс привычки, питание и тренировки дня. Их не нужно искать в чате.</div>
          <button class="materials-toggle" id="materialsToggle" type="button" aria-expanded="false" aria-controls="materialsContent">
            <span id="materialsToggleText">Развернуть материалы</span>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="4 10 8 6 12 10"></polyline>
            </svg>
          </button>
        </div>
      </div>
      <div class="materials-collapsed-note" id="materialsCollapsedNote">Материалы недели 2 скрыты. Нажми «Развернуть материалы», чтобы снова увидеть тему недели, питание, привычки и тренировки дня.</div>

      <div class="materials-content" id="materialsContent">
        <p class="materials-intro">Здесь собран слой второй недели: основные материалы про тревогу, прежние PDF по привычкам и питанию и тренировки текущего дня. Персональная часть остаётся ниже по этой же ссылке.</p>

        <div class="materials-grid">
          <article class="material-card">
            <div class="material-kicker">Неделя 2</div>
            <h3>Работа с тревогой</h3>
            <p>Основные материалы недели уже лежат здесь в нужном порядке: сначала зачем работать с тревогой, потом базовая теория и в конце разбор шести видов тревоги.</p>
            <div class="material-resource-list">
              <div class="material-resource">
                <div class="material-resource-head">
                  <div class="material-resource-title">Зачем работать с тревогой</div>
                  <div class="material-resource-type">Материал</div>
                </div>
                <p>Вход в тему недели: как тревога связана с перееданием, прокрастинацией, думскроллингом, бессонницей и выпадением из жизни.</p>
                <div class="material-link-row">
                  <a class="material-btn" href="{ANXIETY_WHY_URL}" target="_blank" rel="noopener noreferrer">Открыть материал</a>
                </div>
              </div>
              <div class="material-resource">
                <div class="material-resource-head">
                  <div class="material-resource-title">12 постов о тревоге</div>
                  <div class="material-resource-type">Материал</div>
                </div>
                <p>Базовая теория недели: собранный цикл постов, чтобы понять механику тревоги, её петли и привычные реакции.</p>
                <div class="material-link-row">
                  <a class="material-btn" href="{ANXIETY_POSTS_URL}" target="_blank" rel="noopener noreferrer">Открыть базовую теорию</a>
                </div>
              </div>
              <div class="material-resource">
                <div class="material-resource-head">
                  <div class="material-resource-title">6 видов тревоги</div>
                  <div class="material-resource-type">Материал</div>
                </div>
                <p>Финальный разбор шести типов тревоги с внутренними монологами, ловушками и практическими разворотами.</p>
                <div class="material-link-row">
                  <a class="material-btn" href="{ANXIETY_TYPES_URL}" target="_blank" rel="noopener noreferrer">Открыть 6 видов тревоги</a>
                </div>
              </div>
            </div>
            <div class="material-meta">Это основной контент недели 2: сначала понять природу тревоги, потом научиться отличать её формы и замечать свои петли привычки.</div>
          </article>

          <article class="material-card">
            <div class="material-kicker">Опоры</div>
            <h3>Привычки и питание</h3>
            <p>Рекомендации по привычкам и питанию остаются прежними. Если захочешь к ним вернуться, они уже лежат в твоей первой неделе.</p>
            <div class="material-actions">
              <a class="material-btn secondary" href="{WEEK1_TRACKER_URL}">Открыть неделю 1</a>
            </div>
            <div class="material-meta">Здесь мы не дублируем большой блок заново, чтобы неделя 2 оставалась компактной и фокус держался на теме тревоги и тренировках дня.</div>
          </article>

          <article class="material-card">
            <div class="material-kicker">Практика</div>
            <h3>Тренировки недели 2</h3>
            <p>Здесь остаются только тренировки текущего дня. Если на день запланированы две тренировки, появятся две отдельные кнопки.</p>
{WORKOUT_DAY_BUTTONS_SHELL}
            <div class="material-meta">В этом блоке больше нет резервных ссылок на PDF или кабинет: только актуальные тренировки дня по текущему расписанию.</div>
          </article>
        </div>

        <div class="duplication-note">
          <strong>Логика доступа:</strong> неделя 2 живёт на отдельной персональной странице, но базовые материалы дублируются здесь специально, чтобы не заставлять участницу прыгать между неделями ради привычек и питания.
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
        '<h1>Неделя <em>2</em></h1>',
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
        """function createTrackerItem(item, index) {
  const el = document.createElement('div');
  el.className = 'tracker-item' + (item.checked ? ' checked' : '');

  let inputHTML = '';
  if (item.hasInput) {
    inputHTML = `<textarea class="tracker-input" placeholder="${item.inputPlaceholder || 'Запиши...'}"
      data-index="${index}" rows="2">${item.inputValue || ''}</textarea>`;
  }

  el.innerHTML = `
    <div class="tracker-check" data-index="${index}">
      <svg viewBox="0 0 16 16"><polyline points="3 8 7 12 13 4"/></svg>
    </div>
    <div class="tracker-body">
      <div class="tracker-top-row">
        <span class="tracker-icon">${item.icon || ''}</span>
        <span class="tracker-title">${item.title}</span>
      </div>
      ${item.subtitle ? `<div class="tracker-subtitle">${item.subtitle}</div>` : ''}
      ${inputHTML}
    </div>
    <div class="tracker-actions">
      <button class="tracker-action-btn edit" title="Редактировать" data-index="${index}">✎</button>
      <button class="tracker-action-btn delete" title="Удалить" data-index="${index}">✕</button>
    </div>
  `;
""",
        f"""function createTrackerItem(item, index) {{
  const el = document.createElement('div');
  el.className = 'tracker-item' + (item.checked ? ' checked' : '');

  let inputHTML = '';
  if (item.hasInput) {{
    inputHTML = `<textarea class="tracker-input" placeholder="${{item.inputPlaceholder || 'Запиши...'}}"
      data-index="${{index}}" rows="2">${{item.inputValue || ''}}</textarea>`;
  }}

  const helperLinkHTML = ['meditation', 'journaling'].includes(item.id)
    ? `<a class="tracker-helper-link" href="{JOURNEY_LINK_URL}" target="_blank" rel="noopener noreferrer">Открыть медитацию и джорналинг ↗</a>`
    : '';

  el.innerHTML = `
    <div class="tracker-check" data-index="${{index}}">
      <svg viewBox="0 0 16 16"><polyline points="3 8 7 12 13 4"/></svg>
    </div>
    <div class="tracker-body">
      <div class="tracker-top-row">
        <span class="tracker-icon">${{item.icon || ''}}</span>
        <span class="tracker-title">${{item.title}}</span>
      </div>
      ${{item.subtitle ? `<div class="tracker-subtitle">${{item.subtitle}}</div>` : ''}}
      ${{helperLinkHTML}}
      ${{inputHTML}}
    </div>
    <div class="tracker-actions">
      <button class="tracker-action-btn edit" title="Редактировать" data-index="${{index}}">✎</button>
      <button class="tracker-action-btn delete" title="Удалить" data-index="${{index}}">✕</button>
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
    renderManifestoBanner();
    return;
  }
  renderManifestoBanner();
}""",
        1,
    )
    html = html.replace(
        """overlay.addEventListener('click', (e) => {
  if (e.target === overlay && state.manifesto) closeManifesto();
});""",
        """overlay.addEventListener('click', (e) => {
  if (e.target === overlay && state.manifesto && !window.__week2ForceManifestoRefresh) closeManifesto();
});""",
        1,
    )
    html = html.replace(
        """  el.querySelector('.tracker-action-btn.delete').addEventListener('click', () => {
    if (confirm('Удалить этот пункт?')) {
      state.days[currentDay].items.splice(index, 1);
      saveState();
      renderDayNav();
      renderDay();
    }
  });""",
        """  el.querySelector('.tracker-action-btn.delete').addEventListener('click', () => {
    if (confirm('Удалить этот пункт?')) {
      const removedItem = state.days[currentDay].items[index];
      state.days[currentDay].items.splice(index, 1);
      syncTrackerTemplateForward(currentDay, { removeItemId: removedItem?.id });
      saveState();
      renderDayNav();
      renderDay();
    }
  });""",
        1,
    )
    html = html.replace(
        """document.getElementById('itemModalSave').addEventListener('click', () => {
  const title = itemTitleInput.value.trim();
  if (!title) return;

  const itemData = {
    id: 'custom_' + Date.now(),
    icon: itemIconInput.value.trim() || '✦',
    title: title,
    subtitle: itemSubtitleInput.value.trim(),
    hasInput: itemHasInput.checked,
    inputPlaceholder: 'Запиши...',
    category: itemCategoryInput.value.trim().toLowerCase() || 'focus',
    checked: false,
    inputValue: ''
  };

  if (editingItemIndex !== null) {
    // Editing — preserve checked state and inputValue
    const existing = state.days[editingDayIndex].items[editingItemIndex];
    itemData.checked = existing.checked;
    itemData.inputValue = existing.inputValue;
    itemData.id = existing.id;
    state.days[editingDayIndex].items[editingItemIndex] = itemData;
  } else {
    // Adding new
    state.days[editingDayIndex].items.push(itemData);
  }

  saveState();
  closeItemModal();
  renderDayNav();
  renderDay();
});""",
        """document.getElementById('itemModalSave').addEventListener('click', () => {
  const title = itemTitleInput.value.trim();
  if (!title) return;

  const itemData = {
    id: 'custom_' + Date.now(),
    icon: itemIconInput.value.trim() || '✦',
    title: title,
    subtitle: itemSubtitleInput.value.trim(),
    hasInput: itemHasInput.checked,
    inputPlaceholder: 'Запиши...',
    category: itemCategoryInput.value.trim().toLowerCase() || 'focus',
    checked: false,
    inputValue: ''
  };

  if (editingItemIndex !== null) {
    // Editing — preserve checked state and inputValue
    const existing = state.days[editingDayIndex].items[editingItemIndex];
    itemData.checked = existing.checked;
    itemData.inputValue = existing.inputValue;
    itemData.id = existing.id;
    state.days[editingDayIndex].items[editingItemIndex] = itemData;
  } else {
    // Adding new
    state.days[editingDayIndex].items.push(itemData);
  }

  syncTrackerTemplateForward(editingDayIndex ?? currentDay, {
    focusItemId: itemData.id
  });
  saveState();
  closeItemModal();
  renderDayNav();
  renderDay();
});""",
        1,
    )
    html = html.replace("{HABITS_PDF}", HABITS_PDF)
    html = html.replace("{NUTRITION_PDF}", NUTRITION_PDF)
    html = html.replace("{ANXIETY_WHY_URL}", ANXIETY_WHY_URL)
    html = html.replace("{ANXIETY_TYPES_URL}", ANXIETY_TYPES_URL)
    html = html.replace("{ANXIETY_POSTS_URL}", ANXIETY_POSTS_URL)
    html = html.replace("{WEEK1_TRACKER_URL}", f"../week_1_trackers_april_2026/w1_{token}.html?{TRACKER_VERSION_QUERY}")
    html = html.replace("{WORKOUT_DAY_BUTTONS_SHELL}", build_workout_day_buttons_shell())
    return html


def build_runtime_script(name: str, slug: str) -> str:
    return f"""
<script>
  const FORM_ENDPOINT = 'https://high-performance-leads.markesbootcamp.workers.dev';
  const LOAD_ENDPOINT = `${{FORM_ENDPOINT}}/participant-week-tracker?slug=${{encodeURIComponent({quote_js(slug)})}}&weekKey=week-2`;
  const WEEK1_LOAD_ENDPOINT = `${{FORM_ENDPOINT}}/participant-week-tracker?slug=${{encodeURIComponent({quote_js(slug)})}}&weekKey=week-1`;
  const PARTICIPANT_NAME = {quote_js(name)};
  const PARTICIPANT_SLUG = {quote_js(slug)};
  const WEEK_KEY = 'week-2';
  const LOCAL_KEY = `hp_week2_tracker_${{PARTICIPANT_SLUG}}`;
  const WEEK1_LOCAL_KEY = `hp_week1_tracker_${{PARTICIPANT_SLUG}}`;
  const LOCAL_UPDATED_AT_KEY = `${{LOCAL_KEY}}:updated-at`;
  const MATERIALS_COLLAPSED_KEY = `${{LOCAL_KEY}}:materials-collapsed`;
  const STORY_PREFERENCES_KEY = `${{LOCAL_KEY}}:story-preferences`;
  const MANIFESTO_REFRESH_SEEN_KEY = `${{LOCAL_KEY}}:manifesto-refresh-seen`;
  const AUTOSAVE_DELAY_MS = 1600;
  const AUTOSAVE_MAX_WAIT_MS = 8000;
  const DAY_WORKOUT_LINKS = {quote_js(DAY_WORKOUT_LINKS)};
  const WEEK2_EXTRA_ITEMS = [
    {{
      id: 'anxietypattern',
      icon: '🌀',
      title: 'Заметила и разобрала хотя бы один паттерн тревоги',
      subtitle: 'Хотя бы один раз увидела, как тревога запускает мысль, привычку или автоматическую реакцию',
      hasInput: false,
      inputPlaceholder: '',
      category: 'mind'
    }}
  ];
  const KNOWN_DEFAULT_ITEM_IDS = [...DEFAULT_ITEMS.map((item) => item.id), ...WEEK2_EXTRA_ITEMS.map((item) => item.id)];
  const STORY_ANGLE_OPTIONS = ['фокус', 'энергия', 'тело', 'дисциплина', 'мягкость', 'смелость', 'радость', 'контакт с собой'];
  let latestPersistedStateJson = '';
  let latestPersistedAt = '';
  let autosaveTimer = null;
  let autosaveInFlight = false;
  let autosaveDirtySince = 0;
  window.__week2ForceManifestoRefresh = false;
  function getWeek2TemplateItems() {{
    return [...DEFAULT_ITEMS, ...WEEK2_EXTRA_ITEMS];
  }}

  function getDefaultDayItems() {{
    return getWeek2TemplateItems().map((item, index) => ({{
      ...item,
      id: item.id + '_' + index,
      checked: false,
      inputValue: ''
    }}));
  }}

  function normalizeTrackerItem(item, fallbackId = '') {{
    const source = item && typeof item === 'object' ? item : {{}};
    const rawId = typeof source.id === 'string' ? source.id.trim() : '';
    const normalizedId = rawId || fallbackId || `item_${{Date.now()}}`;
    return {{
      ...source,
      id: normalizedId,
      icon: typeof source.icon === 'string' ? source.icon : '',
      title: typeof source.title === 'string' ? source.title : '',
      subtitle: typeof source.subtitle === 'string' ? source.subtitle : '',
      hasInput: Boolean(source.hasInput),
      inputPlaceholder: typeof source.inputPlaceholder === 'string' ? source.inputPlaceholder : 'Запиши...',
      category: typeof source.category === 'string' && source.category.trim() ? source.category.trim().toLowerCase() : 'focus',
      checked: Boolean(source.checked),
      inputValue: typeof source.inputValue === 'string' ? source.inputValue : ''
    }};
  }}

  function normalizeDayItems(items, fallbackToDefault = false) {{
    if (!Array.isArray(items) || !items.length) {{
      return fallbackToDefault ? getDefaultDayItems() : [];
    }}

    return items.map((item, index) => normalizeTrackerItem(item, `item_${{index}}`));
  }}

  function cloneItemTemplate(item, index) {{
    const normalizedItem = normalizeTrackerItem(item, `item_${{index}}`);
    return {{
      ...normalizedItem,
      checked: false,
      inputValue: ''
    }};
  }}

  function mergeDayItemsWithTemplate(templateItems, incomingItems) {{
    const normalizedTemplate = normalizeDayItems(templateItems, true);
    const normalizedIncoming = normalizeDayItems(incomingItems);
    const incomingById = new Map(
      normalizedIncoming.map((item) => [canonicalItemId(item.id) || item.id, item])
    );
    return normalizedTemplate.map((item, index) => {{
      const key = canonicalItemId(item.id) || item.id;
      const existing = incomingById.get(key);
      return {{
        ...cloneItemTemplate(item, index),
        checked: Boolean(existing?.checked),
        inputValue: typeof existing?.inputValue === 'string' ? existing.inputValue : ''
      }};
    }});
  }}

  function enrichTemplateWithWeek2Items(templateItems) {{
    const normalizedTemplate = normalizeDayItems(templateItems, true);
    const templateById = new Map(
      normalizedTemplate.map((item) => [canonicalItemId(item.id) || item.id, item])
    );
    const mergedDefaults = getWeek2TemplateItems().map((item, index) => {{
      const defaultItem = normalizeTrackerItem(item, item.id || `item_${{index}}`);
      const key = canonicalItemId(defaultItem.id) || defaultItem.id;
      const existing = templateById.get(key);
      return existing
        ? {{
            ...defaultItem,
            ...existing,
            id: existing.id || defaultItem.id,
          }}
        : defaultItem;
    }});

    const customItems = normalizedTemplate.filter((item) => {{
      const key = canonicalItemId(item.id) || item.id;
      return !KNOWN_DEFAULT_ITEM_IDS.includes(key);
    }});

    return [...mergedDefaults, ...customItems];
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
    const importedTemplateItems = Array.isArray(rawDays[0]?.items) && rawDays[0].items.length
      ? rawDays[0].items
      : baseDays[0].items;
    const templateItems = enrichTemplateWithWeek2Items(importedTemplateItems);
    const normalizedDays = baseDays.map((baseDay, dayIndex) => {{
      const incomingDay = rawDays[dayIndex] && typeof rawDays[dayIndex] === 'object'
        ? rawDays[dayIndex]
        : dayIndex === 0 && rawDays[0] && typeof rawDays[0] === 'object'
          ? rawDays[0]
          : null;

      const normalizedItems = mergeDayItemsWithTemplate(templateItems, incomingDay?.items || []);

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

  function stateSnapshotJson(value = state) {{
    return JSON.stringify(cloneState(value));
  }}

  function rememberPersistedSnapshot(snapshotJson, submittedAt = '') {{
    latestPersistedStateJson = snapshotJson;
    latestPersistedAt = submittedAt || latestPersistedAt || '';
    autosaveDirtySince = 0;
  }}

  function hasUnsyncedServerChanges(snapshotJson = stateSnapshotJson()) {{
    return snapshotJson !== latestPersistedStateJson;
  }}

  function shouldForceManifestoRefresh() {{
    try {{
      return localStorage.getItem(MANIFESTO_REFRESH_SEEN_KEY) !== 'true';
    }} catch (error) {{
      return true;
    }}
  }}

  function markManifestoRefreshSeen() {{
    window.__week2ForceManifestoRefresh = false;
    try {{
      localStorage.setItem(MANIFESTO_REFRESH_SEEN_KEY, 'true');
    }} catch (error) {{
      // Ignore local preference storage failures.
    }}
  }}

  function buildWeek2StateFromWeek1(rawState) {{
    const source = rawState && typeof rawState === 'object' ? rawState : {{}};
    const rawDays = Array.isArray(source.days) ? source.days : [];
    const templateItems = enrichTemplateWithWeek2Items(
      Array.isArray(rawDays[0]?.items) && rawDays[0].items.length ? rawDays[0].items : getWeek2TemplateItems()
    );
    return {{
      manifesto: typeof source.manifesto === 'string' ? source.manifesto : '',
      days: DAY_NAMES.map((name) => ({{
        name,
        items: templateItems.map((item, index) => cloneItemTemplate(item, index))
      }}))
    }};
  }}

  async function loadTrackerRecord(endpoint) {{
    try {{
      const response = await fetch(endpoint);
      if (!response.ok) {{
        throw new Error('load_failed');
      }}
      const result = await response.json();
      if (!result.ok || !result.found || !result.record?.trackerState) {{
        return null;
      }}
      return {{
        trackerState: result.record.trackerState,
        submittedAt: result.record.submittedAt || result.updatedAt || ''
      }};
    }} catch (error) {{
      return null;
    }}
  }}

  function clearAutosaveTimer() {{
    if (autosaveTimer) {{
      window.clearTimeout(autosaveTimer);
      autosaveTimer = null;
    }}
  }}

  function buildTrackerPayload(snapshotState = state, submittedAt = new Date().toISOString()) {{
    return {{
      kind: 'participant-week-tracker',
      participantName: PARTICIPANT_NAME,
      participantSlug: PARTICIPANT_SLUG,
      weekKey: WEEK_KEY,
      trackerState: cloneState(snapshotState),
      pageUrl: window.location.href,
      source: 'high-performance-week-2-tracker',
      submittedAt
    }};
  }}

  async function postTrackerSnapshot(payload, requestOptions = {{}}) {{
    const response = await fetch(FORM_ENDPOINT, {{
      method: 'POST',
      headers: {{
        'Content-Type': 'application/json'
      }},
      body: JSON.stringify(payload),
      keepalive: Boolean(requestOptions.keepalive)
    }});

    if (!response.ok) {{
      throw new Error('save_failed');
    }}

    return response;
  }}

  function queueAutosave(reason = 'change') {{
    clearAutosaveTimer();
    const snapshotJson = stateSnapshotJson();
    if (!hasUnsyncedServerChanges(snapshotJson)) {{
      autosaveDirtySince = 0;
      return;
    }}

    const isRetry = reason.includes('retry');
    if (!autosaveDirtySince || isRetry) {{
      autosaveDirtySince = Date.now();
    }}

    const elapsed = Date.now() - autosaveDirtySince;
    const maxWaitRemaining = Math.max(0, AUTOSAVE_MAX_WAIT_MS - elapsed);
    const delay = isRetry ? AUTOSAVE_DELAY_MS : Math.min(AUTOSAVE_DELAY_MS, maxWaitRemaining);

    autosaveTimer = window.setTimeout(() => {{
      autosaveTimer = null;
      void persistTrackerSnapshotInBackground(reason);
    }}, delay);
  }}

  async function persistTrackerSnapshotInBackground(reason = 'change') {{
    if (autosaveInFlight) {{
      return false;
    }}

    const snapshotJson = stateSnapshotJson();
    if (!hasUnsyncedServerChanges(snapshotJson)) {{
      return false;
    }}

    autosaveInFlight = true;
    const payload = buildTrackerPayload(state);
    setSaveStatus('Черновик сохранён локально. Догружаю серверную версию...');

    try {{
      await postTrackerSnapshot(payload);
      localStorage.setItem(LOCAL_KEY, snapshotJson);
      localStorage.setItem(LOCAL_UPDATED_AT_KEY, payload.submittedAt);
      rememberPersistedSnapshot(snapshotJson, payload.submittedAt);
      const savedText = new Date(payload.submittedAt).toLocaleString('ru-RU');
      setSaveStatus(`Черновик автоматически сохранён ${{savedText}}. По этой ссылке откроется та же версия и в браузере, и в Telegram.`);
      return true;
    }} catch (error) {{
      setSaveStatus('Не удалось автоматически синхронизировать серверную версию. Локальный черновик остался в браузере.');
      return false;
    }} finally {{
      autosaveInFlight = false;
      if (hasUnsyncedServerChanges()) {{
        queueAutosave(reason === 'restore-local' ? 'restore-local-retry' : 'retry');
      }}
    }}
  }}

  function flushPendingTrackerSnapshot() {{
    clearAutosaveTimer();
    if (autosaveInFlight) {{
      return;
    }}

    const snapshotJson = stateSnapshotJson();
    if (!hasUnsyncedServerChanges(snapshotJson)) {{
      return;
    }}

    const payload = buildTrackerPayload(state);
    const body = JSON.stringify(payload);
    let sent = false;

    try {{
      if (navigator.sendBeacon) {{
        sent = navigator.sendBeacon(FORM_ENDPOINT, new Blob([body], {{ type: 'application/json' }}));
      }}
    }} catch (error) {{
      sent = false;
    }}

    if (!sent) {{
      fetch(FORM_ENDPOINT, {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json'
        }},
        body,
        keepalive: true
      }}).catch(() => {{}});
    }}
  }}

  function syncTrackerTemplateForward(startDayIndex = 0, options = {{}}) {{
    const sourceDay = state.days[startDayIndex];
    if (!sourceDay) {{
      return;
    }}

    const templateItems = normalizeDayItems(sourceDay.items, true);
    const removeKey = options.removeItemId ? canonicalItemId(options.removeItemId) || options.removeItemId : '';

    state.days = state.days.map((day, dayIndex) => {{
      if (dayIndex < startDayIndex) {{
        return day;
      }}

      if (dayIndex === startDayIndex) {{
        return {{
          ...day,
          name: DAY_NAMES[dayIndex] || day.name || `День ${{dayIndex + 1}}`,
          items: templateItems.map((item, index) => normalizeTrackerItem(item, item.id || `item_${{index}}`))
        }};
      }}

      const incomingItems = Array.isArray(day?.items) ? day.items : [];
      const filteredIncomingItems = removeKey
        ? incomingItems.filter((item) => (canonicalItemId(item?.id) || item?.id) !== removeKey)
        : incomingItems;

      return {{
        ...day,
        name: DAY_NAMES[dayIndex] || day?.name || `День ${{dayIndex + 1}}`,
        items: mergeDayItemsWithTemplate(templateItems, filteredIncomingItems)
      }};
    }});
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

  function syncStoryPreferencesFromUI() {{
    const preferences = readStoryPreferences();
    const input = document.getElementById('generatedStoryPrompt');
    persistStoryPreferences({{
      ...preferences,
      customPrompt: input ? input.value : preferences.customPrompt
    }});
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

  function storyPromptSignals() {{
    const prompt = readStoryPreferences().customPrompt.trim().toLowerCase();
    return {{
      raw: prompt,
      noSleepPraise: /не говори.*сон|убери.*сон|сон.*неправд|сон.*не хвали/.test(prompt),
      noProgramNarrative: /не говори.*high performance|не говори.*хайпер|не додумывай|не говори.*процесс|убери.*high performance/.test(prompt),
      hardDay: /день был ужасн|ужасный день|день ужасный/.test(prompt)
    }};
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

  function canonicalItemId(value) {{
    const raw = String(value || '').trim();
    if (!raw) {{
      return '';
    }}
    const base = raw.replace(/_\\d+$/, '');
    return KNOWN_DEFAULT_ITEM_IDS.includes(base) ? base : raw;
  }}

  function getDayItemById(day, itemId) {{
    const items = Array.isArray(day?.items) ? day.items : [];
    return items.find((item) => item && canonicalItemId(item.id) === itemId) || null;
  }}

  function getFilledValue(item) {{
    return cropText(item?.inputValue || '', 180);
  }}

  function joinSentences(parts) {{
    return parts.filter(Boolean).join(' ');
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
      return '';
    }}

    const analysisParts = [];
    if (proteinCount >= 2) {{
      analysisParts.push('По записям видно, что в рационе была неплохая опора на белок.');
    }} else if (proteinCount === 1) {{
      analysisParts.push('Белок в рационе был, но опора на него в течение дня пока выглядит не очень устойчивой.');
    }} else {{
      analysisParts.push('По записям рациону, похоже, не хватило явной опоры на белок.');
    }}

    if (fiberCount >= 2) {{
      analysisParts.push('Также в еде уже заметна клетчатка, а это добавляет сытости и устойчивости.');
    }} else if (fiberCount === 0) {{
      analysisParts.push('Овощей, зелени или других источников клетчатки в записях пока немного.');
    }}

    if (checkedMeals <= 1 || (energyCount === 0 && lightCount >= 1)) {{
      analysisParts.push('По общему ощущению день по калориям мог получиться довольно лёгким.');
    }} else if (checkedMeals >= 2 && energyCount >= 1) {{
      analysisParts.push('По энергии день выглядит более собранным: в рационе были не только быстрые решения, но и поддерживающая еда.');
    }}

    return `По еде в записях есть такая картина: ${{joinHumanList(mealSummaries)}}. ${{analysisParts.join(' ')}}`.trim();
  }}

  function getCompletedStandardItems(day) {{
    const items = Array.isArray(day?.items) ? day.items : [];
    return items.filter((item) => item?.checked).map((item) => canonicalItemId(item.id));
  }}

  function buildOpeningParagraph(day, completedIds) {{
    const signals = storyPromptSignals();
    if (signals.hardDay) {{
      return 'День был тяжёлым и местами рваным, но в нём всё равно остались отдельные собранные моменты, на которые можно опереться при разборе.';
    }}
    if (completedIds.length >= 5) {{
      return `Сегодня получился по-настоящему собранный ${{day.name.toLowerCase()}}. В дне было достаточно отмеченных действий, чтобы он ощущался цельным и устойчивым.`;
    }}
    if (completedIds.length >= 3) {{
      return 'Сегодня удалось удержать несколько важных вещей, и это уже делает день более собранным. Даже неидеальный день может держаться на нескольких повторяемых действиях.';
    }}
    if (completedIds.length >= 1) {{
      return 'Сегодня в дне было немного отмеченных пунктов, но они всё равно задают ему структуру и помогают видеть, за что день держался.';
    }}
    return 'Сегодня день больше про наблюдение, чем про выполнение. Это тоже полезный материал: по нему легче увидеть реальный ритм дня и понять, что стоит укрепить дальше.';
  }}

  function buildDaySummaryParagraph(day, completedIds) {{
    const phrases = {{
      sleep: 'дала себе опору по сну',
      meditation: 'начала день с медитации',
      workout: 'сделала тренировку',
      breakfast: 'собрала себе нормальный завтрак',
      lunch: 'не пропустила обед',
      dinner: 'собрала ужин',
      reading: 'вернула себе внимание через чтение',
      journaling: 'оставила место для джорналинга',
      hardstop: 'поставила рамку работе',
      qualitytime: 'побыла с близкими по-настоящему',
      bedtime: 'подумала о завтрашнем дне уже сегодня'
    }};
    const completed = completedIds.map((id) => phrases[id]).filter(Boolean).slice(0, 5);
    const workoutNote = getFilledValue(getDayItemById(day, 'workout'));
    const journalNote = getFilledValue(getDayItemById(day, 'journaling'));

    const parts = [];
    if (completed.length) {{
      parts.push(`В течение дня были отмечены такие вещи: ${{joinHumanList(completed)}}.`);
    }}
    if (workoutNote) {{
      parts.push(`Из заметок особенно выделяется тренировка: ${{workoutNote}}`);
    }} else if (journalNote) {{
      parts.push(`Из заметок дня сохранилась такая деталь: ${{journalNote}}`);
    }}

    return parts.join(' ');
  }}

  function buildSleepParagraph(day) {{
    const sleepItem = getDayItemById(day, 'sleep');
    const bedtimeItem = getDayItemById(day, 'bedtime');
    const sleepNote = getFilledValue(sleepItem);
    const signals = storyPromptSignals();

    if (!sleepItem && !bedtimeItem) {{
      return '';
    }}
    if (sleepNote) {{
      return `По сну в заметках зафиксировано следующее: ${{sleepNote}}. Это помогает увидеть реальную картину дня и заметить, где сейчас особенно нужна опора.`;
    }}
    if (sleepItem?.checked && !signals.noSleepPraise) {{
      return 'Сон сегодня был одной из заметных опор дня. Такая база обычно помогает держать и энергию, и фокус, и более ровный ритм.';
    }}
    if (bedtimeItem?.checked) {{
      return 'По сну ещё есть куда расти, но вечерняя рамка уже намечена, и это хороший шаг в сторону более бережного ритма.';
    }}
    return '';
  }}

  function buildWinsParagraph(day, completedIds) {{
    const signals = storyPromptSignals();
    const wins = [];
    const winMap = {{
      sleep: signals.noSleepPraise ? '' : 'сон всё-таки был отмечен в трекере',
      meditation: 'дала себе момент тишины и настройки',
      workout: 'выбрала движение и тело',
      breakfast: 'не оставила утро без еды',
      lunch: 'поддержала себя обедом',
      dinner: 'завершила день с заботой о себе',
      reading: 'вернула себе внимание',
      journaling: 'оставила место для себя',
      hardstop: 'поставила границу работе',
      qualitytime: 'сохранила живое присутствие рядом с близкими',
      bedtime: 'подумала о завтрашнем себе'
    }};
    completedIds.forEach((id) => {{
      const phrase = winMap[id];
      if (phrase && wins.length < 3) {{
        wins.push(phrase);
      }}
    }});
    if (!wins.length) {{
      const journalNote = getFilledValue(getDayItemById(day, 'journaling'));
      return journalNote
        ? `Из ценного в этом дне точно осталось вот это наблюдение: ${{journalNote}}`
        : '';
    }}
    return `Из удачных моментов дня можно отметить вот это: ${{joinHumanList(wins)}}.`;
  }}

  function buildProgramLensParagraph(completedIds) {{
    const signals = storyPromptSignals();
    if (signals.noProgramNarrative) {{
      return '';
    }}
    if (completedIds.length >= 1) {{
      return 'Через такую оптику и работает High Performance: первая неделя здесь не про идеальность, а про базу. Шаг за шагом собираются тело, питание, ритм, внимание и ощущение большей опоры внутри дня.';
    }}
    return 'Даже такой день остаётся частью процесса High Performance. Здесь важнее не идеальная картинка, а честная фиксация реальности и постепенная сборка базы, на которой потом держится всё остальное.';
  }}

  function buildStoryFromCurrentDay() {{
    const preferences = readStoryPreferences();
    const day = state.days[currentDay] || {{ name: `День ${{currentDay + 1}}`, items: [] }};
    const completedIds = getCompletedStandardItems(day);
    const opening = buildOpeningParagraph(day, completedIds);
    const dayFlow = buildDaySummaryParagraph(day, completedIds);
    const sleep = buildSleepParagraph(day);
    const nutrition = buildNutritionParagraph(day);
    const wins = buildWinsParagraph(day, completedIds);
    const programLens = buildProgramLensParagraph(completedIds);
    const manifesto = `И я слышу, как это связано с моим манифестом: «${{manifestoSpark()}}». Когда я выбираю даже маленькие действия в его сторону, мои ценности перестают быть красивыми словами и становятся тем, как я реально проживаю день.`;
    const angleFocus = buildAngleFocusParagraph(preferences.angles);
    const closing = completedIds.length >= 4
      ? 'Итог дня: в нём уже есть заметный каркас, на который можно опираться дальше.'
      : 'Итог дня: даже небольшое количество отмеченных пунктов уже помогает увидеть структуру и направление движения.';

    return [opening, dayFlow, sleep, nutrition, wins, programLens, manifesto, angleFocus, closing].filter(Boolean).join('\\n\\n');
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

  function flashGeneratedStoryCard() {{
    const card = document.getElementById('generatedStoryCard');
    if (!card || card.hidden) {{
      return;
    }}
    card.classList.remove('is-refreshed');
    void card.offsetWidth;
    card.classList.add('is-refreshed');
    window.setTimeout(() => {{
      card.classList.remove('is-refreshed');
    }}, 1400);
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
    const emptyState = document.getElementById('workoutEmptyState');
    if (!container) {{
      return;
    }}

    const links = Array.isArray(DAY_WORKOUT_LINKS[currentDay]) ? DAY_WORKOUT_LINKS[currentDay] : [];
    if (!links.length) {{
      container.innerHTML = '';
      emptyState?.classList.add('is-visible');
      return;
    }}

    emptyState?.classList.remove('is-visible');
    container.innerHTML = links.map((link, index) => `
      <a class="material-btn${{index === 0 ? '' : ' secondary'}}" href="${{link.url}}" target="_blank" rel="noopener noreferrer">${{link.label}}</a>
    `).join('');
  }}

  function syncManifestoVisibility() {{
    const forceRefresh = shouldForceManifestoRefresh();
    window.__week2ForceManifestoRefresh = forceRefresh;
    if (manifestoInput) {{
      manifestoInput.value = state.manifesto || '';
    }}
    renderManifestoBanner();

    if (!state.manifesto || forceRefresh) {{
      window.setTimeout(() => {{
        if (!state.manifesto || shouldForceManifestoRefresh()) {{
          overlay.classList.add('active');
        }}
      }}, forceRefresh ? 180 : 600);
      return;
    }}

    overlay.classList.remove('active');
  }}

  async function importWeek1StateIfNeeded() {{
    const hasLocalWeek2 = (() => {{
      try {{
        return Boolean(localStorage.getItem(LOCAL_KEY));
      }} catch (error) {{
        return false;
      }}
    }})();

    if (hasLocalWeek2 || latestPersistedStateJson) {{
      return false;
    }}

    const week1ServerRecord = await loadTrackerRecord(WEEK1_LOAD_ENDPOINT);
    let week1State = week1ServerRecord?.trackerState || null;

    if (!week1State) {{
      try {{
        const savedWeek1 = localStorage.getItem(WEEK1_LOCAL_KEY);
        week1State = savedWeek1 ? JSON.parse(savedWeek1) : null;
      }} catch (error) {{
        week1State = null;
      }}
    }}

    if (!week1State) {{
      return false;
    }}

    state = buildWeek2StateFromWeek1(week1State);
    currentDay = 0;
    const snapshotJson = stateSnapshotJson();
    try {{
      localStorage.setItem(LOCAL_KEY, snapshotJson);
      localStorage.setItem(LOCAL_UPDATED_AT_KEY, new Date().toISOString());
      localStorage.removeItem(MANIFESTO_REFRESH_SEEN_KEY);
    }} catch (error) {{
      // Ignore local storage failures and continue with in-memory state.
    }}
    setSaveStatus('Перенесла манифест и персональные пункты из недели 1. Перед стартом обнови манифест под тему тревоги.');
    queueAutosave('import-week1');
    return true;
  }}

  function saveState() {{
    try {{
      localStorage.setItem(LOCAL_KEY, JSON.stringify(state));
      localStorage.setItem(LOCAL_UPDATED_AT_KEY, new Date().toISOString());
      setSaveStatus('Черновик сохранён в этом браузере. Синхронизирую серверную версию...');
      queueAutosave();
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
      const localUpdatedAt = localStorage.getItem(LOCAL_UPDATED_AT_KEY) || '';
      if (latestPersistedAt && localUpdatedAt && localUpdatedAt <= latestPersistedAt) {{
        return false;
      }}

      state = normalizeTrackerState(JSON.parse(saved));
      currentDay = 0;
      renderManifestoBanner();
      renderWorkoutMaterialButtons();
      renderDayNav();
      renderDay();
      syncManifestoVisibility();
      setSaveStatus('Восстановлен локальный черновик из этого браузера. Сейчас догружу его на сервер.');
      queueAutosave('restore-local');
      return true;
    }} catch (error) {{
      localStorage.removeItem(LOCAL_KEY);
      localStorage.removeItem(LOCAL_UPDATED_AT_KEY);
      return false;
    }}
  }}

  async function loadSavedTracker() {{
    setSaveStatus('Загружаю сохранённую версию трекера...');
    try {{
      const record = await loadTrackerRecord(LOAD_ENDPOINT);
      if (!record?.trackerState) {{
        setSaveStatus('Пока нет сохранённой версии. Можно заполнить трекер и сохранить его по этой же ссылке.');
        return false;
      }}

      state = normalizeTrackerState(record.trackerState);
      currentDay = 0;
      const snapshotJson = stateSnapshotJson();
      const savedAt = record.submittedAt || '';
      rememberPersistedSnapshot(snapshotJson, savedAt);
      renderManifestoBanner();
      renderWorkoutMaterialButtons();
      renderDayNav();
      renderDay();
      syncManifestoVisibility();

      const savedText = savedAt ? new Date(savedAt).toLocaleString('ru-RU') : '';
      setSaveStatus(savedText ? `Открыта сохранённая версия от ${{savedText}}.` : 'Открыта последняя сохранённая версия трекера.');
      return true;
    }} catch (error) {{
      setSaveStatus('Не удалось загрузить сохранённую версию. Можно продолжить с локальным черновиком.');
      return false;
    }}
  }}

  async function persistTrackerSnapshot(triggerButton, pendingStatus = 'Сохраняю трекер...') {{
    clearAutosaveTimer();
    const snapshotJson = stateSnapshotJson();
    const payload = buildTrackerPayload(state);
    const saveButton = document.getElementById('saveTrackerBtn');
    const storyButton = document.getElementById('generateStoryBtn');
    setButtonBusy(saveButton, true, 'Сохраняю...');
    setButtonBusy(storyButton, true, 'Собираю...');
    setSaveStatus(pendingStatus);

    try {{
      await postTrackerSnapshot(payload);
      localStorage.setItem(LOCAL_KEY, snapshotJson);
      localStorage.setItem(LOCAL_UPDATED_AT_KEY, payload.submittedAt);
      rememberPersistedSnapshot(snapshotJson, payload.submittedAt);
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

  function applyStoryPreferences() {{
    syncStoryPreferencesFromUI();
    renderGeneratedStory(buildStoryFromCurrentDay());
    flashGeneratedStoryCard();
    setSaveStatus('Рассказ пересобран с новыми акцентами.');
  }}

  document.getElementById('saveTrackerBtn')?.addEventListener('click', saveTrackerToServer);
  document.getElementById('generateStoryBtn')?.addEventListener('click', generateStoryFlow);
  document.getElementById('copyGeneratedStoryBtn')?.addEventListener('click', copyGeneratedStory);
  document.getElementById('regenerateStoryBtn')?.addEventListener('click', () => toggleStoryControls());
  document.getElementById('applyStoryPreferencesBtn')?.addEventListener('click', applyStoryPreferences);
  document.getElementById('manifestoSave')?.addEventListener('click', () => {{
    markManifestoRefreshSeen();
    setSaveStatus('Манифест обновлён под вторую неделю. Теперь тревогу можно замечать раньше и не отдавать ей весь день.');
  }});
  document.getElementById('generatedStoryPrompt')?.addEventListener('input', (event) => {{
    const preferences = readStoryPreferences();
    persistStoryPreferences({{
      ...preferences,
      customPrompt: event.target.value
    }});
  }});
  window.addEventListener('pagehide', flushPendingTrackerSnapshot);
  document.addEventListener('visibilitychange', () => {{
    if (document.visibilityState === 'hidden') {{
      flushPendingTrackerSnapshot();
    }}
  }});

  const materialsShell = document.getElementById('materialsShell');
  const materialsToggle = document.getElementById('materialsToggle');
  const materialsToggleText = document.getElementById('materialsToggleText');

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

  (async () => {{
    applyMaterialsCollapsedState(readMaterialsCollapsedState());
    state = normalizeTrackerState(state);
    currentDay = 0;
    const loadedWeek2 = await loadSavedTracker();
    const restoredLocal = restoreLocalState();
    if (!loadedWeek2 && !restoredLocal) {{
      await importWeek1StateIfNeeded();
    }}
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
    html = add_personalization(template, participant["public_name"], participant["for_name"], slug, participant["token"])
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
  <title>HIGH PERFORMANCE — Private Week 2 Trackers</title>
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
    <h1>Private <em>Week 2 Trackers</em></h1>
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
            <span class="card-meta">трекер недели 2 · {entry['telegram_handle']}</span>
          </a>"""
        for entry in entries
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>HIGH PERFORMANCE — Week 2 Team Access</title>
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
      <h1>Week 2 <em>Team Access</em></h1>
      <p class="hero-sub">Командная страница со всеми персональными трекерами второй недели. Эту ссылку не пересылаем участницам.</p>
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
    tracker_url = f"{PUBLIC_BASE_URL}/w2_{participant['token']}.html?{TRACKER_VERSION_QUERY}"
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
        f"Внутри уже есть материалы недели 2, продублированные опоры по питанию и привычкам и сам трекер второй недели. "
        f"Новые тренировки можно будет добавить в этот же экран позже, без смены ссылки.\n\n"
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
    participants = get_week1_tracker_participants()

    for old_file in OUTPUT_DIR.glob("w2_*.html"):
        old_file.unlink()
    for stale_name in ("links.txt", "telegram_message.txt"):
        stale_file = OUTPUT_DIR / stale_name
        if stale_file.exists():
            stale_file.unlink()
    for old_team_page in OUTPUT_DIR.glob("week2-team-*.html"):
        old_team_page.unlink()

    entries = []
    for participant in participants:
        slug = participant["slug"]
        filename = f"w2_{participant['token']}.html"
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
    print(f"Generated {len(entries)} week 2 trackers in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
