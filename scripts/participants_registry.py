from __future__ import annotations

from collections import Counter
import re


RAW_PARTICIPANTS = [
    {"name": "Оля Маркес", "public_name": "Оля", "contact": "@OlyMarkes", "source": "manual", "token": "q7k2m9b4v8x3"},
    {"name": "Даша Простова", "public_name": "Даша", "contact": "@beloved_dasha", "source": "manual", "token": "n4r8t2y6p1c5"},
    {"name": "Яна Федорова", "public_name": "Яна", "contact": "@yanabraun", "source": "manual", "token": "h8m3q5z7k2w9"},
    {"name": "Лера", "public_name": "Лера", "contact": "@lerakurepina", "issue": 26, "token": "d6v9n3k7t2m8"},
    {"name": "Аня", "public_name": "Аня", "contact": "@beregukukuhu", "issue": 25, "token": "a7c2r9m4x6p3"},
    {"name": "Viktoria", "public_name": "Вика", "contact": "@vpasko", "issue": 23, "token": "p3t8m6k1z9w4"},
    {"name": "Вера", "public_name": "Вера", "contact": "@verushkavera", "issue": 22, "token": "u5n2c8r4x7p1"},
    {"name": "Валерия", "public_name": "Валерия", "contact": "@Valeriia_Tu", "issue": 21, "token": "j4m9v2k6t8q3"},
    {"name": "Olesya Dauptain", "public_name": "Олеся", "contact": "@aramba_annecy", "issue": 20, "token": "y7p3n8k5c2m6"},
    {"name": "Надежда", "public_name": "Надежда", "contact": "@moroznb", "issue": 18, "token": "b9t4m7q2x5k8"},
    {"name": "Наташа", "public_name": "Наташа", "contact": "@Natasha_SHWD", "issue": 17, "token": "r6k2v9p4m8c1", "paid": False, "active": False},
    {"name": "Ksu Matusevich", "public_name": "Ксю", "contact": "@ksumatu", "issue": 16, "token": "s8m3x7q1k5v9"},
    {"name": "Юля Карасик", "public_name": "Юля", "contact": "@karasichka", "issue": 14, "token": "e4p7t2m9c6k3", "paid": False, "active": False},
    {"name": "Жанар", "public_name": "Жанар", "contact": "@zhantik87", "issue": 13, "token": "w9k5m2r8x3p6"},
    {"name": "Анна", "public_name": "Анна", "contact": "@Jayms17", "issue": 12, "token": "f2v8m4q7k1t5"},
    {"name": "Вика", "public_name": "Вика", "contact": "@vikaevdokimova", "issue": 11, "token": "g7m1p6x9c3k4"},
    {"name": "Наташа", "public_name": "Наташа", "contact": "@nathaliedanz", "issue": 10, "token": "l5q9t3m7v2k8", "paid": False, "active": False},
    {"name": "Катя", "public_name": "Катя", "contact": "@Ekaterina_Novopashina", "issue": 8, "token": "c3k8p5m1x7t4"},
    {"name": "Екатерина Прозорова", "public_name": "Екатерина", "contact": "@katia_paints", "issue": 6, "token": "z2m7v4k9p6c1"},
    {"name": "Таня", "public_name": "Таня", "contact": "@Tatiana_Apakhova", "issue": 33, "token": "m6p4t8k2v7q1"},
    {"name": "Алена Замесина", "public_name": "Алена", "contact": "@alenazamesina", "issue": 56, "token": "n7v3k8p2m5q4", "paid": True, "active": False},
    {"name": "Севара", "public_name": "Севара", "contact": "@sevaragreene", "issue": 38, "token": "r4m8t2q6v1k9", "paid": True},
    {"name": "Лена", "public_name": "Лена", "contact": "@barkovaquality", "issue": 35, "token": "c8p2m6v4k9t1", "paid": False, "active": False},
    {"name": "Полина Рэйтблат", "public_name": "Полина", "contact": "@paulina_raitblat", "issue": 34, "token": "y5k2m8q4v7p1", "paid": False},
    {"name": "Наташа", "public_name": "Наташа", "contact": "@natalytoomany", "issue": 28, "token": "h4v7m2k9p5q8", "paid": False},
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


def extract_public_name(raw: dict[str, str]) -> str:
    explicit = str(raw.get("public_name", "")).strip()
    if explicit:
        return explicit
    return str(raw["name"]).strip().split()[0]


def build_for_name(public_name: str) -> str:
    explicit_overrides = {
        "Ксю": "Ксю",
    }
    if public_name in explicit_overrides:
        return explicit_overrides[public_name]

    lowered = public_name.lower()
    if len(public_name) >= 2 and lowered.endswith("ия"):
        return public_name[:-2] + "ии"
    if lowered.endswith("я"):
        return public_name[:-1] + "и"
    if lowered.endswith("а"):
        if len(public_name) >= 2 and public_name[-2].lower() in {"г", "к", "х", "ж", "ч", "ш", "щ"}:
            return public_name[:-1] + "и"
        return public_name[:-1] + "ы"
    if lowered.endswith("ь"):
        return public_name[:-1] + "и"
    return public_name


def get_participants() -> list[dict[str, str]]:
    participants: list[dict[str, str]] = []
    used_slugs: set[str] = set()
    duplicate_names = Counter(extract_public_name(item) for item in RAW_PARTICIPANTS)

    for raw in RAW_PARTICIPANTS:
        if raw.get("active", True) is False:
            continue
        base_slug = slugify(raw["name"])
        contact_slug = slugify(raw["contact"].replace("@", ""))
        slug = base_slug if base_slug not in used_slugs else f"{base_slug}-{contact_slug}"
        used_slugs.add(slug)

        public_name = extract_public_name(raw)
        for_name = str(raw.get("for_name", "")).strip() or build_for_name(public_name)
        display_name = public_name
        if duplicate_names[public_name] > 1:
            display_name = public_name

        participants.append(
            {
                **raw,
                "full_name": raw["name"],
                "public_name": public_name,
                "for_name": for_name,
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
