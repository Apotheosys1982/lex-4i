from pathlib import Path

from lex_4i.ingest import load_documents, matter_id


ROOT = Path(__file__).resolve().parents[1]


def test_ingest_loads_synthetic_documents():
    documents = load_documents(ROOT / "sample_matter")
    assert len(documents) >= 10
    assert matter_id(documents) == "SYN-WORKPLACE-001"
    assert all(document.sha256 for document in documents)

