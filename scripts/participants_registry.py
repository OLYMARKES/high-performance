from __future__ import annotations

from collections import Counter
import re


RAW_PARTICIPANTS = [
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


def get_participants() -> list[dict[str, str]]:
    participants: list[dict[str, str]] = []
    used_slugs: set[str] = set()
    duplicate_names = Counter(item["name"] for item in RAW_PARTICIPANTS)

    for raw in RAW_PARTICIPANTS:
        base_slug = slugify(raw["name"])
        contact_slug = slugify(raw["contact"].replace("@", ""))
        slug = base_slug if base_slug not in used_slugs else f"{base_slug}-{contact_slug}"
        used_slugs.add(slug)

        display_name = raw["name"]
        if duplicate_names[raw["name"]] > 1:
            display_name = f"{raw['name']} ({raw['contact']})"

        participants.append(
            {
                **raw,
                "slug": slug,
                "display_name": display_name,
                "telegram_handle": raw["contact"],
                "lead_issue": raw.get("issue"),
                "paid": bool(raw.get("paid", True)),
                "course_opened": bool(raw.get("course_opened", False)),
                "opened_course": raw.get("opened_course", ""),
            }
        )

    return participants
