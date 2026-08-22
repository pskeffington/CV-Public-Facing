#!/usr/bin/env python3
"""Contract checks for public project maturity labels.

This test imports the curator's maturity classifier and verifies the evidence
states currently used by data/pipeline_repos.json. It intentionally tests the
classification boundary rather than rendered prose.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stem_cv_curator import maturity_from_status  # noqa: E402

CASES = {
    "Publication ready / final public scholarly freeze / synthetic methodological validation": "synthetic_freeze",
    "Pre-submission manuscript cleanup / blinded-package review": "pre_submission",
    "Executable Phase 1 benchmark pathway / comparative freeze pending": "benchmark_freeze_pending",
    "Pre-analysis research scaffold / manuscript preparation": "pre_analysis",
    "Open-data manuscript scaffold / source validation": "source_validation",
    "Active source-bounded regional public-health research": "active_research",
    "Active environmental-health and spatial-equity research": "active_research",
    "Active archival, provenance, and public-history research": "active_research",
}


def main() -> int:
    failures: list[str] = []
    for status, expected in CASES.items():
        actual = maturity_from_status(status, curated=True)
        if actual != expected:
            failures.append(f"{status!r}: expected {expected!r}, got {actual!r}")

    if failures:
        print("Maturity contract failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 2

    print(f"Maturity contract passed ({len(CASES)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
