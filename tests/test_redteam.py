from pathlib import Path

from lex_4i.redteam import review_draft


ROOT = Path(__file__).resolve().parents[1]


def test_redteam_flags_unsupported_claims():
    report = review_draft(ROOT / "sample_matter" / "drafts" / "draft_demand_letter.md", "SYN-WORKPLACE-001")
    assert len(report["unsupported_claims"]) >= 3
    assert any("owes exactly" in claim["text"] for claim in report["unsupported_claims"])

