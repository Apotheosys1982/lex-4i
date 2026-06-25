from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


LEGAL_ADVICE_BOUNDARY = (
    "This artifact is not legal advice and does not replace attorney judgment. "
    "It organizes matter materials for qualified human/legal review."
)

SYNTHETIC_NOTE = "This is synthetic sample data for demonstration purposes only."


@dataclass(frozen=True)
class MatterDocument:
    path: Path
    relative_path: str
    text: str
    source_type: str
    sha256: str
    fields: dict[str, list[str]]


@dataclass(frozen=True)
class ChronologyEvent:
    event_id: str
    date: str
    actor: str
    description: str
    source_file: str
    source_excerpt_or_reference: str
    support_status: str
    confidence: str
    issue_tags: list[str]
    notes: str

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "date": self.date,
            "actor": self.actor,
            "description": self.description,
            "source_file": self.source_file,
            "source_excerpt_or_reference": self.source_excerpt_or_reference,
            "support_status": self.support_status,
            "confidence": self.confidence,
            "issue_tags": self.issue_tags,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    file_name: str
    source_type: str
    date: str
    actor_or_source: str
    summary: str
    linked_chronology_events: list[str]
    linked_issue_categories: list[str]
    hash: str
    review_notes: str

    def to_dict(self) -> dict:
        return {
            "evidence_id": self.evidence_id,
            "file_name": self.file_name,
            "source_type": self.source_type,
            "date": self.date,
            "actor_or_source": self.actor_or_source,
            "summary": self.summary,
            "linked_chronology_events": self.linked_chronology_events,
            "linked_issue_categories": self.linked_issue_categories,
            "hash": self.hash,
            "review_notes": self.review_notes,
        }

