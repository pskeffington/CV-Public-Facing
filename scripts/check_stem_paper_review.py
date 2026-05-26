#!/usr/bin/env python3
"""Deterministic checks for the STEM paper Markdown review writer."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_paper_evaluator import StemPaperEvaluator  # noqa: E402
from write_stem_paper_review import render_review  # noqa: E402


@dataclass(frozen=True)
class PaperReviewCheckResult:
    passed: bool
    errors: list[str]
    length: int

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "length": self.length,
        }


class PaperReviewCheck:
    FIXTURE = " ".join([
        "This submitted manuscript reports public health epidemiology methods",
        "using a longitudinal dataset, regression analysis, validation metrics,",
        "reproducible code, repository documentation, results, tables, and figures.",
        "It cites DOI 10.1038/nature12373, arXiv:2101.00001, PMID: 23803847,",
        "and https://example.org/reproducibility-manifest.",
    ])

    REQUIRED_SECTIONS = [
        "# STEM Paper Review",
        "## Review configuration",
        "## Composite score",
        "## STEM presence",
        "## Publishing signal",
        "## Review flags",
        "## Source provenance",
        "## Extracted references",
    ]

    def run(self) -> PaperReviewCheckResult:
        errors: list[str] = []
        payload = StemPaperEvaluator(live=False).evaluate(self.FIXTURE, author="Example Submitter")
        report = render_review(payload, title="Contract fixture")
        for section in self.REQUIRED_SECTIONS:
            if section not in report:
                errors.append(f"Missing report section: {section}")
        for token in [
            "Live mode:",
            "Max author candidates:",
            "Composite STEM weight:",
            "Composite publishing weight:",
            "Reference signal weight:",
            "Author signal weight:",
            "Allowed URL hosts:",
            "Blocked URL hosts:",
            "External services enabled:",
            "Composite score:",
            "STEM score:",
            "Reference count:",
            "Policy-blocked references:",
            "Author match confidence:",
            "| Type | Value | Verified | Mode | Source | Score | Band |",
        ]:
            if token not in report:
                errors.append(f"Missing report token: {token}")
        if "10.1038/nature12373" not in report:
            errors.append("Expected DOI reference not rendered")
        if "offline" not in report or "identifier_extractor" not in report:
            errors.append("Expected offline provenance not rendered")
        if "0.75" not in report or "0.25" not in report:
            errors.append("Expected default composite weights not rendered")
        return PaperReviewCheckResult(not errors, errors, len(report))


def main() -> int:
    result = PaperReviewCheck().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
