#!/usr/bin/env python3
"""Citation verification and publishing-signal scoring for STEM drift review."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "stem-cv-curator-citation-verifier/0.8"
OPENALEX_AUTHOR_URL = "https://api.openalex.org/authors"
CROSSREF_WORK_URL = "https://api.crossref.org/works/"
PUBMED_ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
ARXIV_API_URL = "https://export.arxiv.org/api/query"
DEFAULT_AUTHOR_CANDIDATES = 5


def checked_at_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def normalize_host(host: str | None) -> str:
    return (host or "").strip().lower().lstrip(".")


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
    metadata: dict[str, object] | None = None

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
    author_match_confidence: str = "none"
    note: str | None = None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["candidates"] = [candidate.to_dict() if hasattr(candidate, "to_dict") else candidate for candidate in self.candidates]
        return payload


class CitationExtractor:
    DOI_RE = re.compile(r"(?i)(?:https?://(?:dx\.)?doi\.org/|doi:\s*)?(10\.\d{4,9}/[-._;()/:A-Z0-9]+)")
    ARXIV_RE = re.compile(r"(?i)\barXiv[:\s]+(\d{4}\.\d{4,5}(?:v\d+)?|[a-z\-]+/\d{7}(?:v\d+)?)")
    PMID_RE = re.compile(r"(?i)\bPMID[:\s]*(\d{6,9})\b")
    URL_RE = re.compile(r"https?://[^\s)\]>}]+")
    DOI_TRAILING_CHARS = " .,!?:;)]}>\"'"

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

    @classmethod
    def _normalize(cls, reference_type: str, raw: str) -> str:
        value = raw.strip()
        if reference_type == "doi":
            value = re.sub(r"(?i)^https?://(?:dx\.)?doi\.org/", "", value)
            value = re.sub(r"(?i)^doi:\s*", "", value)
            value = value.rstrip(cls.DOI_TRAILING_CHARS)
            return value.lower()
        return value.rstrip(".,;:")


class CitationVerifier:
    def __init__(
        self,
        live: bool = False,
        timeout: int = 12,
        allowed_url_hosts: list[str] | None = None,
        blocked_url_hosts: list[str] | None = None,
    ) -> None:
        self.live = live
        self.timeout = timeout
        self.allowed_url_hosts = {normalize_host(host) for host in (allowed_url_hosts or []) if normalize_host(host)}
        self.blocked_url_hosts = {normalize_host(host) for host in (blocked_url_hosts or []) if normalize_host(host)}

    def verify(self, reference: CitationReference) -> CitationVerification:
        if not self.live:
            return self._offline(reference)
        if reference.reference_type == "doi":
            return self._verify_doi(reference)
        if reference.reference_type == "pmid":
            return self._verify_pmid(reference)
        if reference.reference_type == "arxiv":
            return self._verify_arxiv(reference)
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
            metadata=None,
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
            metadata=None,
        )

    def _verify_pmid(self, reference: CitationReference) -> CitationVerification:
        params = {"db": "pubmed", "id": reference.value, "retmode": "json"}
        endpoint = PUBMED_ESUMMARY_URL + "?" + urllib.parse.urlencode(params)
        checked_at = checked_at_utc()
        ok, status, payload = self._request_json(endpoint)
        metadata = self._pubmed_metadata(reference.value, payload) if ok else None
        verified = bool(metadata)
        signals = ["pmid_extracted"]
        if verified:
            signals.append("pubmed_esummary_metadata_found")
        score = self._score_reference(reference.reference_type, verified, None)
        return CitationVerification(
            reference=reference,
            verified=verified,
            status_code=status,
            publishing_score=score,
            publishing_band=self._band(score),
            citation_count=None,
            signals=signals,
            source="ncbi_pubmed_esummary",
            endpoint=endpoint,
            checked_at=checked_at,
            verification_mode="live",
            metadata=metadata,
        )

    def _verify_arxiv(self, reference: CitationReference) -> CitationVerification:
        arxiv_id = self._arxiv_id_without_version(reference.value)
        endpoint = ARXIV_API_URL + "?" + urllib.parse.urlencode({"id_list": arxiv_id})
        checked_at = checked_at_utc()
        ok, status, xml_text = self._request_text(endpoint)
        metadata = self._arxiv_metadata(reference.value, xml_text) if ok else None
        verified = bool(metadata)
        signals = ["arxiv_extracted"]
        if verified:
            signals.append("arxiv_metadata_found")
        score = self._score_reference(reference.reference_type, verified, None)
        return CitationVerification(
            reference=reference,
            verified=verified,
            status_code=status,
            publishing_score=score,
            publishing_band=self._band(score),
            citation_count=None,
            signals=signals,
            source="arxiv_api",
            endpoint=endpoint,
            checked_at=checked_at,
            verification_mode="live",
            metadata=metadata,
        )

    def _verify_url_like(self, reference: CitationReference) -> CitationVerification:
        endpoint = reference.canonical_url
        checked_at = checked_at_utc()
        allowed, reason = self._raw_url_allowed(endpoint)
        if not allowed:
            score = self._score_reference(reference.reference_type, False, None)
            return CitationVerification(
                reference=reference,
                verified=False,
                status_code=None,
                publishing_score=score,
                publishing_band=self._band(score),
                citation_count=None,
                signals=[reference.reference_type + "_extracted", "url_policy_blocked"],
                note=reason,
                source=self._source_for_reference(reference.reference_type),
                endpoint=endpoint,
                checked_at=checked_at,
                verification_mode="live_policy_blocked",
                metadata=None,
            )
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
            metadata=None,
        )

    def _raw_url_allowed(self, url: str) -> tuple[bool, str | None]:
        if not self.allowed_url_hosts and not self.blocked_url_hosts:
            return True, None
        host = normalize_host(urllib.parse.urlparse(url).hostname)
        if not host:
            return False, "URL host could not be parsed; live URL ping skipped."
        if self._host_matches(host, self.blocked_url_hosts):
            return False, f"URL host {host} is blocked by live URL policy."
        if self.allowed_url_hosts and not self._host_matches(host, self.allowed_url_hosts):
            return False, f"URL host {host} is not in the live URL allowlist."
        return True, None

    @staticmethod
    def _host_matches(host: str, patterns: set[str]) -> bool:
        return any(host == pattern or host.endswith("." + pattern) for pattern in patterns)

    def _request_json(self, url: str) -> tuple[bool, int | None, Any]:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                return True, int(res.status), json.loads(res.read().decode("utf-8", errors="replace"))
        except Exception as exc:
            status = getattr(exc, "code", None)
            return False, status if isinstance(status, int) else None, None

    def _request_text(self, url: str) -> tuple[bool, int | None, str | None]:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml,text/xml,*/*"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                return True, int(res.status), res.read().decode("utf-8", errors="replace")
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
    def _pubmed_metadata(pmid: str, payload: Any) -> dict[str, object] | None:
        if not isinstance(payload, dict):
            return None
        result = payload.get("result")
        if not isinstance(result, dict):
            return None
        item = result.get(pmid)
        if not isinstance(item, dict):
            return None
        authors = []
        raw_authors = item.get("authors", [])
        if isinstance(raw_authors, list):
            for author in raw_authors[:10]:
                if isinstance(author, dict) and author.get("name"):
                    authors.append(str(author.get("name")))
        article_ids = {}
        raw_ids = item.get("articleids", [])
        if isinstance(raw_ids, list):
            for article_id in raw_ids:
                if isinstance(article_id, dict) and article_id.get("idtype") and article_id.get("value"):
                    article_ids[str(article_id.get("idtype"))] = str(article_id.get("value"))
        return {
            "pmid": pmid,
            "title": item.get("title"),
            "journal": item.get("fulljournalname") or item.get("source"),
            "publication_date": item.get("pubdate"),
            "publication_year": CitationVerifier._publication_year(item.get("pubdate")),
            "authors": authors,
            "doi": article_ids.get("doi"),
            "pmcid": article_ids.get("pmc"),
            "publication_types": item.get("pubtype", []),
        }

    @staticmethod
    def _arxiv_metadata(arxiv_id: str, xml_text: str | None) -> dict[str, object] | None:
        if not xml_text:
            return None
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return None
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None
        authors = []
        for author in entry.findall("atom:author", ns)[:10]:
            name = author.findtext("atom:name", default="", namespaces=ns).strip()
            if name:
                authors.append(name)
        categories = []
        for category in entry.findall("atom:category", ns):
            term = category.attrib.get("term")
            if term:
                categories.append(term)
        doi = entry.findtext("arxiv:doi", default="", namespaces=ns).strip() or None
        journal_ref = entry.findtext("arxiv:journal_ref", default="", namespaces=ns).strip() or None
        return {
            "arxiv_id": arxiv_id,
            "canonical_arxiv_id": CitationVerifier._arxiv_id_without_version(arxiv_id),
            "title": CitationVerifier._collapse_ws(entry.findtext("atom:title", default="", namespaces=ns)),
            "abstract": CitationVerifier._collapse_ws(entry.findtext("atom:summary", default="", namespaces=ns)),
            "authors": authors,
            "categories": categories,
            "primary_category": categories[0] if categories else None,
            "published": entry.findtext("atom:published", default="", namespaces=ns) or None,
            "updated": entry.findtext("atom:updated", default="", namespaces=ns) or None,
            "doi": doi,
            "journal_ref": journal_ref,
        }

    @staticmethod
    def _arxiv_id_without_version(arxiv_id: str) -> str:
        return re.sub(r"v\d+$", "", arxiv_id.strip())

    @staticmethod
    def _collapse_ws(value: object) -> str | None:
        if not isinstance(value, str):
            return None
        collapsed = re.sub(r"\s+", " ", value).strip()
        return collapsed or None

    @staticmethod
    def _publication_year(pubdate: object) -> int | None:
        if not isinstance(pubdate, str):
            return None
        match = re.search(r"\b(19|20)\d{2}\b", pubdate)
        return int(match.group(0)) if match else None

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
                author_match_confidence="offline_unverified",
                note="Run with --live for author citation counts and candidate disambiguation.",
            )
        payload = self._query_openalex(name, orcid)
        if isinstance(payload, str):
            return AuthorCitationProfile(
                name,
                orcid,
                None,
                None,
                "openalex",
                False,
                author_match_confidence="lookup_error",
                note=payload,
            )
        results = payload.get("results", []) if isinstance(payload, dict) else []
        if not results:
            return AuthorCitationProfile(
                name,
                orcid,
                None,
                None,
                "openalex",
                False,
                author_match_confidence="no_match",
                note="No OpenAlex author match found.",
            )
        candidates = [self._candidate_from_author(author) for author in results if isinstance(author, dict)]
        if not candidates:
            return AuthorCitationProfile(
                name,
                orcid,
                None,
                None,
                "openalex",
                False,
                author_match_confidence="no_match",
                note="OpenAlex returned no usable author candidates.",
            )
        top = candidates[0]
        ambiguity_warning = self._ambiguity_warning(name, orcid, candidates)
        confidence = self._match_confidence(orcid, candidates)
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
            author_match_confidence=confidence,
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
    def _match_confidence(orcid: str | None, candidates: list[AuthorCandidate]) -> str:
        if orcid and candidates:
            return "orcid_exact"
        if len(candidates) == 1:
            return "name_single_candidate"
        if len(candidates) > 1:
            return "name_multiple_candidates"
        return "no_match"

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


def verify_text(
    text: str,
    live: bool = False,
    author: str | None = None,
    orcid: str | None = None,
    max_author_candidates: int = DEFAULT_AUTHOR_CANDIDATES,
    allowed_url_hosts: list[str] | None = None,
    blocked_url_hosts: list[str] | None = None,
) -> dict[str, object]:
    refs = CitationExtractor().extract(text)
    verifier = CitationVerifier(live=live, allowed_url_hosts=allowed_url_hosts, blocked_url_hosts=blocked_url_hosts)
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
    parser.add_argument("--allow-url-host", action="append", default=[], help="Allow raw URL live pings only for this host or parent domain. Repeatable.")
    parser.add_argument("--block-url-host", action="append", default=[], help="Block raw URL live pings for this host or parent domain. Repeatable.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()
    if args.paths:
        text = "\n".join(Path(path).read_text(encoding="utf-8", errors="replace") for path in args.paths)
    else:
        import sys
        text = sys.stdin.read()
    payload = verify_text(
        text,
        live=args.live,
        author=args.author,
        orcid=args.orcid,
        max_author_candidates=args.max_author_candidates,
        allowed_url_hosts=args.allow_url_host,
        blocked_url_hosts=args.block_url_host,
    )
    print(json.dumps(payload, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
