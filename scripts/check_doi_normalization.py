#!/usr/bin/env python3
"""Deterministic DOI extraction and normalization checks."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_citation_verifier import CitationExtractor  # noqa: E402


@dataclass(frozen=True)
class DoiNormalizationCheckResult:
    passed: bool
    errors: list[str]
    dois: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "dois": self.dois,
        }


class DoiNormalizationCheck:
    FIXTURE = " ".join([
        "Bare DOI 10.1000/XYZ123.",
        "DOI label doi:10.1000/ABC.Def;",
        "HTTPS DOI https://doi.org/10.1000/Mixed.Case).",
        "DX DOI http://dx.doi.org/10.1000/Legacy-Path,",
        "Quoted DOI \"10.1000/Quoted.Value\".",
    ])

    EXPECTED = {
        "10.1000/xyz123",
        "10.1000/abc.def",
        "10.1000/mixed.case",
        "10.1000/legacy-path",
        "10.1000/quoted.value",
    }

    def run(self) -> DoiNormalizationCheckResult:
        errors: list[str] = []
        refs = CitationExtractor().extract(self.FIXTURE)
        dois = sorted(ref.value for ref in refs if ref.reference_type == "doi")
        found = set(dois)
        missing = sorted(self.EXPECTED - found)
        unexpected = sorted(found - self.EXPECTED)
        if missing:
            errors.append("Missing normalized DOI values: " + ", ".join(missing))
        if unexpected:
            errors.append("Unexpected DOI values: " + ", ".join(unexpected))
        if len(dois) != len(self.EXPECTED):
            errors.append(f"Expected {len(self.EXPECTED)} DOI values, found {len(dois)}")
        return DoiNormalizationCheckResult(not errors, errors, dois)


def main() -> int:
    result = DoiNormalizationCheck().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
