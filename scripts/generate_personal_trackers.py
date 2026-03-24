from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "tracker_april_2026_v1.html"
OUTPUT_DIR = ROOT / "trackers_april_2026"
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/trackers_april_2026"


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
    {"name": "нина", "contact": "@1028305", "issue": 4},
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


def personalize_html(template: str, name: str, contact: str, slug: str, issue: int) -> str:
    title = f"Трекер дня 1–7 апреля 2026 — {name}"
    hero_tag = f"1–7 апреля 2026 • {name}"
    hero_copy = (
        f"Персональный трекер недели для {name} ({contact}). "
        "Отмечай ежедневные ритуалы, вписывай свои задачи и держи фокус "
        "на том, что реально двигает тебя вперёд."
    )
    footer_copy = (
        f"Базовые привычки уже добавлены для {name}: медитация, тренировка, чтение книги, "
        "хардстоп работы в 19:00, отказ от экрана после 20:00, вовремя лечь спать, "
        "план дня и джорналинг 10 минут."
    )

    html = template
    html = html.replace(
        "<title>Трекер дня 1–7 апреля 2026</title>",
        f"<title>{title}</title>",
        1,
    )
    html = html.replace(
        '<div class="hero-tag">1–7 апреля 2026</div>',
        f'<div class="hero-tag">{hero_tag}</div>',
        1,
    )
    html = html.replace(
        """      <p>
        Неделя мягкой дисциплины: отмечай ежедневные ритуалы, вписывай свои задачи и держи фокус
        на том, что реально двигает тебя вперёд.
      </p>""",
        f"      <p>{hero_copy}</p>",
        1,
    )
    html = html.replace(
        """    <p class="footer-note">
      Базовые привычки уже добавлены: медитация, тренировка, чтение книги, хардстоп работы в 19:00,
      отказ от экрана после 20:00, вовремя лечь спать, план дня и джорналинг 10 минут.
    </p>""",
        f'    <p class="footer-note">{footer_copy}</p>',
        1,
    )
    html = html.replace(
        'const STORAGE_KEY = "high-performance-tracker-april-2026-v1";',
        f'const STORAGE_KEY = "high-performance-tracker-april-2026-v1-{slug}";',
        1,
    )

    source_comment = (
        f"<!-- Generated for {name} ({contact}) from GitHub issue #{issue}: "
        f"https://github.com/OLYMARKES/high-performance-leads/issues/{issue} -->\n"
    )
    return source_comment + html


def build_index(entries: list[dict[str, str]]) -> str:
    cards = []
    for entry in entries:
      cards.append(
          f"""
          <a class="card" href="{entry['filename']}">
            <span class="card-name">{entry['name']}</span>
            <span class="card-meta">{entry['contact']}</span>
            <span class="card-meta">issue #{entry['issue']}</span>
          </a>"""
      )

    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Именные трекеры — апрель 2026</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Nunito+Sans:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --cream: #fbf7f2;
      --warm-white: rgba(255, 253, 249, 0.86);
      --terracotta: #c8744d;
      --charcoal: #3d3834;
      --warm-gray: #8a8278;
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
        radial-gradient(circle at top left, rgba(216, 141, 109, 0.12), transparent 36%),
        radial-gradient(circle at bottom right, rgba(239, 229, 216, 0.72), transparent 34%),
        linear-gradient(180deg, #fcf9f5 0%, #f9f4ed 100%);
      color: var(--charcoal);
      font-family: var(--font-body);
      padding: 36px 18px 56px;
    }}

    .page {{
      max-width: 1180px;
      margin: 0 auto;
    }}

    .hero {{
      text-align: center;
      padding: 28px 0 34px;
    }}

    .hero-tag {{
      display: inline-flex;
      padding: 14px 28px;
      border: 1px solid rgba(200, 116, 77, 0.24);
      border-radius: 999px;
      color: var(--terracotta);
      letter-spacing: 0.26em;
      text-transform: uppercase;
      font-size: 0.9rem;
      background: rgba(255, 253, 249, 0.48);
    }}

    h1 {{
      margin-top: 28px;
      font-family: var(--font-display);
      font-size: clamp(4rem, 8vw, 6.4rem);
      font-weight: 400;
      line-height: 0.94;
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

    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }}

    .card {{
      display: block;
      text-decoration: none;
      border: 1px solid var(--line);
      border-radius: 26px;
      padding: 22px 20px;
      background: var(--warm-white);
      box-shadow: var(--shadow);
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

    @media (max-width: 920px) {{
      .grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
    }}

    @media (max-width: 640px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="hero-tag">апрель 2026 • именные трекеры</div>
      <h1>High <span>Performance</span></h1>
      <p>
        Здесь собраны персональные трекеры для участниц coworking-а.
        Тестовые заявки убраны, дубли схлопнуты до одного человека.
      </p>
    </section>
    <section class="grid">
{cards_html}
    </section>
  </main>
</body>
</html>
"""


def build_links_text(entries: list[dict[str, str]]) -> str:
    lines = ["High Performance trackers", ""]
    for entry in entries:
        lines.append(f"{entry['name']} ({entry['contact']}): {PUBLIC_BASE_URL}/{entry['filename']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    entries = []
    used_slugs = set()

    for participant in PARTICIPANTS:
        base_slug = slugify(participant["name"])
        contact_slug = slugify(participant["contact"].replace("@", ""))
        slug = base_slug

        if slug in used_slugs:
            slug = f"{base_slug}-{contact_slug}"

        used_slugs.add(slug)

        filename = f"tracker_{slug}_april_2026_v1.html"
        html = personalize_html(
            template=template,
            name=participant["name"],
            contact=participant["contact"],
            slug=slug,
            issue=participant["issue"],
        )
        (OUTPUT_DIR / filename).write_text(html, encoding="utf-8")
        entries.append(
            {
                "name": participant["name"],
                "contact": participant["contact"],
                "issue": str(participant["issue"]),
                "filename": filename,
            }
        )

    index_html = build_index(entries)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    (OUTPUT_DIR / "links.txt").write_text(build_links_text(entries), encoding="utf-8")
    print(f"Generated {len(entries)} trackers in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
