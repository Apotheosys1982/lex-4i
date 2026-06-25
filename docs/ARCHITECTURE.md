# Architecture

Lex 4i is a deterministic legal-operations harness inspired by lex fori: forum, procedure, source record, and review context matter. It converts a synthetic matter folder into structured artifacts that can be inspected by a qualified human reviewer.

It is not legal advice and does not replace attorney judgment.

## 4i Model

- Intake: collect matter materials, facts, correspondence, drafts, and evidence.
- Index: build chronology, evidence index, source map, and exhibit map.
- Interpret: classify issue/risk signals, contradictions, missing information, and unsupported assertions.
- Instrument: generate review packets, red-team reports, receipts, hashes, validation artifacts, and review gates.

## Input Layer

The input is a matter folder containing Markdown files:

- `intake.md`
- `facts.md`
- correspondence files
- evidence files
- draft files

Each sample file contains synthetic facts and explicit field markers. The markers keep v0.1 deterministic and testable.

## Ingestion Layer

`ingest.py` walks the matter folder, reads Markdown files, extracts field markers, computes source hashes, and classifies each document by folder and filename.

## Chronology Layer

`chronology.py` turns event markers into ordered chronology events. Events are labeled as supported, partially supported, inferred, missing support, or conflicting information.

## Evidence Index Layer

`evidence_index.py` creates one evidence item per processed source file, links documents to chronology events and issue categories, and records a SHA-256 hash for document control.

## Issue/Risk Map Layer

`issue_map.py` aggregates issue/risk signals without making legal conclusions. Categories are workflow classification signals that require human review.

## Draft-Support Layer

`draft_support.py` organizes source-backed facts, facts needing verification, possible sections, exhibit candidates, tone notes, and human review checks.

## Red-Team Layer

`redteam.py` reviews the synthetic draft letter for unsupported assertions, overbroad statements, vague claims, missing source support, tone risk, and required human review.

## Receipt Layer

`receipts.py` writes JSON and Markdown receipts with run timestamp, input folder, output folder, processed files, hashes, generated outputs, counts, validation status, and boundary language.

## Human Review Boundary

The harness produces organization, not legal judgment. Legal significance, case strategy, deadlines, jurisdictional rules, and send decisions require qualified human/legal review.
