#!/usr/bin/env python3
"""Smoke checks for the STEM presence scoring metric."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_presence import StemPresenceScorer  # noqa: E402


class StemPresenceCheck:
    """Small deterministic test harness for CI and local Makefile checks."""

    def __init__(self) -> None:
        self.scorer = StemPresenceScorer()

    def core_stem_fixture(self) -> str:
        return (
            "This manuscript reports public health epidemiology methods using a "
            "longitudinal dataset, regression analysis, validation, benchmark "
            "metrics, reproducible code, repository documentation, results, "
            "tables, and a submitted manuscript workflow."
        )

    def drift_fixture(self) -> str:
        return (
            "This personal biography is a symbolic narrative memoir and promotional "
            "portfolio-only placeholder with speculative esoteric framing and no "
            "dataset, method, analysis, validation, code, or measurable result."
        )

    def run(self) -> dict[str, object]:
        core = self.scorer.score_text(self.core_stem_fixture())
        drift = self.scorer.score_text(self.drift_fixture())
        checks = {
            "core_score_at_least_75": core.score >= 75,
            "core_band_is_core_stem": core.band == "core_stem",
            "drift_score_below_core": drift.score < core.score,
            "drift_has_matched_drift_terms": bool(drift.matched_drift_terms),
        }
        return {
            "passed": all(checks.values()),
            "checks": checks,
            "core_fixture": core.to_dict(),
            "drift_fixture": drift.to_dict(),
        }


def main() -> int:
    result = StemPresenceCheck().run()
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
