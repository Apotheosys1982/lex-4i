from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_has_lex_4i_positioning():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Lex 4i" in readme
    assert "lex fori" in readme
    assert "Intake" in readme
    assert "Index" in readme
    assert "Interpret" in readme
    assert "Instrument" in readme
    old_display_name = "Legal Matter " + "Workbench"
    old_package_name = "legal_matter_" + "workbench"
    assert old_display_name not in readme
    assert old_package_name not in readme


def test_github_packet_is_present():
    packet = (ROOT / "docs" / "GITHUB_REPO_PACKET.md").read_text(encoding="utf-8")
    assert "AI-assisted legal-ops harness" in packet
    assert "not legal advice" in packet.lower()
    assert "python3 -m lex_4i.cli run sample_matter --out outputs/sample_run" in packet
