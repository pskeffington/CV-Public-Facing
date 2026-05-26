#!/usr/bin/env python3
"""Citation verification and publishing-signal scoring for STEM drift review."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "stem-cv-curator-citation-verifier/0.3"
OPENALEX_AUTHOR_URL = "https://api.openalex.org/authors"
CROSSREF_WORK_URL = "https://api.crossref.org/works/"
DEFAULT_AUTHOR_CANDIDATES = 5


def checked_at_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass(frozen=True)
class CitationReference:
    reference_type: str
    value: str
    source_hint: str = "text"

    @property
    def canonical_url(self) -> str:
        if self.reference_type == "doi":
            return "https://doi.org/" + self.value
        if self.reference_type == "arxiv":
            return "https://arxiv.org/abs/" + self.value
        if self.reference_type == "pmid":
            return "https://pubmed.ncbi.nlm.nih.gov/" + self.value + "/"
        return self.value


@dataclass(frozen=True)
class CitationVerification:
    reference: CitationReference
    verified: bool
    status_code: int | None
    publishing_score: int
    publishing_band: str
    citation_count: int | None = None
    signals: list[str] = field(default_factory=list)
    note: str | None = None
    source: str = "identifier_extractor"
    endpoint: str | None = None
    checked_at: str | None = None
    verification_mode: str = "offline"

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["reference"]["canonical_url"] = self.reference.canonical_url
        return payload


@dataclass(frozen=True)
class AuthorCandidate:
    matched_name: str | None
    author_id: str | None
    cited_by_count: int | None = None
    works_count: int | None = None
    h_index: int | None = None
    i10_index: int | None = None
    author_signal_score: int = 0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class AuthorCitationProfile:
    query_name: str | None
    query_orcid: str | None
    matched_name: str | None
    author_id: str | None
    source: str
    verified: bool
    cited_by_count: int | None = None
    works_count: int | None = None
    h_index: int | None = None
    i10_index: int | None = None
    author_signal_score: int = 0
    candidate_count: int = 0
    candidates: list[AuthorCandidate] = field(default_factory=list)
    ambiguity_warning: str | None = None
    note: str | None = None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["candidates"] = [candidate.to_dict() if hasattr(candidate, "to_dict") else candidate for candidate in self.candidates]
        return payload


class CitationExtractor:
    DOI_RE = re.compile(r"(?i)\b10\.\d{4,9}/[-._;()/:A-Z0-9]+")
    ARXIV_RE = re.compile(r"(?i)\barXiv[:\s]+(\d{4}\.\d{4,5}(?:v\d+)?|[a-z\-]+/\d{7}(?:v\d+)?)")
    PMID_RE = re.compile(r"(?i)\bPMID[:\s]*(\d{6,9})\b")
    URL_RE = re.compile(r"https?://[^\s)\]>}]+")

    def extract(self, text: str) -> list[CitationReference]:
        refs: list[CitationReference] = []
        seen: set[tuple[str, str]] = set()
        for reference_type, values in [
            ("doi", self.DOI_RE.findall(text)),
            ("arxiv", self.ARXIV_RE.findall(text)),
            ("pmid", self.PMID_RE.findall(text)),
            ("url", self.URL_RE.findall(text)),
        ]:
            for raw in values:
                value = self._normalize(reference_type, raw)
                key = (reference_type, value.lower())
                if key not in seen:
                    seen.add(key)
                    refs.append(CitationReference(reference_type, value))
        return refs

    @staticmethod
    def _normalize(reference_type: str, raw: str) -> str:
        value = raw.strip().rstrip(".,;:")
        if reference_type == "doi":
            value = value.lower()
        return value


class CitationVerifier:
    def __init__(self, live: bool = False, timeout: int = 12) -> None:
        self.live = live
        self.timeout = timeout

    def verify(self, reference: CitationReference) -> CitationVerification:
        if not self.live:
            return self._offline(reference)
        if reference.reference_type == "doi":
            return self._verify_doi(reference)
        return self._verify_url_like(reference)

    def _offline(self, reference: CitationReference) -> CitationVerification:
        score = {"doi": 55, "pmid": 50, "arxiv": 45, "url": 25}.get(reference.reference_type, 15)
        return CitationVerification(
            reference=reference,
            verified=False,
            status_code=None,
            publishing_score=score,
            publishing_band=self._band(score),
            signals=["identifier_extracted", "live_verification_not_requested"],
            note="Run with --live to ping citation endpoints.",
            source="identifier_extractor",
            endpoint=None,
            checked_at=checked_at_utc(),
            verification_mode="offline",
        )

    def _verify_doi(self, reference: CitationReference) -> CitationVerification:
        endpoint = CROSSREF_WORK_URL + urllib.parse.quote(reference.value, safe="")
        checked_at = checked_at_utc()
        ok, status, payload = self._request_json(endpoint)
        citation_count = None
        signals = ["doi_extracted"]
        if ok and isinstance(payload, dict):
            message = payload.get("message", {})
            if isinstance(message, dict):
                citation_count = self._safe_int(message.get("is-referenced-by-count"))
                signals.append("crossref_metadata_found")
                if citation_count is not None:
                    signals.append("crossref_cited_by_count_found")
        score = self._score_reference(reference.reference_type, ok, citation_count)
        return CitationVerification(
            reference=reference,
            verified=ok,
            status_code=status,
            publishing_score=score,
            publishing_band=self._band(score),
            citation_count=citation_count,
            signals=signals,
            source="crossref",
            endpoint=endpoint,
            checked_at=checked_at,
            verification_mode="live",
        )

    def _verify_url_like(self, reference: CitationReference) -> CitationVerification:
        endpoint = reference.canonical_url
        checked_at = checked_at_utc()
        ok, status = self._ping(endpoint)
        score = self._score_reference(reference.reference_type, ok, None)
        signals = [reference.reference_type + "_extracted"]
        if ok:
            signals.append("endpoint_reachable")
        return CitationVerification(
            reference=reference,
            verified=ok,
            status_code=status,
            publishing_score=score,
            publishing_band=self._band(score),
            citation_count=None,
            signals=signals,
            source=self._source_for_reference(reference.reference_type),
            endpoint=endpoint,
            checked_at=checked_at,
            verification_mode="live",
        )

    def _request_json(self, url: str) -> tuple[bool, int | None, Any]:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                return True, int(res.status), json.loads(res.read().decode("utf-8", errors="replace"))
        except Exception as exc:
            status = getattr(exc, "code", None)
            return False, status if isinstance(status, int) else None, None

    def _ping(self, url: str) -> tuple[bool, int | None]:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                return 200 <= int(res.status) < 400, int(res.status)
        except Exception as exc:
            status = getattr(exc, "code", None)
            return False, status if isinstance(status, int) else None

    @staticmethod
    def _source_for_reference(reference_type: str) -> str:
        return {
            "pmid": "pubmed_endpoint",
            "arxiv": "arxiv_endpoint",
            "url": "url_endpoint",
        }.get(reference_type, "reference_endpoint")

    @staticmethod
    def _safe_int(value: object) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _score_reference(reference_type: str, verified: bool, citation_count: int | None) -> int:
        score = {"doi": 65, "pmid": 60, "arxiv": 55, "url": 35}.get(reference_type, 20)
        if verified:
            score += 15
        if citation_count is not None:
            if citation_count >= 100:
                score += 20
            elif citation_count >= 25:
                score += 15
            elif citation_count >= 5:
                score += 10
            elif citation_count >= 1:
                score += 5
        return max(0, min(100, score))

    @staticmethod
    def _band(score: int) -> str:
        if score >= 80:
            return "strong_publishing_signal"
        if score >= 60:
            return "moderate_publishing_signal"
        if score >= 35:
            return "weak_or_unverified_signal"
        return "low_publishing_signal"


class AuthorCitationLookup:
    def __init__(self, live: bool = False, timeout: int = 12, max_candidates: int = DEFAULT_AUTHOR_CANDIDATES) -> None:
        self.live = live
        self.timeout = timeout
        self.max_candidates = max(1, max_candidates)

    def lookup(self, name: str | None = None, orcid: str | None = None) -> AuthorCitationProfile | None:
        if not name and not orcid:
            return None
        if not self.live:
            return AuthorCitationProfile(
                name,
                orcid,
                None,
                None,
                "openalex",
                False,
                candidate_count=0,
                candidates=[],
                note="Run with --live for author citation counts and candidate disambiguation.",
            )
        payload = self._query_openalex(name, orcid)
        if isinstance(payload, str):
            return AuthorCitationProfile(name, orcid, None, None, "openalex", False, note=payload)
        results = payload.get("results", []) if isinstance(payload, dict) else []
        if not results:
            return AuthorCitationProfile(name, orcid, None, None, "openalex", False, note="No OpenAlex author match found.")
        candidates = [self._candidate_from_author(author) for author in results if isinstance(author, dict)]
        top = candidates[0]
        ambiguity_warning = self._ambiguity_warning(name, orcid, candidates)
        return AuthorCitationProfile(
            name,
            orcid,
            top.matched_name,
            top.author_id,
            "openalex",
            True,
            top.cited_by_count,
            top.works_count,
            top.h_index,
            top.i10_index,
            top.author_signal_score,
            candidate_count=len(candidates),
            candidates=candidates,
            ambiguity_warning=ambiguity_warning,
        )

    def _query_openalex(self, name: str | None, orcid: str | None) -> dict[str, Any] | str:
        params: dict[str, str] = {"per-page": str(self.max_candidates)}
        if orcid:
            params["filter"] = "orcid:" + orcid
        elif name:
            params["search"] = name
        url = OPENALEX_AUTHOR_URL + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                payload = json.loads(res.read().decode("utf-8", errors="replace"))
        except Exception as exc:
            return str(exc)
        return payload if isinstance(payload, dict) else "OpenAlex returned a non-object payload."

    def _candidate_from_author(self, author: dict[str, Any]) -> AuthorCandidate:
        stats = author.get("summary_stats", {}) if isinstance(author.get("summary_stats"), dict) else {}
        cited_by_count = self._safe_int(author.get("cited_by_count"))
        works_count = self._safe_int(author.get("works_count"))
        h_index = self._safe_int(stats.get("h_index"))
        i10_index = self._safe_int(stats.get("i10_index"))
        return AuthorCandidate(
            matched_name=str(author.get("display_name", "")) or None,
            author_id=str(author.get("id", "")) or None,
            cited_by_count=cited_by_count,
            works_count=works_count,
            h_index=h_index,
            i10_index=i10_index,
            author_signal_score=self._score_author(cited_by_count, works_count, h_index),
        )

    @staticmethod
    def _ambiguity_warning(name: str | None, orcid: str | None, candidates: list[AuthorCandidate]) -> str | None:
        if orcid:
            return None
        if len(candidates) <= 1:
            return None
        top_names = ", ".join(candidate.matched_name or "unknown" for candidate in candidates[:3])
        return f"OpenAlex returned {len(candidates)} author candidates for {name or 'query'}; review identity match before using author metrics. Top candidates: {top_names}."

    @staticmethod
    def _safe_int(value: object) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _score_author(citations: int | None, works: int | None, h_index: int | None) -> int:
        score = 0
        if citations is not None:
            if citations >= 1000:
                score += 45
            elif citations >= 250:
                score += 35
            elif citations >= 50:
                score += 25
            elif citations >= 10:
                score += 15
            elif citations >= 1:
                score += 8
        if works is not None:
            score += min(25, works * 2)
        if h_index is not None:
            score += min(30, h_index * 3)
        return max(0, min(100, score))


def verify_text(text: str, live: bool = False, author: str | None = None, orcid: str | None = None, max_author_candidates: int = DEFAULT_AUTHOR_CANDIDATES) -> dict[str, object]:
    refs = CitationExtractor().extract(text)
    verifier = CitationVerifier(live=live)
    verified = [verifier.verify(ref).to_dict() for ref in refs]
    author_profile = AuthorCitationLookup(live=live, max_candidates=max_author_candidates).lookup(author, orcid)
    return {
        "live": live,
        "reference_count": len(refs),
        "verified_reference_count": sum(1 for item in verified if item.get("verified")),
        "author_citation_profile": author_profile.to_dict() if author_profile else None,
        "references": verified,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract and optionally verify STEM citations and author citation counts.")
    parser.add_argument("paths", nargs="*", help="Text/Markdown files to inspect. Reads stdin when omitted.")
    parser.add_argument("--live", action="store_true", help="Ping DOI/arXiv/PubMed/URL endpoints and query OpenAlex author counts.")
    parser.add_argument("--author", help="Submitter/author name for OpenAlex author citation lookup.")
    parser.add_argument("--orcid", help="Submitter ORCID for OpenAlex author citation lookup.")
    parser.add_argument("--max-author-candidates", type=int, default=DEFAULT_AUTHOR_CANDIDATES, help="Maximum OpenAlex author candidates to return in live mode.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()
    if args.paths:
        text = "\n".join(Path(path).read_text(encoding="utf-8", errors="replace") for path in args.paths)
    else:
        import sys
        text = sys.stdin.read()
    payload = verify_text(text, live=args.live, author=args.author, orcid=args.orcid, max_author_candidates=args.max_author_candidates)
    print(json.dumps(payload, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
