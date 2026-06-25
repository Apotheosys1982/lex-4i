from __future__ import annotations

from .ingest import all_missing_items
from .models import ChronologyEvent, EvidenceItem, MatterDocument, LEGAL_ADVICE_BOUNDARY


def build_missing_info_checklist(documents: list[MatterDocument], events: list[ChronologyEvent]) -> list[str]:
    items = [entry["item"] for entry in all_missing_items(documents)]
    for event in events:
        if event.support_status in {"partially supported", "missing support", "conflicting information", "inferred event"}:
            items.append(f"Review support for {event.event_id}: {event.description}")
    return sorted(set(items))


def render_missing_info_checklist(items: list[str]) -> str:
    lines = ["# Missing Information Checklist", "", f"> {LEGAL_ADVICE_BOUNDARY}", ""]
    lines.append("Resolve these gaps before relying on the matter framing or draft language.")
    lines.append("")
    for item in items:
        lines.append(f"- [ ] {item}")
    lines.append("")
    return "\n".join(lines)


def render_drafting_support_packet(
    events: list[ChronologyEvent],
    evidence_items: list[EvidenceItem],
    missing_items: list[str],
) -> str:
    supported = [event for event in events if event.support_status == "supported"]
    needs_review = [event for event in events if event.support_status != "supported"]
    exhibits = [item for item in evidence_items if item.source_type in {"evidence", "correspondence"}]

    lines = ["# Drafting Support Packet", "", f"> {LEGAL_ADVICE_BOUNDARY}", ""]
    lines.append("This packet organizes drafting material. It is not a final draft and does not provide legal advice.")
    lines.append("")
    lines.append("## Known Source-Backed Facts")
    for event in supported:
        lines.append(f"- {event.date}: {event.description} ({event.source_file})")
    lines.append("")
    lines.append("## Facts Needing Verification")
    for event in needs_review:
        lines.append(f"- {event.event_id}: {event.description} [{event.support_status}]")
    lines.append("")
    lines.append("## Possible Document Sections")
    lines.extend(
        [
            "- Background and assignment timeline",
            "- Timekeeping concern chronology",
            "- Warning and termination chronology",
            "- Evidence and exhibit list",
            "- Gaps requiring review",
            "- Requested records or next-step review",
        ]
    )
    lines.append("")
    lines.append("## Source-Backed Assertions")
    for event in supported:
        lines.append(f"- Supported by {event.source_file}: {event.description}")
    lines.append("")
    lines.append("## Unsupported / High-Risk Assertions")
    for event in needs_review:
        lines.append(f"- Do not state without review: {event.description}")
    for item in missing_items:
        lines.append(f"- Missing source gap: {item}")
    lines.append("")
    lines.append("## Suggested Exhibits / Attachments")
    for item in exhibits:
        lines.append(f"- {item.evidence_id}: {item.file_name}")
    lines.append("")
    lines.append("## Tone Notes")
    lines.extend(
        [
            "- Avoid legal conclusions unless reviewed by qualified counsel.",
            "- Avoid precise damages figures unless supported by calculation records.",
            "- Separate documented facts from disputed recollections.",
            "- Request missing records rather than asserting unsupported facts as final.",
        ]
    )
    lines.append("")
    lines.append("## Human Review Checklist")
    lines.extend(
        [
            "- [ ] Confirm jurisdiction and deadlines.",
            "- [ ] Confirm policy version and record completeness.",
            "- [ ] Confirm payroll and system-log support.",
            "- [ ] Confirm witness reliability and exact statements.",
            "- [ ] Confirm whether any draft should be sent.",
        ]
    )
    lines.append("")
    return "\n".join(lines)

