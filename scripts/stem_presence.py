#!/usr/bin/env python3
"""STEM presence and drift scoring for public research surfaces.

The scorer is intentionally transparent and deterministic. It favors evidence
of core STEM progress: domain specificity, methods, reproducibility, validation,
measurement, and concrete outputs. It penalizes surface drift toward purely
biographical, promotional, speculative, or non-evidence-bearing narrative text.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class StemPresenceScore:
    """Computed STEM-alignment score for a paper, repository, or project."""

    score: int
    drift_score: int
    band: str
    rationale: str
    matched_domain_terms: list[str] = field(default_factory=list)
    matched_method_terms: list[str] = field(default_factory=list)
    matched_reproducibility_terms: list[str] = field(default_factory=list)
    matched_progress_terms: list[str] = field(default_factory=list)
    matched_drift_terms: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class StemPresenceScorer:
    """Score how closely a paper/project surface tracks core STEM progress.

    Scores are returned on a 0-100 scale. Higher scores indicate stronger STEM
    presence; higher drift_score values indicate more distance from core STEM
    progress. The algorithm is vocabulary based by design so that CV outputs are
    auditable and clone-safe without requiring external services.
    """

    DOMAIN_TERMS = {
        "science", "scientific", "technology", "engineering", "mathematics",
        "statistical", "statistics", "econometrics", "epidemiology", "public health",
        "biomedical", "clinical", "genomics", "radiomics", "signal", "imaging",
        "machine learning", "artificial intelligence", "model", "classifier",
        "regression", "neural", "dataset", "data", "simulation", "sensor",
        "environmental", "infrastructure", "water", "wash", "computational",
        "algorithm", "software", "reproducible", "validation", "benchmark",
    }

    METHOD_TERMS = {
        "method", "methods", "methodology", "analysis", "analytic", "estimate",
        "estimation", "identification", "causal", "inferential", "hypothesis",
        "variable", "covariate", "sample", "cohort", "panel", "longitudinal",
        "experiment", "measurement", "metric", "outcome", "feature", "training",
        "testing", "evaluation", "sensitivity", "specificity", "calibration",
        "cross-validation", "cross validation", "confidence interval", "standard error",
        "robustness", "validation", "benchmark", "protocol", "pipeline",
    }

    REPRODUCIBILITY_TERMS = {
        "reproducible", "replication", "repository", "code", "script", "notebook",
        "data dictionary", "source", "version", "release", "environment", "container",
        "makefile", "ci", "test", "unit test", "documentation", "manifest",
        "model card", "citation", "license", "artifact", "workflow", "provenance",
    }

    PROGRESS_TERMS = {
        "result", "results", "finding", "findings", "submitted", "manuscript",
        "publication", "preprint", "peer review", "abstract", "table", "figure",
        "draft", "revision", "validated", "implemented", "deployed", "generated",
        "accepted", "under review", "ready", "roadmap", "milestone", "output",
    }

    DRIFT_TERMS = {
        "memoir", "personal", "biography", "autobiography", "family history",
        "genealogy", "legacy", "symbolic", "esoteric", "myth", "mystical",
        "philosophy", "narrative", "story", "opinion", "manifesto", "advocacy",
        "promotional", "brand", "marketing", "portfolio-only", "placeholder",
        "uncurated", "intake needed", "speculative", "conceptual only",
    }

    WEIGHTS = {
        "domain": 35.0,
        "method": 30.0,
        "reproducibility": 20.0,
        "progress": 15.0,
    }

    DRIFT_PENALTY = 25.0

    def score_text(self, *parts: str | None) -> StemPresenceScore:
        """Score combined text parts and return an auditable metric object."""
        text = self._normalize(" ".join(part or "" for part in parts))
        domain = self._matches(text, self.DOMAIN_TERMS)
        method = self._matches(text, self.METHOD_TERMS)
        reproducibility = self._matches(text, self.REPRODUCIBILITY_TERMS)
        progress = self._matches(text, self.PROGRESS_TERMS)
        drift = self._matches(text, self.DRIFT_TERMS)

        raw = (
            self._coverage(domain, 5) * self.WEIGHTS["domain"]
            + self._coverage(method, 5) * self.WEIGHTS["method"]
            + self._coverage(reproducibility, 4) * self.WEIGHTS["reproducibility"]
            + self._coverage(progress, 4) * self.WEIGHTS["progress"]
        )
        penalty = self._coverage(drift, 5) * self.DRIFT_PENALTY
        score = int(round(max(0.0, min(100.0, raw - penalty))))
        drift_score = 100 - score
        band = self._band(score)
        rationale = self._rationale(score, band, domain, method, reproducibility, progress, drift)

        return StemPresenceScore(
            score=score,
            drift_score=drift_score,
            band=band,
            rationale=rationale,
            matched_domain_terms=domain,
            matched_method_terms=method,
            matched_reproducibility_terms=reproducibility,
            matched_progress_terms=progress,
            matched_drift_terms=drift,
        )

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()).strip()

    @staticmethod
    def _matches(text: str, terms: Iterable[str]) -> list[str]:
        found: list[str] = []
        for term in sorted(terms):
            escaped = re.escape(term.lower()).replace(r"\ ", r"\s+")
            if re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", text):
                found.append(term)
        return found

    @staticmethod
    def _coverage(matches: list[str], saturation: int) -> float:
        if saturation <= 0:
            return 0.0
        return min(1.0, len(matches) / saturation)

    @staticmethod
    def _band(score: int) -> str:
        if score >= 75:
            return "core_stem"
        if score >= 55:
            return "stem_adjacent"
        if score >= 35:
            return "mixed_or_transitional"
        return "low_stem_presence"

    @staticmethod
    def _rationale(
        score: int,
        band: str,
        domain: list[str],
        method: list[str],
        reproducibility: list[str],
        progress: list[str],
        drift: list[str],
    ) -> str:
        strengths = []
        if domain:
            strengths.append(f"domain terms={len(domain)}")
        if method:
            strengths.append(f"method terms={len(method)}")
        if reproducibility:
            strengths.append(f"reproducibility terms={len(reproducibility)}")
        if progress:
            strengths.append(f"progress terms={len(progress)}")
        if not strengths:
            strengths.append("limited STEM evidence terms")
        drift_note = f"; drift terms={len(drift)}" if drift else ""
        return f"{band} score {score}/100 based on {', '.join(strengths)}{drift_note}."


def score_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    score = StemPresenceScorer().score_text(path.name, text)
    return {"path": str(path), "stem_presence": score.to_dict()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score STEM presence and drift for a text/Markdown paper surface.")
    parser.add_argument("paths", nargs="*", help="Text, Markdown, or extracted-paper files to score. Reads stdin when omitted.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    if args.paths:
        payload = [score_file(Path(path)) for path in args.paths]
    else:
        text = sys.stdin.read()
        payload = [{"path": "stdin", "stem_presence": StemPresenceScorer().score_text(text).to_dict()}]

    print(json.dumps(payload, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
