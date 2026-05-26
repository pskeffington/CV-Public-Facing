#!/usr/bin/env python3
"""Citation verification and publishing-signal scoring for STEM drift review."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

USER_AGENT = "stem-cv-curator-citation-verifier/0.1"
OPENALEX_AUTHOR_URL = "https://api.openalex.org/authors"
CROSSREF_WORK_URL = "https://api.crossref.org/works/"


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

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["reference"]["canonical_url"] = self.reference.canonical_url
        return payload


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
    note: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


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
        )

    def _verify_doi(self, reference: CitationReference) -> CitationVerification:
        endpoint = CROSSREF_WORK_URL + urllib.parse.quote(reference.value, safe="")
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
        return CitationVerification(reference, ok, status, score, self._band(score), citation_count, signals)

    def _verify_url_like(self, reference: CitationReference) -> CitationVerification:
        ok, status = self._ping(reference.canonical_url)
        score = self._score_reference(reference.reference_type, ok, None)
        signals = [reference.reference_type + "_extracted"]
        if ok:
            signals.append("endpoint_reachable")
        return CitationVerification(reference, ok, status, score, self._band(score), None, signals)

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
    def __init__(self, live: bool = False, timeout: int = 12) -> None:
        self.live = live
        self.timeout = timeout

    def lookup(self, name: str | None = None, orcid: str | None = None) -> AuthorCitationProfile | None:
        if not name and not orcid:
            return None
        if not self.live:
            return AuthorCitationProfile(name, orcid, None, None, "openalex", False, note="Run with --live for author citation counts.")
        params: dict[str, str] = {"per-page": "1"}
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
            return AuthorCitationProfile(name, orcid, None, None, "openalex", False, note=str(exc))
        results = payload.get("results", []) if isinstance(payload, dict) else []
        if not results:
            return AuthorCitationProfile(name, orcid, None, None, "openalex", False, note="No OpenAlex author match found.")
        author = results[0]
        stats = author.get("summary_stats", {}) if isinstance(author.get("summary_stats"), dict) else {}
        cited_by_count = self._safe_int(author.get("cited_by_count"))
        works_count = self._safe_int(author.get("works_count"))
        h_index = self._safe_int(stats.get("h_index"))
        i10_index = self._safe_int(stats.get("i10_index"))
        score = self._score_author(cited_by_count, works_count, h_index)
        return AuthorCitationProfile(
            name,
            orcid,
            str(author.get("display_name", "")) or None,
            str(author.get("id", "")) or None,
            "openalex",
            True,
            cited_by_count,
            works_count,
            h_index,
            i10_index,
            score,
        )

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


def verify_text(text: str, live: bool = False, author: str | None = None, orcid: str | None = None) -> dict[str, object]:
    refs = CitationExtractor().extract(text)
    verifier = CitationVerifier(live=live)
    verified = [verifier.verify(ref).to_dict() for ref in refs]
    author_profile = AuthorCitationLookup(live=live).lookup(author, orcid)
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
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()
    if args.paths:
        text = "\n".join(Path(path).read_text(encoding="utf-8", errors="replace") for path in args.paths)
    else:
        import sys
        text = sys.stdin.read()
    payload = verify_text(text, live=args.live, author=args.author, orcid=args.orcid)
    print(json.dumps(payload, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
