from __future__ import annotations

from .ingest import first_field
from .models import EvidenceItem, MatterDocument, ChronologyEvent, LEGAL_ADVICE_BOUNDARY


def _summary_for(document: MatterDocument) -> str:
    if "summary" in document.fields:
        return document.fields["summary"][0]
    for line in document.text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and ":" not in stripped:
            return stripped[:220]
    return "No summary marker provided."


def build_evidence_index(documents: list[MatterDocument], events: list[ChronologyEvent]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for index, document in enumerate(documents, start=1):
        linked_events = [event.event_id for event in events if event.source_file == document.relative_path]
        issue_categories = sorted(
            {
                tag
                for event in events
                if event.source_file == document.relative_path
                for tag in event.issue_tags
            }
        )
        date = first_field(document, "date", first_field(document, "event_date", "unknown"))
        actor = first_field(document, "actor", first_field(document, "from", first_field(document, "organization", "unknown")))
        items.append(
            EvidenceItem(
                evidence_id=f"EVD-{index:03d}",
                file_name=document.relative_path,
                source_type=document.source_type,
                date=date,
                actor_or_source=actor,
                summary=_summary_for(document),
                linked_chronology_events=linked_events,
                linked_issue_categories=issue_categories,
                hash=document.sha256,
                review_notes="Human review required before relying on this source for legal significance.",
            )
        )
    return items


def evidence_payload(matter_id: str, items: list[EvidenceItem]) -> dict:
    return {
        "matter_id": matter_id,
        "legal_advice_boundary": LEGAL_ADVICE_BOUNDARY,
        "evidence_items": [item.to_dict() for item in items],
    }

