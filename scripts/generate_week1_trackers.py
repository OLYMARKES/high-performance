from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "week_1_trackers_april_2026"
SOURCE_TEMPLATE_PATH = Path("/Users/olymarkes/Documents/Claude/Projects/High perfomance/week-1-tracker.html")
PUBLIC_BASE_URL = "https://olymarkes.github.io/high-performance/week_1_trackers_april_2026"
TEAM_PAGE_TOKEN = "week1-vault-t8m4q2c7k9p5"


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


def add_personalization(template: str, name: str, slug: str) -> str:
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
        f'<p class="hero-sub">Персональный трекер первой недели для {name}. Заполняй манифест, отмечай ежедневные шаги и сохраняй прогресс по этой же ссылке.</p>',
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
        """/* ── Save panel ── */
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

/* ── Footer ── */""",
        1,
    )
    html = html.replace(
        "@media (max-width: 600px) {\n  .hero { min-height: 36vh; }",
        """@media (max-width: 600px) {
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
      state = JSON.parse(saved);
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

      state = result.record.trackerState;
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

  (async () => {{
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
    html = add_personalization(template, participant["name"], slug)
    html = html.replace("</body>\n</html>", f"{build_runtime_script(participant['name'], slug)}\n</body>\n</html>", 1)
    if participant.get("issue"):
        source_comment = (
            f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['name']} "
            f"from GitHub issue #{participant['issue']}: https://github.com/OLYMARKES/high-performance-leads/issues/{participant['issue']} -->\n"
        )
    else:
        source_comment = f"<!-- Generated from {SOURCE_TEMPLATE_PATH} for {participant['name']} from manual roster update -->\n"
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
          <a class="card" href="{entry['filename']}">
            <span class="card-name">{entry['name']}</span>
            <span class="card-meta">трекер недели 1</span>
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


def main() -> None:
    template = SOURCE_TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old_file in OUTPUT_DIR.glob("w1_*.html"):
        old_file.unlink()
    for stale_name in ("links.txt", "telegram_message.txt"):
        stale_file = OUTPUT_DIR / stale_name
        if stale_file.exists():
            stale_file.unlink()
    for old_team_page in OUTPUT_DIR.glob("week1-team-*.html"):
        old_team_page.unlink()

    entries = []
    used_slugs = set()
    for participant in PARTICIPANTS:
        base_slug = slugify(participant["name"])
        contact_slug = slugify(participant["contact"].replace("@", ""))
        slug = base_slug if base_slug not in used_slugs else f"{base_slug}-{contact_slug}"
        used_slugs.add(slug)

        filename = f"w1_{participant['token']}.html"
        page_html = build_participant_page(template, {**participant, "slug": slug})
        (OUTPUT_DIR / filename).write_text(page_html, encoding="utf-8")
        entries.append({"name": participant["name"], "filename": filename})

    (OUTPUT_DIR / "index.html").write_text(build_index_page(), encoding="utf-8")
    (OUTPUT_DIR / f"{TEAM_PAGE_TOKEN}.html").write_text(build_team_page(entries), encoding="utf-8")
    print(f"Generated {len(entries)} week 1 trackers in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
