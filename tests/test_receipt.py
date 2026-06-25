import json
from pathlib import Path

from lex_4i.cli import run


ROOT = Path(__file__).resolve().parents[1]


def test_cli_run_writes_receipt_and_outputs(tmp_path):
    out_dir = tmp_path / "sample_run"
    result = run(ROOT / "sample_matter", out_dir)
    assert result == 0
    receipt = json.loads((out_dir / "matter_receipt.json").read_text(encoding="utf-8"))
    assert receipt["validation_status"] == "pass"
    assert receipt["human_review_required"] is True
    assert receipt["unsupported_claim_count"] >= 3
    assert (out_dir / "chronology.md").exists()
    assert (out_dir / "red_team_review.md").exists()

