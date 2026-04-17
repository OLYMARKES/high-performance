from __future__ import annotations

from pathlib import Path

from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
SOURCE_TEMPLATE_PATH = ROOT / "week-4-tracker.html"
OUTPUT_DIR = ROOT / "week_4_trackers_april_2026"
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/week_4_trackers_april_2026"
TRACKER_VERSION_QUERY = "v=week4-rollout-v1"
TEAM_PAGE_TOKEN = "week4-vault-x6m3q9p2k7t4"
CHAT_URL = "https://t.me/+UQzb3a_ohdliMTEy"
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


def get_week4_tracker_participants() -> list[dict[str, str]]:
    return [*get_participants(), *CURATOR_TRACKER_PARTICIPANTS]


def build_week_switch_markup(token: str) -> str:
    return f"""    <nav class="week-switch reveal" aria-label="Переключение недели">
      <a class="week-switch-btn" href="../week_1_trackers_april_2026/w1_{token}.html?{TRACKER_VERSION_QUERY}">Неделя 1</a>
      <a class="week-switch-btn" href="../week_2_trackers_april_2026/w2_{token}.html?{TRACKER_VERSION_QUERY}">Неделя 2</a>
      <a class="week-switch-btn" href="../week_3_trackers_april_2026/w3_{token}.html?{TRACKER_VERSION_QUERY}">Неделя 3</a>
      <a class="week-switch-btn is-active" href="../week_4_trackers_april_2026/w4_{token}.html?{TRACKER_VERSION_QUERY}">Неделя 4</a>
    </nav>"""


def add_personalization(template: str, participant: dict[str, str]) -> str:
    name = participant["public_name"]
    for_name = participant["for_name"]
    slug = participant["slug"]
    token = participant["token"]

    html = template
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots" content="noindex, nofollow, noarchive">',
        1,
    )
    html = html.replace("<title>Трекер недели 4 — High Performance</title>", f"<title>Трекер недели 4 — {name}</title>", 1)
    html = html.replace(
        '<div class="hero-tag">High Performance · Трекер · Апрель 2026</div>',
        f'<div class="hero-tag">High Performance · {name} · Неделя 4</div>',
        1,
    )
    html = html.replace(
        '<p class="hero-sub">Благодарность как противоядие от обесценивания. Одна практика на всю неделю — намаливание того, что уже есть.</p>',
        f'<p class="hero-sub">Персональный трекер четвёртой недели для {for_name}. Здесь собраны материал недели, тренировка дня, недельная практика и ежедневный трекер с автосохранением.</p>',
        1,
    )
    html = html.replace(
        """.hero-sub {
  font-size: 17px;
  color: var(--warm-gray);
  max-width: 520px;
  margin: 0 auto;
  line-height: 1.65;
}

/* ══════════════════════════════════
   DAY NAV""",
        """.hero-sub {
  font-size: 17px;
  color: var(--warm-gray);
  max-width: 620px;
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
   DAY NAV""",
        1,
    )
    html = html.replace(
        '    <!-- Materials section -->',
        f"{build_week_switch_markup(token)}\n\n    <!-- Materials section -->",
        1,
    )
    html = html.replace('href="week-4.html" target="_blank"', 'href="../week-4.html" target="_blank" rel="noopener"', 1)
    html = html.replace(
        "Оля Маркес · High Performance · Трекер недели 4 · Апрель 2026",
        f"{name} · High Performance · Трекер недели 4 · Апрель 2026",
        1,
    )
    html = html.replace("'hp_week4_tracker'", f"'hp_week4_tracker_{slug}'")
    return html


def build_participant_page(template: str, participant: dict[str, str]) -> str:
    html = add_personalization(template, participant)
    issue = participant.get("issue")
    if issue:
        source_comment = (
            f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['public_name']} "
            f"from GitHub issue #{issue}: https://github.com/OLYMARKES/high-performance-leads/issues/{issue} -->\n"
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
  <title>HIGH PERFORMANCE — Private Week 4 Trackers</title>
  <style>
    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      background: #fbf7f2;
      color: #3d3834;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .card {
      width: min(720px, 100%);
      background: rgba(255, 253, 249, 0.92);
      border: 1px solid rgba(200, 116, 77, 0.16);
      border-radius: 24px;
      padding: 32px 28px;
      text-align: center;
    }
    a { color: #c8744d; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Private Week 4 Trackers</h1>
    <p>Эта директория не показывает общий список участниц. Открывать трекер нужно по личной или командной ссылке.</p>
  </div>
</body>
</html>
"""


def build_team_page(entries: list[dict[str, str]]) -> str:
    cards_html = "\n".join(
        f"""          <a class="card" href="{entry['filename']}?{TRACKER_VERSION_QUERY}">
            <span class="card-name">{entry['name']}</span>
            <span class="card-meta">{entry['telegram_handle']}</span>
          </a>"""
        for entry in entries
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>Week 4 Team Access</title>
  <style>
    body {{
      min-height: 100vh;
      margin: 0;
      padding: 36px 18px 56px;
      background: linear-gradient(180deg, #fcf9f5 0%, #f9f4ed 100%);
      color: #3d3834;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .page {{ max-width: 1180px; margin: 0 auto; }}
    .hero {{ text-align: center; padding: 28px 0 34px; }}
    .panel {{
      background: rgba(255, 253, 249, 0.86);
      border: 1px solid rgba(200, 116, 77, 0.16);
      border-radius: 24px;
      padding: 24px 22px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }}
    .card {{
      display: block;
      text-decoration: none;
      border: 1px solid rgba(200, 116, 77, 0.16);
      border-radius: 24px;
      padding: 22px 20px;
      background: rgba(255, 253, 249, 0.92);
      color: inherit;
    }}
    .card-name {{ display: block; font-size: 24px; }}
    .card-meta {{ display: block; margin-top: 8px; color: #8a8278; font-size: 14px; }}
    @media (max-width: 920px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    @media (max-width: 640px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class="page">
    <div class="hero">
      <h1>Week 4 Team Access</h1>
      <p>Командная страница со всеми персональными трекерами четвёртой недели. Эту ссылку не пересылаем участницам.</p>
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


def build_telegram_messages(participants: list[dict[str, str]]) -> str:
    blocks = []
    for participant in participants:
        tracker_url = f"{PUBLIC_BASE_URL}/w4_{participant['token']}.html?{TRACKER_VERSION_QUERY}"
        blocks.append(
            f"=== {participant['display_name']} · {participant['telegram_handle']} ===\n"
            f"Привет, {participant['public_name']}!\n\n"
            f"Открываю тебе трекер недели 4:\n{tracker_url}\n\n"
            f"Внутри уже есть материал недели, тренировка дня, недельная практика и персональный трекер с автосохранением.\n\n"
            f"Чат программы:\n{CHAT_URL}\n"
        )
    return "\n\n" + ("\n\n" + ("-" * 72) + "\n\n").join(blocks) + "\n"


def main() -> None:
    template = SOURCE_TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    participants = get_week4_tracker_participants()

    for old_file in OUTPUT_DIR.glob("w4_*.html"):
        old_file.unlink()
    for stale_name in ("telegram_message.txt",):
        stale_file = OUTPUT_DIR / stale_name
        if stale_file.exists():
            stale_file.unlink()
    for old_team_page in OUTPUT_DIR.glob("week4-vault-*.html"):
        old_team_page.unlink()

    entries = []
    for participant in participants:
        filename = f"w4_{participant['token']}.html"
        page_html = build_participant_page(template, participant)
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
    print(f"Generated {len(entries)} week 4 trackers in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
