# GitHub Repo Packet

## Repository Name

`lex-4i`

## Display Name

Lex 4i

## Description

AI-assisted legal-ops harness for matter intake, evidence indexing, issue mapping, drafting review, and receipt-backed workflow artifacts.

## Topics

- `legal-ops`
- `compliance`
- `evidence-indexing`
- `chronology`
- `red-team-review`
- `workflow-automation`
- `ai-workflow`
- `receipts`

## Short Positioning

Lex 4i is a legal/compliance workflow proof artifact. It demonstrates how messy matter materials can be organized into reviewable chronology, evidence index, issue/risk signals, drafting support, red-team findings, unsupported-claim reports, hashes, and receipts.

## Boundary

Lex 4i is not legal advice, not an AI lawyer, and not a legal conclusion engine. It is an infrastructure harness for organizing matter materials into artifacts a qualified human can inspect.

## Pinned Repo Blurb

Lex 4i turns a synthetic matter folder into receipt-backed legal-ops artifacts: intake map, chronology, evidence index, issue/risk map, missing-info checklist, drafting support, red-team review, unsupported-claims report, hashes, and validation receipt.

## Demo Command

```bash
python3 -m lex_4i.cli run sample_matter --out outputs/sample_run
```

## Clean Clone Test

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m lex_4i.cli run sample_matter --out outputs/sample_run
.venv/bin/python -m pytest
```

