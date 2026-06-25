from __future__ import annotations

from collections import defaultdict

from .ingest import all_missing_items
from .models import ChronologyEvent, MatterDocument, LEGAL_ADVICE_BOUNDARY


HIGH_PRIORITY_SIGNALS = {
    "retaliation signal",
    "wage/hour signal",
    "discrimination signal",
    "harassment signal",
    "deadline/procedure concern",
}


def build_issue_map(documents: list[MatterDocument], events: list[ChronologyEvent]) -> list[dict]:
    grouped: dict[str, dict] = {}
    missing_items = all_missing_items(documents)
    missing_by_source = defaultdict(list)
    for item in missing_items:
        missing_by_source[item["source_file"]].append(item["item"])

    for event in events:
        for tag in event.issue_tags:
            issue = grouped.setdefault(
                tag,
                {
                    "category": tag,
                    "related_events": [],
                    "supporting_source_references": [],
                    "missing_information": [],
                    "review_priority": "high" if tag in HIGH_PRIORITY_SIGNALS else "medium",
                    "human_review_required": True,
                    "review_note": "This is an issue/risk signal for qualified human/legal review, not a legal conclusion.",
                },
            )
            issue["related_events"].append(event.event_id)
            if event.source_file not in issue["supporting_source_references"]:
                issue["supporting_source_references"].append(event.source_file)
            for missing in missing_by_source.get(event.source_file, []):
                if missing not in issue["missing_information"]:
                    issue["missing_information"].append(missing)

    for item in missing_items:
        issue = grouped.setdefault(
            "documentation gap",
            {
                "category": "documentation gap",
                "related_events": [],
                "supporting_source_references": [],
                "missing_information": [],
                "review_priority": "medium",
                "human_review_required": True,
                "review_note": "Missing source material should be resolved before relying on the draft or issue framing.",
            },
        )
        if item["source_file"] not in issue["supporting_source_references"]:
            issue["supporting_source_references"].append(item["source_file"])
        if item["item"] not in issue["missing_information"]:
            issue["missing_information"].append(item["item"])

    return sorted(grouped.values(), key=lambda issue: issue["category"])


def issue_payload(matter_id: str, issues: list[dict]) -> dict:
    return {
        "matter_id": matter_id,
        "legal_advice_boundary": LEGAL_ADVICE_BOUNDARY,
        "issues": issues,
    }

