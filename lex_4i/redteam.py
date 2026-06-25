from __future__ import annotations

import re
from pathlib import Path

from .models import LEGAL_ADVICE_BOUNDARY

RISK_PATTERNS = [
    ("unsupported marker", re.compile(r"\[UNSUPPORTED\]", re.IGNORECASE)),
    ("legal conclusion risk", re.compile(r"\b(clearly violated the law|valid legal claim|illegal)\b", re.IGNORECASE)),
    ("absolute language risk", re.compile(r"\b(every single day|always|never|guaranteed)\b", re.IGNORECASE)),
    ("unsupported damages figure", re.compile(r"\$\d[\d,]*(?:\.\d{2})?")),
]


def review_draft(draft_path: Path, matter_id: str) -> dict:
    text = draft_path.read_text(encoding="utf-8")
    findings: list[dict] = []
    unsupported_claims: list[dict] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" in stripped[:25]:
            continue
        matched = False
        for category, pattern in RISK_PATTERNS:
            if pattern.search(stripped):
                finding = {
                    "line": line_number,
                    "category": category,
                    "text": stripped.replace("[UNSUPPORTED]", "").strip(),
                    "review_note": "Human/legal review required before relying on or sending this assertion.",
                }
                findings.append(finding)
                if "unsupported" in category or "[UNSUPPORTED]" in stripped:
                    unsupported_claims.append(finding)
                matched = True
        if not matched and len(stripped) > 180:
            findings.append(
                {
                    "line": line_number,
                    "category": "long assertion review",
                    "text": stripped,
                    "review_note": "Long assertions should be checked against source support before use.",
                }
            )
    return {
        "matter_id": matter_id,
        "draft_file": draft_path.as_posix(),
        "legal_advice_boundary": LEGAL_ADVICE_BOUNDARY,
        "findings": findings,
        "unsupported_claims": unsupported_claims,
    }


def render_red_team_review(report: dict) -> str:
    lines = ["# Drafting Red-Team Review", "", f"> {LEGAL_ADVICE_BOUNDARY}", ""]
    lines.append("This review flags drafting risks. It does not decide legal merit.")
    lines.append("")
    for finding in report["findings"]:
        lines.append(f"## Line {finding['line']} - {finding['category']}")
        lines.append(f"- Text: {finding['text']}")
        lines.append(f"- Review note: {finding['review_note']}")
        lines.append("")
    if not report["findings"]:
        lines.append("No red-team findings were detected by the v0.1 ruleset.")
    return "\n".join(lines)


def render_unsupported_claims(report: dict) -> str:
    lines = ["# Unsupported Claims Report", "", f"> {LEGAL_ADVICE_BOUNDARY}", ""]
    if not report["unsupported_claims"]:
        lines.append("No unsupported claims were detected by the v0.1 ruleset.")
        return "\n".join(lines) + "\n"
    lines.append("These claims should not be used without additional source support and qualified review.")
    lines.append("")
    for claim in report["unsupported_claims"]:
        lines.append(f"- Line {claim['line']}: {claim['text']}")
    lines.append("")
    return "\n".join(lines)

