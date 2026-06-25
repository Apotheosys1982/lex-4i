from __future__ import annotations

import json
from pathlib import Path

from .models import ChronologyEvent, EvidenceItem, LEGAL_ADVICE_BOUNDARY


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def md_header(title: str) -> str:
    return f"# {title}\n\n> {LEGAL_ADVICE_BOUNDARY}\n\n"


def render_chronology(events: list[ChronologyEvent]) -> str:
    lines = [md_header("Evidence Chronology")]
    lines.append("| Event ID | Date | Actor | Event | Source | Support | Confidence | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for event in events:
        lines.append(
            f"| {event.event_id} | {event.date} | {event.actor} | {event.description} | "
            f"{event.source_file} | {event.support_status} | {event.confidence} | {event.notes} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_evidence_index(items: list[EvidenceItem]) -> str:
    lines = [md_header("Evidence Index")]
    lines.append("| Evidence ID | File | Type | Date | Summary | Linked Events | Issue Categories | Hash |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for item in items:
        lines.append(
            f"| {item.evidence_id} | {item.file_name} | {item.source_type} | {item.date} | "
            f"{item.summary} | {', '.join(item.linked_chronology_events) or 'none'} | "
            f"{', '.join(item.linked_issue_categories) or 'none'} | `{item.hash[:16]}...` |"
        )
    lines.append("")
    return "\n".join(lines)


def render_issue_map(issues: list[dict]) -> str:
    lines = [md_header("Issue / Risk Map")]
    lines.append("These are issue/risk signals for review. They are not legal conclusions.\n")
    for issue in issues:
        lines.append(f"## {issue['category']}")
        lines.append(f"- Review priority: {issue['review_priority']}")
        lines.append(f"- Human review required: {issue['human_review_required']}")
        lines.append(f"- Related events: {', '.join(issue['related_events']) or 'none'}")
        lines.append(f"- Sources: {', '.join(issue['supporting_source_references']) or 'none'}")
        if issue["missing_information"]:
            lines.append("- Missing information:")
            for item in issue["missing_information"]:
                lines.append(f"  - {item}")
        lines.append(f"- Review note: {issue.get('review_note', '')}")
        lines.append("")
    return "\n".join(lines)

