#!/usr/bin/env python3
"""Evidence-bounded maturity classification for public research objects."""

from __future__ import annotations


def maturity_from_status(status: str, curated: bool) -> str:
    """Map curated status prose to stable public maturity labels.

    Specific evidence states are evaluated before broad legacy terms so a
    frozen synthetic package, pre-submission manuscript, or pending benchmark
    freeze is not flattened into a generic active scaffold.
    """

    lower = status.lower()

    if "final public scholarly freeze" in lower or (
        "synthetic" in lower and "freeze" in lower and "validation" in lower
    ):
        return "synthetic_freeze"

    if "pre-submission" in lower or "blinded-package review" in lower:
        return "pre_submission"

    if "benchmark" in lower and "freeze pending" in lower:
        return "benchmark_freeze_pending"

    if "pre-analysis" in lower:
        return "pre_analysis"

    if "source validation" in lower or "source-validation" in lower:
        return "source_validation"

    if "submitted" in lower or "peer review" in lower:
        return "submitted"

    if "publication" in lower and "ready" in lower:
        return "publication_ready"

    if "manuscript" in lower and "active" in lower:
        return "active_manuscript"

    if "validation" in lower:
        return "validation_gated"

    if "early" in lower:
        return "early_stage"

    if "active" in lower:
        return "active_research"

    if curated:
        return "active_scaffold"

    return "intake"
