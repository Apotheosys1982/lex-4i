from pathlib import Path

from lex_4i.chronology import extract_events
from lex_4i.evidence_index import build_evidence_index
from lex_4i.ingest import load_documents


ROOT = Path(__file__).resolve().parents[1]


def test_evidence_index_links_events_and_hashes():
    documents = load_documents(ROOT / "sample_matter")
    events = extract_events(documents)
    items = build_evidence_index(documents, events)
    assert len(items) == len(documents)
    assert all(len(item.hash) == 64 for item in items)
    assert any(item.linked_chronology_events for item in items)
    assert any("wage/hour signal" in item.linked_issue_categories for item in items)

