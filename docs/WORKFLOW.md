# Workflow

Lex 4i follows a receipt-backed matter organization workflow built around Intake, Index, Interpret, and Instrument.

```text
matter folder
  -> ingest
  -> chronology
  -> evidence index
  -> issue/risk map
  -> drafting support
  -> red-team review
  -> validation
  -> receipt
```

## 1. Matter Folder

The operator starts with a matter folder. In v0.1, the included matter is fully synthetic.

## 2. Ingest

The harness reads Markdown files, extracts structured markers, computes file hashes, and records source metadata.

## 3. Chronology

Event markers become chronology events with support status, confidence, source references, and notes.

## 4. Evidence Index

Every processed document becomes an indexed evidence item with hash, summary, source type, linked events, linked issue categories, and review notes.

## 5. Issue/Risk Map

The harness groups issue/risk signals and documentation gaps. It does not conclude that any legal claim exists.

## 6. Drafting Support

The harness organizes known facts, facts needing verification, source-backed assertions, unsupported assertions, exhibit candidates, and human review checks.

## 7. Red-Team Review

The harness reviews a synthetic draft letter for unsupported assertions, tone risk, vague claims, overbroad claims, and missing support.

## 8. Receipt

The harness writes a JSON and Markdown receipt so the run can be audited.

## Approval Gate

No generated draft should be sent or relied on without qualified human/legal review.
