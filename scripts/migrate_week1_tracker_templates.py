from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone

from participants_registry import get_participants


BASE_URL = "https://high-performance-leads.markesbootcamp.workers.dev"
TRACKER_BASE_URL = "https://olymarkes.github.io/high-performance/week_1_trackers_april_2026"
TRACKER_VERSION_QUERY = "v=materials-pdf-v29"
REQUEST_ORIGIN = "https://olymarkes.github.io"
DAY_NAMES = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def canonical_item_id(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    return re.sub(r"_\d+$", "", raw)


def normalize_item(item: object, index: int) -> dict[str, object]:
    source = item if isinstance(item, dict) else {}
    raw_id = str(source.get("id") or "").strip()
    normalized_id = raw_id or f"item_{index}"
    category = str(source.get("category") or "focus").strip().lower() or "focus"

    return {
        **source,
        "id": normalized_id,
        "icon": source.get("icon") if isinstance(source.get("icon"), str) else "",
        "title": source.get("title") if isinstance(source.get("title"), str) else "",
        "subtitle": source.get("subtitle") if isinstance(source.get("subtitle"), str) else "",
        "hasInput": bool(source.get("hasInput")),
        "inputPlaceholder": source.get("inputPlaceholder")
        if isinstance(source.get("inputPlaceholder"), str)
        else "Запиши...",
        "category": category,
        "checked": bool(source.get("checked")),
        "inputValue": source.get("inputValue") if isinstance(source.get("inputValue"), str) else "",
    }


def normalize_day_items(items: object) -> list[dict[str, object]]:
    if not isinstance(items, list) or not items:
        return []
    return [normalize_item(item, index) for index, item in enumerate(items)]


def clone_item_template(item: object, index: int) -> dict[str, object]:
    normalized = normalize_item(item, index)
    normalized["checked"] = False
    normalized["inputValue"] = ""
    return normalized


def merge_day_items(template_items: object, incoming_items: object) -> list[dict[str, object]]:
    normalized_template = normalize_day_items(template_items)
    normalized_incoming = normalize_day_items(incoming_items)
    incoming_by_id = {
        canonical_item_id(str(item.get("id") or "")) or str(item.get("id") or ""): item
        for item in normalized_incoming
    }

    merged_items: list[dict[str, object]] = []
    for index, item in enumerate(normalized_template):
        key = canonical_item_id(str(item.get("id") or "")) or str(item.get("id") or "")
        existing = incoming_by_id.get(key, {})
        merged_items.append(
            {
                **clone_item_template(item, index),
                "checked": bool(existing.get("checked")),
                "inputValue": existing.get("inputValue") if isinstance(existing.get("inputValue"), str) else "",
            }
        )
    return merged_items


def normalize_tracker_state(raw_state: object) -> dict[str, object] | None:
    if not isinstance(raw_state, dict):
        return None

    raw_days = raw_state.get("days") if isinstance(raw_state.get("days"), list) else []
    first_day = raw_days[0] if raw_days and isinstance(raw_days[0], dict) else {}
    template_items = first_day.get("items") if isinstance(first_day.get("items"), list) else []
    if not template_items:
        return None

    normalized_days: list[dict[str, object]] = []
    for index, day_name in enumerate(DAY_NAMES):
        incoming_day = raw_days[index] if index < len(raw_days) and isinstance(raw_days[index], dict) else {}
        incoming_items = incoming_day.get("items") if isinstance(incoming_day.get("items"), list) else []
        normalized_days.append(
            {
                **incoming_day,
                "name": day_name,
                "items": merge_day_items(template_items, incoming_items),
            }
        )

    return {
        **raw_state,
        "manifesto": raw_state.get("manifesto") if isinstance(raw_state.get("manifesto"), str) else "",
        "days": normalized_days,
    }


def fetch_json(url: str) -> dict[str, object]:
    result = subprocess.run(
        [
            "curl",
            "-fsS",
            "-H",
            f"Origin: {REQUEST_ORIGIN}",
            url,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def post_json(url: str, payload: dict[str, object]) -> dict[str, object]:
    result = subprocess.run(
        [
            "curl",
            "-fsS",
            "-X",
            "POST",
            "-H",
            "Content-Type: application/json",
            "-H",
            f"Origin: {REQUEST_ORIGIN}",
            "--data-binary",
            json.dumps(payload, ensure_ascii=False),
            url,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    updated: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []

    for participant in get_participants():
        slug = participant["slug"]
        token = participant["token"]
        load_url = f"{BASE_URL}/participant-week-tracker?slug={slug}&weekKey=week-1"

        try:
            payload = fetch_json(load_url)
        except subprocess.CalledProcessError as exc:
            errors.append(f"{slug}: load failed (exit {exc.returncode})")
            continue
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{slug}: load failed ({exc})")
            continue

        if not payload.get("ok") or not payload.get("found") or not isinstance(payload.get("record"), dict):
            skipped.append(f"{slug}: not found")
            continue

        record = payload["record"]
        tracker_state = record.get("trackerState")
        normalized_state = normalize_tracker_state(tracker_state)
        if normalized_state is None:
            skipped.append(f"{slug}: no day-1 template")
            continue

        before = json.dumps(tracker_state, ensure_ascii=False, sort_keys=True)
        after = json.dumps(normalized_state, ensure_ascii=False, sort_keys=True)
        if before == after:
            skipped.append(f"{slug}: already aligned")
            continue

        save_payload = {
            "kind": "participant-week-tracker",
            "participantName": record.get("participantName") or participant["public_name"],
            "participantSlug": slug,
            "weekKey": record.get("weekKey") or "week-1",
            "trackerState": normalized_state,
            "pageUrl": f"{TRACKER_BASE_URL}/w1_{token}.html?{TRACKER_VERSION_QUERY}",
            "source": "high-performance-week-1-migration",
            "submittedAt": datetime.now(timezone.utc).isoformat(),
        }

        try:
            result = post_json(BASE_URL, save_payload)
        except subprocess.CalledProcessError as exc:
            errors.append(f"{slug}: save failed (exit {exc.returncode})")
            continue
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{slug}: save failed ({exc})")
            continue

        if not result.get("ok"):
            errors.append(f"{slug}: save returned not ok")
            continue

        updated.append(slug)

    print(
        json.dumps(
            {
                "updated": updated,
                "skipped": skipped,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
