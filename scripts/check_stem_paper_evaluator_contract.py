#!/usr/bin/env python3
"""Contract checks for composite STEM paper evaluator output."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_paper_evaluator import StemPaperEvaluator  # noqa: E402


@dataclass(frozen=True)
class EvaluatorContractResult:
    """Validation result for the evaluator output contract."""

    passed: bool
    errors: list[str]
    composite_score: int
    reference_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "composite_score": self.composite_score,
            "reference_count": self.reference_count,
        }


class StemPaperEvaluatorContractChecker:
    """Validate the evaluator JSON shape and core numeric invariants."""

    FIXTURE = " ".join([
        "This submitted manuscript reports public health epidemiology methods",
        "using a longitudinal dataset, regression analysis, validation metrics,",
        "reproducible code, repository documentation, results, tables, and figures.",
        "It cites DOI 10.1038/nature12373, arXiv:2101.00001, PMID: 23803847,",
        "and https://example.org/reproducibility-manifest.",
    ])

    TOP_LEVEL_KEYS = {
        "live",
        "stem_presence",
        "publishing_signal_summary",
        "composite_paper_score",
        "citation_verification",
    }

    STEM_KEYS = {
        "score",
        "drift_score",
        "band",
        "rationale",
        "matched_domain_terms",
        "matched_method_terms",
        "matched_reproducibility_terms",
        "matched_progress_terms",
        "matched_drift_terms",
    }

    PUBLISHING_KEYS = {
        "reference_count",
        "verified_reference_count",
        "average_reference_score",
        "author_signal_score",
        "cited_by_count",
        "works_count",
        "h_index",
        "i10_index",
        "author_candidate_count",
        "author_ambiguity_warning",
        "author_match_confidence",
        "source_provenance",
        "policy_blocked_reference_count",
    }

    COMPOSITE_KEYS = {
        "stem_presence_score",
        "stem_drift_score",
        "publishing_signal_score",
        "composite_score",
        "composite_drift_score",
        "band",
        "rationale",
        "review_flags",
    }

    CITATION_KEYS = {
        "live",
        "reference_count",
        "verified_reference_count",
        "author_citation_profile",
        "references",
    }

    VALID_COMPOSITE_BANDS = {
        "strong_stem_paper_package",
        "credible_stem_paper_package",
        "mixed_or_underverified_package",
        "high_drift_or_low_evidence_package",
    }

    def run(self) -> EvaluatorContractResult:
        errors: list[str] = []
        payload = StemPaperEvaluator(live=False).evaluate(self.FIXTURE, author="Example Submitter")
        self._check_keys("top-level", payload, self.TOP_LEVEL_KEYS, errors)

        stem = self._object(payload, "stem_presence", errors)
        publishing = self._object(payload, "publishing_signal_summary", errors)
        composite = self._object(payload, "composite_paper_score", errors)
        citation = self._object(payload, "citation_verification", errors)

        self._check_keys("stem_presence", stem, self.STEM_KEYS, errors)
        self._check_keys("publishing_signal_summary", publishing, self.PUBLISHING_KEYS, errors)
        self._check_keys("composite_paper_score", composite, self.COMPOSITE_KEYS, errors)
        self._check_keys("citation_verification", citation, self.CITATION_KEYS, errors)

        self._check_score_pair("stem_presence", stem, "score", "drift_score", errors)
        self._check_score_pair("composite_paper_score", composite, "composite_score", "composite_drift_score", errors)
        self._check_range("composite_paper_score", composite, "publishing_signal_score", errors)

        if composite.get("band") not in self.VALID_COMPOSITE_BANDS:
            errors.append(f"Invalid composite band: {composite.get('band')}")
        if not isinstance(composite.get("review_flags"), list):
            errors.append("composite_paper_score.review_flags must be a list")
        if "author_match_unconfirmed" not in composite.get("review_flags", []):
            errors.append("Offline composite review_flags should include author_match_unconfirmed")
        if citation.get("live") is not False:
            errors.append("Contract fixture must run in offline mode with live=false")
        if int(citation.get("verified_reference_count", -1)) != 0:
            errors.append("Offline citation verification should not live-verify references")
        if int(citation.get("reference_count", 0)) < 4:
            errors.append("Expected at least four extracted references in contract fixture")
        if int(publishing.get("reference_count", 0)) != int(citation.get("reference_count", -1)):
            errors.append("Publishing summary reference_count does not match citation_verification reference_count")
        if not isinstance(publishing.get("source_provenance"), list) or not publishing.get("source_provenance"):
            errors.append("publishing_signal_summary.source_provenance must be a non-empty list")
        if self._safe_int(publishing.get("policy_blocked_reference_count"), -1) != 0:
            errors.append("Offline policy_blocked_reference_count should be zero")
        if self._safe_int(publishing.get("author_candidate_count"), -1) != 0:
            errors.append("Offline author_candidate_count should be zero")
        if publishing.get("author_ambiguity_warning") is not None:
            errors.append("Offline author_ambiguity_warning should be null")
        if publishing.get("author_match_confidence") != "offline_unverified":
            errors.append("Offline author_match_confidence should be offline_unverified")

        return EvaluatorContractResult(
            passed=not errors,
            errors=errors,
            composite_score=self._safe_int(composite.get("composite_score")),
            reference_count=self._safe_int(citation.get("reference_count")),
        )

    @staticmethod
    def _object(payload: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
        value = payload.get(key)
        if not isinstance(value, dict):
            errors.append(f"Expected object at {key}")
            return {}
        return value

    @staticmethod
    def _check_keys(name: str, payload: dict[str, Any], required: set[str], errors: list[str]) -> None:
        missing = sorted(required - set(payload.keys()))
        if missing:
            errors.append(f"{name} missing keys: {', '.join(missing)}")

    @classmethod
    def _check_score_pair(cls, name: str, payload: dict[str, Any], score_key: str, drift_key: str, errors: list[str]) -> None:
        score = cls._safe_int(payload.get(score_key), -1)
        drift = cls._safe_int(payload.get(drift_key), -1)
        if not 0 <= score <= 100:
            errors.append(f"{name}.{score_key} outside 0-100: {score}")
        if not 0 <= drift <= 100:
            errors.append(f"{name}.{drift_key} outside 0-100: {drift}")
        if 0 <= score <= 100 and 0 <= drift <= 100 and score + drift != 100:
            errors.append(f"{name}.{score_key} and {drift_key} do not sum to 100")

    @classmethod
    def _check_range(cls, name: str, payload: dict[str, Any], key: str, errors: list[str]) -> None:
        value = cls._safe_int(payload.get(key), -1)
        if not 0 <= value <= 100:
            errors.append(f"{name}.{key} outside 0-100: {value}")

    @staticmethod
    def _safe_int(value: object, default: int = 0) -> int:
        try:
            return int(value) if value is not None else default
        except (TypeError, ValueError):
            return default


def main() -> int:
    result = StemPaperEvaluatorContractChecker().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
