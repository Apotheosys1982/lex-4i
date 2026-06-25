from __future__ import annotations

from .models import ChronologyEvent, MatterDocument, LEGAL_ADVICE_BOUNDARY


def _split_tags(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def extract_events(documents: list[MatterDocument]) -> list[ChronologyEvent]:
    raw_events: list[dict[str, str | list[str]]] = []
    for document in documents:
        current: dict[str, str | list[str]] | None = None
        for line in document.text.splitlines():
            stripped = line.strip()
            if stripped.startswith("Event-Date:"):
                if current:
                    raw_events.append(current)
                current = {
                    "date": stripped.split(":", 1)[1].strip(),
                    "source_file": document.relative_path,
                    "source_excerpt_or_reference": document.relative_path,
                }
                continue
            if current is None:
                continue
            if stripped.startswith("Actor:"):
                current["actor"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("Event:"):
                current["description"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("Support:"):
                current["support_status"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("Issue-Tags:"):
                current["issue_tags"] = _split_tags(stripped.split(":", 1)[1].strip())
            elif stripped.startswith("Confidence:"):
                current["confidence"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("Notes:"):
                current["notes"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("Excerpt:"):
                current["source_excerpt_or_reference"] = stripped.split(":", 1)[1].strip().strip('"')
        if current:
            raw_events.append(current)

    raw_events.sort(key=lambda event: (str(event.get("date", "")), str(event.get("source_file", ""))))
    events: list[ChronologyEvent] = []
    for index, raw in enumerate(raw_events, start=1):
        events.append(
            ChronologyEvent(
                event_id=f"CHR-{index:03d}",
                date=str(raw.get("date", "unknown")),
                actor=str(raw.get("actor", "unknown")),
                description=str(raw.get("description", "")),
                source_file=str(raw.get("source_file", "")),
                source_excerpt_or_reference=str(raw.get("source_excerpt_or_reference", "")),
                support_status=str(raw.get("support_status", "missing support")),
                confidence=str(raw.get("confidence", "unknown")),
                issue_tags=list(raw.get("issue_tags", [])),
                notes=str(raw.get("notes", "")),
            )
        )
    return events


def chronology_payload(matter_id: str, events: list[ChronologyEvent]) -> dict:
    return {
        "matter_id": matter_id,
        "legal_advice_boundary": LEGAL_ADVICE_BOUNDARY,
        "events": [event.to_dict() for event in events],
    }

