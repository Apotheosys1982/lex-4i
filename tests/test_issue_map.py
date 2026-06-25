from pathlib import Path

from lex_4i.chronology import extract_events
from lex_4i.ingest import load_documents
from lex_4i.issue_map import build_issue_map


ROOT = Path(__file__).resolve().parents[1]


def test_issue_map_uses_review_signal_language():
    documents = load_documents(ROOT / "sample_matter")
    events = extract_events(documents)
    issues = build_issue_map(documents, events)
    categories = {issue["category"] for issue in issues}
    assert "retaliation signal" in categories
    assert "wage/hour signal" in categories
    assert all(issue["human_review_required"] is True for issue in issues)
    assert all("not a legal conclusion" in issue["review_note"] or "Missing source" in issue["review_note"] for issue in issues)

