# Lex 4i Rename Receipt - 2026-06-24

## Rename

- Old scaffold name: `legal-matter-workbench`
- New product/repo name: `lex-4i`
- Product display name: `Lex 4i`
- Old local path: `/Users/johnbarros/Documents/Codex/04_products_and_verticals/legal-matter-workbench`
- New local path: `/Users/johnbarros/Documents/Codex/04_products_and_verticals/lex-4i`
- Old Python package: `legal_matter_workbench`
- New Python package: `lex_4i`

## Product Meaning

Lex 4i is inspired by `lex fori`: the forum matters, the source record matters, and the workflow must be reviewable.

The `4i` operating loop is:

- Intake: collect matter materials, facts, correspondence, drafts, and evidence.
- Index: build chronology, evidence index, source map, and exhibit map.
- Interpret: classify issue/risk signals, contradictions, missing information, and unsupported assertions.
- Instrument: generate review packets, red-team reports, receipts, hashes, validation artifacts, and review gates.

## Files / Registries Updated

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/WORKFLOW.md`
- `docs/GITHUB_PROFILE_POSITIONING.md`
- `pyproject.toml`
- `tests/*.py`
- `lex_4i/*.py`
- `_mission_control/PROJECT_REGISTRY.md`
- `_mission_control/PROJECT_REGISTRY.json`
- `outputs/sample_run/*` regenerated under the new path

## Commands Run

```bash
python3 -m lex_4i.cli run sample_matter --out outputs/sample_run
python3 -m json.tool /Users/johnbarros/Documents/Codex/_mission_control/PROJECT_REGISTRY.json
python3 -m compileall lex_4i
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip pytest
.venv/bin/python -m pytest
```

## Validation

- Old path no longer used as canonical project path.
- New path exists.
- CLI run passed under `lex_4i`.
- `PROJECT_REGISTRY.json` parses.
- Python compile check passed.
- Pytest passed: `6 passed`.
- Sample run artifacts regenerated with `/Users/johnbarros/Documents/Codex/04_products_and_verticals/lex-4i`.
- No public deploy occurred.
- No Git push occurred.
- No unrelated projects were moved, renamed, or deleted.

## Current Command

```bash
python3 -m lex_4i.cli run sample_matter --out outputs/sample_run
```

