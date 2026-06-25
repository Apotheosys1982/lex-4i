from __future__ import annotations

import re
from pathlib import Path

from .hashing import sha256_file
from .models import MatterDocument

FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 -]+):\s*(.+?)\s*$")


def normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def extract_fields(text: str) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = FIELD_RE.match(line.strip())
        if not match:
            continue
        key = normalize_key(match.group(1))
        fields.setdefault(key, []).append(match.group(2).strip())
    return fields


def classify_source(path: Path, matter_path: Path, fields: dict[str, list[str]]) -> str:
    if "source_type" in fields:
        return fields["source_type"][0].strip().lower()
    relative = path.relative_to(matter_path)
    if relative.parts and relative.parts[0] in {"correspondence", "evidence", "drafts"}:
        return relative.parts[0].rstrip("s")
    if path.name == "intake.md":
        return "intake"
    if path.name == "facts.md":
        return "facts"
    return "matter_note"


def load_documents(matter_path: Path) -> list[MatterDocument]:
    matter_path = matter_path.resolve()
    documents: list[MatterDocument] = []
    for path in sorted(matter_path.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        fields = extract_fields(text)
        documents.append(
            MatterDocument(
                path=path,
                relative_path=path.relative_to(matter_path).as_posix(),
                text=text,
                source_type=classify_source(path, matter_path, fields),
                sha256=sha256_file(path),
                fields=fields,
            )
        )
    return documents


def matter_id(documents: list[MatterDocument]) -> str:
    for document in documents:
        if "matter_id" in document.fields:
            return document.fields["matter_id"][0]
    return "SYN-WORKPLACE-001"


def first_field(document: MatterDocument, key: str, default: str = "") -> str:
    return document.fields.get(key, [default])[0]


def all_missing_items(documents: list[MatterDocument]) -> list[dict[str, str]]:
    missing: list[dict[str, str]] = []
    for document in documents:
        for item in document.fields.get("missing", []):
            missing.append({"source_file": document.relative_path, "item": item})
    return missing

