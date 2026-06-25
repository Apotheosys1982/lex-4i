# Lex 4i

Lex 4i is an AI-assisted legal-ops workflow harness for turning structured synthetic matter files into chronology, evidence index, issue/risk map, missing-info checklist, red-team review, unsupported-claims report, and receipt-backed review artifacts.

Not legal advice. Not attorney replacement. Not litigation prediction. Built for source-bound organization and human review.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-8%20passed-brightgreen)
![Data](https://img.shields.io/badge/data-synthetic%20sample-orange)
![Legal Advice](https://img.shields.io/badge/legal%20advice-no-red)
![Review](https://img.shields.io/badge/human%20review-required-purple)
![Receipts](https://img.shields.io/badge/receipts-generated-blue)
![Version](https://img.shields.io/badge/v0.1-proof-lightgrey)

Lex 4i is inspired by the procedural idea of lex fori: the forum, source record, and procedural context matter. The current v0.1 repo demonstrates workflow infrastructure for organizing matter materials into structured, reviewable artifacts.

## Visual Overview

<!--
Hero visual reserved for approved repo asset:
assets/lex-4i-readme-hero.png

Do not copy ImageGen output into this repo until the image has been visually inspected and approved.
The approved visual must communicate Intake -> Index -> Interpret -> Instrument, source-bound artifacts, receipts, and human review.
It must not claim legal advice, attorney replacement, litigation prediction, court-ready filing, legal research access, Westlaw, LexisNexis, PACER, court API access, or proprietary legal database access.
-->

## Try It

Run the v0.1 sample matter pipeline:

```bash
python3 -m lex_4i.cli run sample_matter --out outputs/sample_run
```

## Sample Run Snapshot

- Matter ID: `SYN-WORKPLACE-001`
- Validation status: `pass`
- Chronology events: `14`
- Evidence items: `11`
- Issue categories: `8`
- Unsupported claims flagged: `6`
- Missing information items: `22`
- Files processed: `11`
- Outputs generated: `13`

## What It Generates

Lex 4i takes a synthetic matter folder and produces reviewable legal-operations artifacts:

- `chronology.md` / `chronology.json`
- `evidence_index.md` / `evidence_index.json`
- `issue_map.md` / `issue_map.json`
- `missing_info_checklist.md`
- `drafting_support_packet.md`
- `red_team_review.md`
- `unsupported_claims_report.md`
- `red_team_report.json`
- `matter_receipt.md` / `matter_receipt.json`

## Why It Exists

Legal AI should start with the record, not the answer. Lex 4i demonstrates a constrained workflow pattern for organizing matter materials before human review.

The harness is designed for high-stakes document organization where source boundaries, human review, and audit trails matter. It is not a legal-advice bot and does not replace attorney judgment.

## The 4i Operating Loop

Lex 4i uses a four-part workflow:

- Intake: collect matter materials, facts, correspondence, drafts, and evidence.
- Index: build the evidence index, chronology, source map, and exhibit map.
- Interpret: classify issue/risk signals, contradictions, missing information, and unsupported claims without giving legal conclusions.
- Instrument: generate review packets, red-team reports, receipts, hashes, validation artifacts, and human review gates.

## Quickstart

From a clean clone:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m lex_4i.cli run sample_matter --out outputs/sample_run
.venv/bin/python -m pytest
```

For a direct local run without installing the package:

```bash
python3 -m lex_4i.cli run sample_matter --out outputs/sample_run
```

Then inspect:

```text
outputs/sample_run/chronology.md
outputs/sample_run/evidence_index.md
outputs/sample_run/issue_map.md
outputs/sample_run/drafting_support_packet.md
outputs/sample_run/red_team_review.md
outputs/sample_run/matter_receipt.md
```

## What It Does Not Do

- It does not provide legal advice.
- It does not replace attorneys, compliance officers, HR investigators, or human reviewers.
- It does not predict legal outcomes.
- It does not determine whether any claim is valid.
- It does not access Westlaw, LexisNexis, PACER, court APIs, or proprietary legal databases.
- It does not use real private matter facts.

## Why It Matters

Document-heavy matters often start messy: emails, timelines, policies, notes, draft letters, unsupported assertions, missing dates, and conflicting facts. Lex 4i shows how AI-assisted workflow infrastructure can turn that mess into structured artifacts that a qualified human can inspect.

The project demonstrates disciplined matter organization rather than automated legal judgment.

## Architecture Overview

```text
matter folder
  -> ingest
  -> chronology
  -> evidence index
  -> issue/risk map
  -> drafting support
  -> red-team review
  -> validators
  -> receipt + hashes
```

The sample matter is synthetic and marker-driven so the v0.1 harness can be deterministic, testable, and reviewable without relying on external AI APIs.

## Human Review Boundary

Every generated artifact is an organizational aid. A qualified human reviewer must evaluate legal significance, factual accuracy, strategy, deadlines, jurisdictional requirements, ethics obligations, and whether any draft should be sent.

## Legal Advice Boundary

This project is not legal advice. It is not an attorney-client communication tool. It is not a substitute for legal counsel. It organizes synthetic demonstration materials into structured artifacts for review.

## Folder Structure

```text
docs/                    Project architecture and review boundaries
schemas/                 JSON schema contracts for generated artifacts
sample_matter/           Synthetic sample matter input folder
lex_4i/                  Python package and CLI
outputs/                 Generated run outputs
tests/                   Pytest suite
receipts/                Build/project receipts
```

## GitHub Description

Use this repository description:

```text
AI-assisted legal-ops harness for matter intake, evidence indexing, issue mapping, drafting review, and receipt-backed workflow artifacts.
```

Suggested topics:

```text
legal-ops, compliance, evidence-indexing, chronology, red-team-review, workflow-automation, ai-workflow, receipts
```

## Roadmap

Future hardening may include:

- Richer document parsing
- PDF ingestion
- OCR support
- DOCX export
- Local LLM support
- RAG/source retrieval
- Public legal source adapter interfaces
- Mock provider adapter interfaces
- Timeline visualization
- Browser proof surface
- Bounded assistant over generated matter artifacts
- Attorney review workflow
- Compliance/investigation variants

These are roadmap items, not current claims.

## Author / Operator Positioning

This repository demonstrates AI-assisted workflow infrastructure for document-heavy, high-stakes, adversarial domains. It is meant to show matter organization, evidence tracking, source boundaries, drafting support, red-team review, validation, receipts, and human review gates without overclaiming legal authority.
