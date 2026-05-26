#!/usr/bin/env python3
"""Deterministic smoke checks for citation verification components."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_citation_verifier import CitationExtractor, verify_text  # noqa: E402


@dataclass(frozen=True)
class CitationVerifierCheckResult:
    passed: bool
    errors: list[str]
    reference_count: int
    author_profile_present: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "reference_count": self.reference_count,
            "author_profile_present": self.author_profile_present,
        }


class CitationVerifierCheck:
    """Offline-safe contract checks for citation extraction and author-profile shape."""

    FIXTURE = " ".join([
        "This manuscript cites DOI 10.1038/nature12373,",
        "arXiv:2101.00001, PMID: 23803847,",
        "and https://example.org/reproducibility-manifest.",
    ])

    def run(self) -> CitationVerifierCheckResult:
        errors: list[str] = []
        references = CitationExtractor().extract(self.FIXTURE)
        by_type = {reference.reference_type for reference in references}
        for expected in {"doi", "arxiv", "pmid", "url"}:
            if expected not in by_type:
                errors.append(f"Missing extracted reference type: {expected}")

        payload = verify_text(self.FIXTURE, live=False, author="Example Submitter")
        if payload.get("live") is not False:
            errors.append("Offline verification payload should have live=false")
        if payload.get("reference_count") != 4:
            errors.append(f"Expected four references, found {payload.get('reference_count')}")
        if payload.get("verified_reference_count") != 0:
            errors.append("Offline verifier should not mark references as live-verified")
        profile = payload.get("author_citation_profile")
        if not isinstance(profile, dict):
            errors.append("Missing offline author citation profile")
        else:
            if profile.get("verified") is not False:
                errors.append("Offline author profile should be unverified")
            if profile.get("author_signal_score") != 0:
                errors.append("Offline author signal score should be zero")
            if profile.get("candidate_count") != 0:
                errors.append("Offline author candidate_count should be zero")
            if profile.get("candidates") != []:
                errors.append("Offline author candidates should be an empty list")
            if profile.get("ambiguity_warning") is not None:
                errors.append("Offline author ambiguity_warning should be null")

        return CitationVerifierCheckResult(not errors, errors, len(references), isinstance(profile, dict))


def main() -> int:
    result = CitationVerifierCheck().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
