from pathlib import Path

from lex_4i.chronology import extract_events
from lex_4i.ingest import load_documents


ROOT = Path(__file__).resolve().parents[1]


def test_chronology_extracts_supported_and_partial_events():
    documents = load_documents(ROOT / "sample_matter")
    events = extract_events(documents)
    statuses = {event.support_status for event in events}
    assert len(events) >= 8
    assert "supported" in statuses
    assert "partially supported" in statuses
    assert any("timekeeping" in event.description.lower() for event in events)

