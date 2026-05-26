#!/usr/bin/env python3
"""Composite paper evaluator for STEM presence, drift, and publishing signals."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_citation_verifier import DEFAULT_AUTHOR_CANDIDATES, verify_text  # noqa: E402
from stem_presence import StemPresenceScorer  # noqa: E402


@dataclass(frozen=True)
class ReviewConfiguration:
    """Configuration that produced a STEM paper review."""

    live: bool
    max_author_candidates: int
    allowed_url_hosts: list[str] = field(default_factory=list)
    blocked_url_hosts: list[str] = field(default_factory=list)
    external_services_enabled: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PublishingSignalSummary:
    """Compact publishing-signal summary for a submitted paper package."""

    reference_count: int
    verified_reference_count: int
    average_reference_score: float
    author_signal_score: int
    cited_by_count: int | None
    works_count: int | None
    h_index: int | None
    i10_index: int | None
    author_candidate_count: int = 0
    author_ambiguity_warning: str | None = None
    author_match_confidence: str = "none"
    source_provenance: list[str] = field(default_factory=list)
    policy_blocked_reference_count: int = 0


@dataclass(frozen=True)
class CompositePaperScore:
    """Combined STEM drift and publishing-context score."""

    stem_presence_score: int
    stem_drift_score: int
    publishing_signal_score: int
    composite_score: int
    composite_drift_score: int
    band: str
    rationale: str
    review_flags: list[str] = field(default_factory=list)


class StemPaperEvaluator:
    """Evaluate paper text using STEM presence and citation/publishing signals."""

    def __init__(
        self,
        live: bool = False,
        max_author_candidates: int = DEFAULT_AUTHOR_CANDIDATES,
        allowed_url_hosts: list[str] | None = None,
        blocked_url_hosts: list[str] | None = None,
    ) -> None:
        self.live = live
        self.max_author_candidates = max_author_candidates
        self.allowed_url_hosts = allowed_url_hosts or []
        self.blocked_url_hosts = blocked_url_hosts or []
        self.presence_scorer = StemPresenceScorer()

    def evaluate(self, text: str, author: str | None = None, orcid: str | None = None) -> dict[str, object]:
        stem_presence = self.presence_scorer.score_text(text)
        citation_payload = verify_text(
            text,
            live=self.live,
            author=author,
            orcid=orcid,
            max_author_candidates=self.max_author_candidates,
            allowed_url_hosts=self.allowed_url_hosts,
            blocked_url_hosts=self.blocked_url_hosts,
        )
        publishing_summary = self._summarize_publishing(citation_payload)
        composite = self._score_composite(stem_presence.score, stem_presence.drift_score, publishing_summary)
        return {
            "live": self.live,
            "review_configuration": asdict(self._review_configuration()),
            "stem_presence": stem_presence.to_dict(),
            "publishing_signal_summary": asdict(publishing_summary),
            "composite_paper_score": asdict(composite),
            "citation_verification": citation_payload,
        }

    def _review_configuration(self) -> ReviewConfiguration:
        services = ["local_stem_presence", "identifier_extractor"]
        if self.live:
            services.extend(["crossref", "ncbi_pubmed_esummary", "arxiv_api", "openalex"])
            services.append("raw_url_ping")
        return ReviewConfiguration(
            live=self.live,
            max_author_candidates=self.max_author_candidates,
            allowed_url_hosts=sorted(set(self.allowed_url_hosts)),
            blocked_url_hosts=sorted(set(self.blocked_url_hosts)),
            external_services_enabled=services,
        )

    def _summarize_publishing(self, payload: dict[str, object]) -> PublishingSignalSummary:
        references = payload.get("references", [])
        if not isinstance(references, list):
            references = []
        scores: list[int] = []
        source_provenance: list[str] = []
        policy_blocked_count = 0
        for item in references:
            if isinstance(item, dict):
                try:
                    scores.append(int(item.get("publishing_score", 0)))
                except (TypeError, ValueError):
                    scores.append(0)
                source = str(item.get("source", "reference_source_unknown"))
                mode = str(item.get("verification_mode", "mode_unknown"))
                source_provenance.append(f"reference:{source}:{mode}")
                signals = item.get("signals", [])
                if mode == "live_policy_blocked" or (isinstance(signals, list) and "url_policy_blocked" in signals):
                    policy_blocked_count += 1
        average_reference_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        author_profile = payload.get("author_citation_profile")
        if not isinstance(author_profile, dict):
            author_profile = {}
        if author_profile:
            source = str(author_profile.get("source", "author_source_unknown"))
            confidence = str(author_profile.get("author_match_confidence", "none"))
            source_provenance.append(f"author_profile:{source}:{confidence}")
        return PublishingSignalSummary(
            reference_count=int(payload.get("reference_count", 0) or 0),
            verified_reference_count=int(payload.get("verified_reference_count", 0) or 0),
            average_reference_score=average_reference_score,
            author_signal_score=self._safe_int(author_profile.get("author_signal_score"), 0),
            cited_by_count=self._safe_optional_int(author_profile.get("cited_by_count")),
            works_count=self._safe_optional_int(author_profile.get("works_count")),
            h_index=self._safe_optional_int(author_profile.get("h_index")),
            i10_index=self._safe_optional_int(author_profile.get("i10_index")),
            author_candidate_count=self._safe_int(author_profile.get("candidate_count"), 0),
            author_ambiguity_warning=str(author_profile.get("ambiguity_warning")) if author_profile.get("ambiguity_warning") else None,
            author_match_confidence=str(author_profile.get("author_match_confidence", "none")),
            source_provenance=sorted(set(source_provenance)),
            policy_blocked_reference_count=policy_blocked_count,
        )

    def _score_composite(
        self,
        stem_score: int,
        stem_drift_score: int,
        publishing: PublishingSignalSummary,
    ) -> CompositePaperScore:
        citation_bonus = min(100, int(round(publishing.average_reference_score * 0.65 + publishing.author_signal_score * 0.35)))
        composite_score = int(round(stem_score * 0.75 + citation_bonus * 0.25))
        composite_score = max(0, min(100, composite_score))
        composite_drift_score = 100 - composite_score
        band = self._band(composite_score)
        review_flags = self._review_flags(stem_drift_score, publishing)
        rationale = (
            f"{band} composite score {composite_score}/100 from STEM presence {stem_score}/100, "
            f"STEM drift {stem_drift_score}/100, {publishing.reference_count} extracted references, "
            f"{publishing.verified_reference_count} live-verified references, author signal "
            f"{publishing.author_signal_score}/100, {publishing.author_candidate_count} author candidates, "
            f"author match confidence {publishing.author_match_confidence}, and "
            f"{publishing.policy_blocked_reference_count} policy-blocked references."
        )
        if publishing.author_ambiguity_warning:
            rationale += " Author identity requires review."
        return CompositePaperScore(
            stem_presence_score=stem_score,
            stem_drift_score=stem_drift_score,
            publishing_signal_score=citation_bonus,
            composite_score=composite_score,
            composite_drift_score=composite_drift_score,
            band=band,
            rationale=rationale,
            review_flags=review_flags,
        )

    @staticmethod
    def _review_flags(stem_drift_score: int, publishing: PublishingSignalSummary) -> list[str]:
        flags: list[str] = []
        if stem_drift_score >= 45:
            flags.append("high_stem_drift")
        if publishing.reference_count == 0:
            flags.append("no_references_extracted")
        if publishing.reference_count > 0 and publishing.verified_reference_count == 0:
            flags.append("references_not_live_verified")
        if publishing.policy_blocked_reference_count > 0:
            flags.append("reference_url_policy_blocked")
        if publishing.author_ambiguity_warning or publishing.author_match_confidence == "name_multiple_candidates":
            flags.append("author_identity_ambiguous")
        if publishing.author_signal_score == 0:
            flags.append("no_verified_author_signal")
        if publishing.author_match_confidence in {"offline_unverified", "lookup_error", "no_match", "none"}:
            flags.append("author_match_unconfirmed")
        return flags

    @staticmethod
    def _safe_int(value: object, default: int) -> int:
        try:
            return int(value) if value is not None else default
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_optional_int(value: object) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _band(score: int) -> str:
        if score >= 80:
            return "strong_stem_paper_package"
        if score >= 60:
            return "credible_stem_paper_package"
        if score >= 40:
            return "mixed_or_underverified_package"
        return "high_drift_or_low_evidence_package"


def read_text(paths: list[str]) -> str:
    if paths:
        return "\n".join(Path(path).read_text(encoding="utf-8", errors="replace") for path in paths)
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a paper package for STEM presence, drift, citations, and author publishing signals.")
    parser.add_argument("paths", nargs="*", help="Paper text/Markdown files. Reads stdin when omitted.")
    parser.add_argument("--live", action="store_true", help="Enable live citation and author lookup.")
    parser.add_argument("--author", help="Submitter/author name for author citation lookup.")
    parser.add_argument("--orcid", help="Submitter ORCID for author citation lookup.")
    parser.add_argument("--max-author-candidates", type=int, default=DEFAULT_AUTHOR_CANDIDATES, help="Maximum OpenAlex author candidates to return in live mode.")
    parser.add_argument("--allow-url-host", action="append", default=[], help="Allow raw URL live pings only for this host or parent domain. Repeatable.")
    parser.add_argument("--block-url-host", action="append", default=[], help="Block raw URL live pings for this host or parent domain. Repeatable.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()
    payload = StemPaperEvaluator(
        live=args.live,
        max_author_candidates=args.max_author_candidates,
        allowed_url_hosts=args.allow_url_host,
        blocked_url_hosts=args.block_url_host,
    ).evaluate(read_text(args.paths), author=args.author, orcid=args.orcid)
    print(json.dumps(payload, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
