#!/usr/bin/env python3
"""Deterministic checks for the composite STEM paper evaluator."""

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


@dataclass(frozen=True)
class PaperEvaluatorCheckResult:
    passed: bool
    errors: list[str]
    composite_score: int
    band: str

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "composite_score": self.composite_score,
            "band": self.band,
        }


class PaperEvaluatorCheck:
    FIXTURE = " ".join([
        "This submitted manuscript reports public health epidemiology methods",
        "using a longitudinal dataset, regression analysis, validation metrics,",
        "reproducible code, repository documentation, results, tables, and figures.",
        "It cites DOI 10.1038/nature12373, arXiv:2101.00001, and PMID: 23803847.",
    ])

    def run(self) -> PaperEvaluatorCheckResult:
        errors: list[str] = []
        payload = StemPaperEvaluator(live=False).evaluate(self.FIXTURE, author="Example Submitter")
        score = payload.get("composite_paper_score", {})
        if not isinstance(score, dict):
            errors.append("Missing composite_paper_score object")
            return PaperEvaluatorCheckResult(False, errors, 0, "missing")
        composite = int(score.get("composite_score", 0))
        band = str(score.get("band", ""))
        if composite < 60:
            errors.append(f"Expected composite score >= 60, found {composite}")
        if band not in {"strong_stem_paper_package", "credible_stem_paper_package"}:
            errors.append(f"Unexpected composite band: {band}")
        citation = payload.get("citation_verification", {})
        if not isinstance(citation, dict):
            errors.append("Missing citation_verification object")
        elif int(citation.get("reference_count", 0)) < 3:
            errors.append("Expected at least three extracted references")
        return PaperEvaluatorCheckResult(not errors, errors, composite, band)


def main() -> int:
    result = PaperEvaluatorCheck().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
