from __future__ import annotations

import argparse
from pathlib import Path

from .chronology import chronology_payload, extract_events
from .draft_support import build_missing_info_checklist, render_drafting_support_packet, render_missing_info_checklist
from .evidence_index import build_evidence_index, evidence_payload
from .ingest import load_documents, matter_id
from .issue_map import build_issue_map, issue_payload
from .receipts import build_receipt, write_receipt
from .redteam import render_red_team_review, render_unsupported_claims, review_draft
from .renderers import render_chronology, render_evidence_index, render_issue_map, write_json
from .validators import (
    validate_boundary_docs,
    validate_generated_outputs,
    validate_sample_matter,
    validation_status,
)


def run(matter_folder: Path, output_folder: Path) -> int:
    project_root = Path(__file__).resolve().parents[1]
    matter_folder = matter_folder.resolve()
    output_folder.mkdir(parents=True, exist_ok=True)

    preflight_errors = validate_sample_matter(matter_folder) + validate_boundary_docs(project_root)
    documents = load_documents(matter_folder)
    matter = matter_id(documents)
    events = extract_events(documents)
    evidence_items = build_evidence_index(documents, events)
    issues = build_issue_map(documents, events)
    missing_items = build_missing_info_checklist(documents, events)
    draft_path = matter_folder / "drafts" / "draft_demand_letter.md"
    red_team_report = review_draft(draft_path, matter)

    outputs: list[str] = []

    def write_text(relative: str, text: str) -> None:
        (output_folder / relative).write_text(text, encoding="utf-8")
        outputs.append(relative)

    def write_payload(relative: str, payload: dict) -> None:
        write_json(output_folder / relative, payload)
        outputs.append(relative)

    write_payload("chronology.json", chronology_payload(matter, events))
    write_text("chronology.md", render_chronology(events))
    write_payload("evidence_index.json", evidence_payload(matter, evidence_items))
    write_text("evidence_index.md", render_evidence_index(evidence_items))
    write_payload("issue_map.json", issue_payload(matter, issues))
    write_text("issue_map.md", render_issue_map(issues))
    write_text("missing_info_checklist.md", render_missing_info_checklist(missing_items))
    write_text("drafting_support_packet.md", render_drafting_support_packet(events, evidence_items, missing_items))
    write_payload("red_team_report.json", red_team_report)
    write_text("red_team_review.md", render_red_team_review(red_team_report))
    write_text("unsupported_claims_report.md", render_unsupported_claims(red_team_report))

    receipt = build_receipt(
        matter_id=matter,
        input_folder=matter_folder,
        output_folder=output_folder.resolve(),
        documents=documents,
        outputs_generated=outputs + ["matter_receipt.json", "matter_receipt.md"],
        chronology_event_count=len(events),
        evidence_item_count=len(evidence_items),
        issue_category_count=len(issues),
        unsupported_claim_count=len(red_team_report["unsupported_claims"]),
        missing_info_item_count=len(missing_items),
        validation_status="pending",
        validation_errors=preflight_errors,
    )
    write_receipt(output_folder, receipt)

    validation_errors = preflight_errors + validate_generated_outputs(output_folder)
    receipt = build_receipt(
        matter_id=matter,
        input_folder=matter_folder,
        output_folder=output_folder.resolve(),
        documents=documents,
        outputs_generated=outputs + ["matter_receipt.json", "matter_receipt.md"],
        chronology_event_count=len(events),
        evidence_item_count=len(evidence_items),
        issue_category_count=len(issues),
        unsupported_claim_count=len(red_team_report["unsupported_claims"]),
        missing_info_item_count=len(missing_items),
        validation_status=validation_status(validation_errors),
        validation_errors=validation_errors,
    )
    write_receipt(output_folder, receipt)

    print(f"matter_id={matter}")
    print(f"output_folder={output_folder.resolve()}")
    print(f"validation_status={receipt['validation_status']}")
    if validation_errors:
        for error in validation_errors:
            print(f"validation_error={error}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lex 4i legal-operations workflow harness CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run the full Lex 4i matter workflow pipeline")
    run_parser.add_argument("matter_folder", type=Path)
    run_parser.add_argument("--out", required=True, type=Path, help="Output folder")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        return run(args.matter_folder, args.out)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
