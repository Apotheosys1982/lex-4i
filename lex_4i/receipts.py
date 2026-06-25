from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .models import LEGAL_ADVICE_BOUNDARY, MatterDocument
from .renderers import write_json


def build_receipt(
    matter_id: str,
    input_folder: Path,
    output_folder: Path,
    documents: list[MatterDocument],
    outputs_generated: list[str],
    chronology_event_count: int,
    evidence_item_count: int,
    issue_category_count: int,
    unsupported_claim_count: int,
    missing_info_item_count: int,
    validation_status: str,
    validation_errors: list[str],
) -> dict:
    return {
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "matter_id": matter_id,
        "input_folder": input_folder.as_posix(),
        "output_folder": output_folder.as_posix(),
        "files_processed": [document.relative_path for document in documents],
        "source_file_hashes": {document.relative_path: document.sha256 for document in documents},
        "outputs_generated": outputs_generated,
        "chronology_event_count": chronology_event_count,
        "evidence_item_count": evidence_item_count,
        "issue_category_count": issue_category_count,
        "unsupported_claim_count": unsupported_claim_count,
        "missing_info_item_count": missing_info_item_count,
        "validation_status": validation_status,
        "validation_errors": validation_errors,
        "human_review_required": True,
        "legal_advice_boundary": LEGAL_ADVICE_BOUNDARY,
    }


def write_receipt(output_folder: Path, receipt: dict) -> None:
    write_json(output_folder / "matter_receipt.json", receipt)
    lines = [
        "# Matter Receipt",
        "",
        f"> {LEGAL_ADVICE_BOUNDARY}",
        "",
        "## Status",
        "",
        f"- Validation status: `{receipt['validation_status']}`",
        f"- Human review required: `{str(receipt['human_review_required']).lower()}`",
        "- Legal advice boundary present: `true`",
        "",
        "## Run",
        "",
        f"- Run timestamp: {receipt['run_timestamp']}",
        f"- Matter ID: {receipt['matter_id']}",
        f"- Input folder: `{receipt['input_folder']}`",
        f"- Output folder: `{receipt['output_folder']}`",
        "",
        "## Counts",
        "",
        f"- Files processed: {len(receipt['files_processed'])}",
        f"- Outputs generated: {len(receipt['outputs_generated'])}",
        f"- Chronology events: {receipt['chronology_event_count']}",
        f"- Evidence items: {receipt['evidence_item_count']}",
        f"- Issue categories: {receipt['issue_category_count']}",
        f"- Unsupported claims: {receipt['unsupported_claim_count']}",
        f"- Missing info items: {receipt['missing_info_item_count']}",
        "",
        "## Outputs",
    ]
    for output in receipt["outputs_generated"]:
        lines.append(f"- `{output}`")
    lines.append("")
    lines.append("## Source Hashes")
    lines.append("")
    for file_name, file_hash in receipt["source_file_hashes"].items():
        lines.append(f"- `{file_name}`: `{file_hash[:16]}...`")
    if receipt["validation_errors"]:
        lines.append("")
        lines.append("## Validation Errors")
        for error in receipt["validation_errors"]:
            lines.append(f"- {error}")
    else:
        lines.append("")
        lines.append("## Validation Errors")
        lines.append("")
        lines.append("None.")
    lines.append("")
    lines.append("## Review Boundary")
    lines.append("")
    lines.append("Generated artifacts organize the sample matter. They do not decide legal meaning, legal strategy, deadlines, or whether a draft should be sent.")
    lines.append("")
    (output_folder / "matter_receipt.md").write_text("\n".join(lines), encoding="utf-8")
