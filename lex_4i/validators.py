from __future__ import annotations

import json
from pathlib import Path

from .models import LEGAL_ADVICE_BOUNDARY, SYNTHETIC_NOTE

REQUIRED_INPUTS = [
    "intake.md",
    "facts.md",
    "correspondence/email_001.md",
    "correspondence/email_002.md",
    "correspondence/demand_response.md",
    "evidence/timesheet_notes.md",
    "evidence/policy_excerpt.md",
    "evidence/termination_notice.md",
    "evidence/witness_note.md",
    "drafts/draft_demand_letter.md",
]

REQUIRED_OUTPUTS = [
    "chronology.md",
    "chronology.json",
    "evidence_index.md",
    "evidence_index.json",
    "issue_map.md",
    "issue_map.json",
    "missing_info_checklist.md",
    "drafting_support_packet.md",
    "red_team_review.md",
    "unsupported_claims_report.md",
    "red_team_report.json",
    "matter_receipt.json",
    "matter_receipt.md",
]

PRIVATE_OR_REAL_NAME_GUARDS = [
    "John Barros",
    "John P. Barros",
    "AEMI",
    "C-4 Analytics",
    "Clinically AI",
    "Navitas",
]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_sample_matter(matter_path: Path) -> list[str]:
    errors: list[str] = []
    if not matter_path.exists():
        return [f"sample matter folder does not exist: {matter_path}"]
    for relative in REQUIRED_INPUTS:
        if not (matter_path / relative).exists():
            errors.append(f"missing required input: {relative}")
    for path in matter_path.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if SYNTHETIC_NOTE not in text:
            errors.append(f"missing synthetic sample note: {path.relative_to(matter_path)}")
        for guard in PRIVATE_OR_REAL_NAME_GUARDS:
            if guard in text:
                errors.append(f"sample data contains guarded real/private name '{guard}' in {path.relative_to(matter_path)}")
    return errors


def validate_boundary_docs(project_root: Path) -> list[str]:
    errors: list[str] = []
    required_docs = [
        project_root / "README.md",
        project_root / "docs" / "LEGAL_ADVICE_BOUNDARY.md",
        project_root / "docs" / "HUMAN_REVIEW_BOUNDARIES.md",
    ]
    for path in required_docs:
        if not path.exists():
            errors.append(f"missing boundary doc: {path}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        if "not legal advice" not in text:
            errors.append(f"missing legal advice boundary language: {path}")
        if "human" not in text or "review" not in text:
            errors.append(f"missing human review boundary language: {path}")
    return errors


def validate_generated_outputs(out_dir: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_OUTPUTS:
        if not (out_dir / relative).exists():
            errors.append(f"missing generated output: {relative}")

    json_contracts = {
        "chronology.json": ["matter_id", "legal_advice_boundary", "events"],
        "evidence_index.json": ["matter_id", "legal_advice_boundary", "evidence_items"],
        "issue_map.json": ["matter_id", "legal_advice_boundary", "issues"],
        "red_team_report.json": ["matter_id", "draft_file", "legal_advice_boundary", "findings", "unsupported_claims"],
        "matter_receipt.json": [
            "run_timestamp",
            "matter_id",
            "input_folder",
            "output_folder",
            "files_processed",
            "source_file_hashes",
            "outputs_generated",
            "validation_status",
            "legal_advice_boundary",
        ],
    }
    for relative, keys in json_contracts.items():
        path = out_dir / relative
        if not path.exists():
            continue
        try:
            payload = _load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in {relative}: {exc}")
            continue
        for key in keys:
            if key not in payload:
                errors.append(f"{relative} missing required key: {key}")

    for path in out_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if LEGAL_ADVICE_BOUNDARY not in text:
            errors.append(f"generated markdown missing boundary language: {path.name}")
    return errors


def validation_status(errors: list[str]) -> str:
    return "pass" if not errors else "fail"

