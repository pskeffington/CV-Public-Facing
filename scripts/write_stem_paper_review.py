#!/usr/bin/env python3
"""Render a Markdown review from the composite STEM paper evaluator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_paper_evaluator import StemPaperEvaluator, read_text  # noqa: E402


def clean(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


def render_review(payload: dict[str, Any], title: str = "Submitted paper") -> str:
    stem = payload.get("stem_presence", {}) if isinstance(payload.get("stem_presence"), dict) else {}
    publishing = payload.get("publishing_signal_summary", {}) if isinstance(payload.get("publishing_signal_summary"), dict) else {}
    composite = payload.get("composite_paper_score", {}) if isinstance(payload.get("composite_paper_score"), dict) else {}
    citation = payload.get("citation_verification", {}) if isinstance(citation_payload := payload.get("citation_verification"), dict) else {}
    refs = citation.get("references", []) if isinstance(citation.get("references"), list) else []
    flags = composite.get("review_flags", []) if isinstance(composite.get("review_flags"), list) else []
    provenance = publishing.get("source_provenance", []) if isinstance(publishing.get("source_provenance"), list) else []

    lines = [
        "# STEM Paper Review",
        "",
        f"Paper: {clean(title)}",
        "",
        "## Composite score",
        "",
        f"- Composite score: {composite.get('composite_score', 'n/a')}",
        f"- Composite drift score: {composite.get('composite_drift_score', 'n/a')}",
        f"- Band: `{clean(composite.get('band', 'n/a'))}`",
        f"- Rationale: {clean(composite.get('rationale', 'n/a'))}",
        "",
        "## STEM presence",
        "",
        f"- STEM score: {stem.get('score', 'n/a')}",
        f"- STEM drift score: {stem.get('drift_score', 'n/a')}",
        f"- Band: `{clean(stem.get('band', 'n/a'))}`",
        "",
        "## Publishing signal",
        "",
        f"- Reference count: {publishing.get('reference_count', 'n/a')}",
        f"- Live-verified references: {publishing.get('verified_reference_count', 'n/a')}",
        f"- Policy-blocked references: {publishing.get('policy_blocked_reference_count', 'n/a')}",
        f"- Average reference score: {publishing.get('average_reference_score', 'n/a')}",
        f"- Author signal score: {publishing.get('author_signal_score', 'n/a')}",
        f"- Author candidate count: {publishing.get('author_candidate_count', 'n/a')}",
        f"- Author match confidence: `{clean(publishing.get('author_match_confidence', 'n/a'))}`",
        f"- Author ambiguity warning: {clean(publishing.get('author_ambiguity_warning') or 'none')}",
        "",
        "## Review flags",
        "",
    ]
    if flags:
        lines.extend(f"- `{clean(flag)}`" for flag in flags)
    else:
        lines.append("- none")

    lines += ["", "## Source provenance", ""]
    if provenance:
        lines.extend(f"- `{clean(item)}`" for item in provenance)
    else:
        lines.append("- none")

    lines += [
        "",
        "## Extracted references",
        "",
        "| Type | Value | Verified | Mode | Source | Score | Band |",
        "|---|---|---:|---|---|---:|---|",
    ]
    for item in refs:
        if not isinstance(item, dict):
            continue
        reference = item.get("reference", {}) if isinstance(item.get("reference"), dict) else {}
        lines.append(
            "| "
            + " | ".join([
                clean(reference.get("reference_type", "")),
                clean(reference.get("value", "")),
                clean(item.get("verified", False)),
                clean(item.get("verification_mode", "")),
                clean(item.get("source", "")),
                clean(item.get("publishing_score", "")),
                clean(item.get("publishing_band", "")),
            ])
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a Markdown review for a STEM paper package.")
    parser.add_argument("paths", nargs="*", help="Paper text/Markdown files. Reads stdin when omitted.")
    parser.add_argument("--live", action="store_true", help="Enable live citation and author lookup.")
    parser.add_argument("--author", help="Submitter/author name for author citation lookup.")
    parser.add_argument("--orcid", help="Submitter ORCID for author citation lookup.")
    parser.add_argument("--max-author-candidates", type=int, default=5, help="Maximum OpenAlex author candidates to return in live mode.")
    parser.add_argument("--allow-url-host", action="append", default=[], help="Allow raw URL live pings only for this host or parent domain. Repeatable.")
    parser.add_argument("--block-url-host", action="append", default=[], help="Block raw URL live pings for this host or parent domain. Repeatable.")
    parser.add_argument("--title", default="Submitted paper", help="Title label for the Markdown report.")
    parser.add_argument("--out", help="Output Markdown path. Prints to stdout when omitted.")
    args = parser.parse_args()
    payload = StemPaperEvaluator(
        live=args.live,
        max_author_candidates=args.max_author_candidates,
        allowed_url_hosts=args.allow_url_host,
        blocked_url_hosts=args.block_url_host,
    ).evaluate(read_text(args.paths), author=args.author, orcid=args.orcid)
    rendered = render_review(payload, title=args.title)
    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
        print("Wrote " + args.out)
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
