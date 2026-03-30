from __future__ import annotations

from pathlib import Path

from participants_registry import get_participants


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "trackers_april_2026"
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/trackers_april_2026"
WEEK1_TRACKER_BASE_URL = "https://olymarkes.github.io/high-performance/week_1_trackers_april_2026"
TRACKER_VERSION_QUERY = "v=materials-pdf-v18"


def build_redirect_page(name: str, token: str, issue: int | None) -> str:
    destination = f"{WEEK1_TRACKER_BASE_URL}/w1_{token}.html?{TRACKER_VERSION_QUERY}"
    if issue:
        source_comment = (
            f"<!-- Redirect stub for {name} from GitHub issue #{issue}: "
            f"https://github.com/OLYMARKES/high-performance-leads/issues/{issue} -->\n"
        )
    else:
        source_comment = f"<!-- Redirect stub for {name} from manual roster update -->\n"

    return source_comment + f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <meta http-equiv="refresh" content="0; url={destination}">
  <title>Перенаправление...</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
      background: #fbf7f2;
      color: #3d3834;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .card {{
      max-width: 560px;
      text-align: center;
      background: rgba(255, 253, 249, 0.92);
      border: 1px solid rgba(200, 116, 77, 0.16);
      border-radius: 24px;
      padding: 32px 28px;
    }}
    a {{
      color: #c8744d;
    }}
  </style>
  <script>
    window.location.replace({destination!r});
  </script>
</head>
<body>
  <div class="card">
    <p>Старый трекер больше не используется.</p>
    <p>Открываю правильный трекер с манифестом для {name}.</p>
    <p><a href="{destination}">Перейти вручную</a></p>
  </div>
</body>
</html>
"""


def build_index(entries: list[dict[str, str]]) -> str:
    cards = []
    for entry in entries:
        cards.append(
            f"""
          <a class="card" href="{entry['filename']}">
            <span class="card-name">{entry['display_name']}</span>
            <span class="card-meta">редирект на правильный трекер с манифестом</span>
          </a>"""
        )

    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>Именные трекеры — redirect</title>
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
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }}
    .card {{
      display: block;
      text-decoration: none;
      border: 1px solid rgba(200, 116, 77, 0.16);
      border-radius: 26px;
      padding: 22px 20px;
      background: rgba(255, 253, 249, 0.86);
      color: inherit;
    }}
    .card-name {{ display: block; font-size: 24px; }}
    .card-meta {{ display: block; margin-top: 8px; color: #8a8278; font-size: 14px; }}
    @media (max-width: 920px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    @media (max-width: 640px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <h1>Старые трекеры</h1>
      <p>Эта директория сохранена только для совместимости. Все ссылки ниже перенаправляют на правильные week 1 trackers с манифестом.</p>
    </section>
    <section class="grid">
{cards_html}
    </section>
  </main>
</body>
</html>
"""


def build_links_text(entries: list[dict[str, str]]) -> str:
    lines = ["High Performance trackers (redirects)", ""]
    for entry in entries:
        lines.append(f"{entry['display_name']}: {PUBLIC_BASE_URL}/{entry['filename']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old_file in OUTPUT_DIR.glob("tracker_*_april_2026_v1.html"):
        old_file.unlink()

    entries = []

    for participant in get_participants():
        slug = participant["slug"]
        filename = f"tracker_{slug}_april_2026_v1.html"
        html = build_redirect_page(
            name=participant["public_name"],
            token=participant["token"],
            issue=participant.get("issue"),
        )
        (OUTPUT_DIR / filename).write_text(html, encoding="utf-8")
        entries.append(
            {
                "name": participant["public_name"],
                "display_name": participant["display_name"],
                "issue": str(participant.get("issue", "")),
                "filename": filename,
            }
        )

    (OUTPUT_DIR / "index.html").write_text(build_index(entries), encoding="utf-8")
    (OUTPUT_DIR / "links.txt").write_text(build_links_text(entries), encoding="utf-8")
    print(f"Generated {len(entries)} redirect trackers in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
