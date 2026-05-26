# STEM Citation Verification

The STEM citation verifier adds source-integrity and publishing-signal checks to the STEM drift package.

It is designed to answer two separate questions:

1. Does the submitted paper or project surface contain verifiable citation identifiers?
2. Does the submitter have an independently observable publishing/citation footprint?

The verifier is conservative by default. Offline mode extracts identifiers and assigns only identifier-based publishing-signal scores. Live mode is explicit and uses public scholarly endpoints.

## Script

```text
scripts/stem_citation_verifier.py
```

## Citation extraction

The extractor recognizes:

| Type | Example |
|---|---|
| DOI | `10.1038/nature12373` |
| arXiv | `arXiv:2101.00001` |
| PMID | `PMID: 23803847` |
| URL | `https://example.org/reproducibility-manifest` |

## Offline use

```bash
python3 scripts/stem_citation_verifier.py --pretty paper.md
cat paper.txt | python3 scripts/stem_citation_verifier.py --pretty
```

Offline mode returns extracted references and conservative publishing-signal scores but does not mark references as live-verified.

## Live use

```bash
python3 scripts/stem_citation_verifier.py --pretty --live paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --author "Jane Researcher" paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --orcid "0000-0000-0000-0000" paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --author "Jane Researcher" --max-author-candidates 5 paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --allow-url-host example.org paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --block-url-host private.example paper.md
```

Live mode can query:

| Signal | Source |
|---|---|
| DOI metadata and cited-by count | Crossref |
| PMID metadata | NCBI PubMed ESummary |
| arXiv metadata | arXiv API Atom feed |
| URL endpoint reachability | public endpoint ping, optionally controlled by URL policy |
| Submitter author profile | OpenAlex |

## Raw URL policy controls

Raw URL pings can be constrained without disabling DOI, PMID, arXiv, or OpenAlex checks:

```bash
python3 scripts/stem_citation_verifier.py --live --allow-url-host example.org paper.md
python3 scripts/stem_citation_verifier.py --live --block-url-host private.example paper.md
```

`--allow-url-host` restricts raw URL live pings to the listed host or its subdomains. `--block-url-host` prevents pings to the listed host or its subdomains. Both flags are repeatable. If both are supplied, the blocklist takes precedence. Policy-blocked raw URL references remain in the output but have `verified: false`, `verification_mode: live_policy_blocked`, and a `url_policy_blocked` signal.

## Per-reference provenance

Every extracted reference now carries audit provenance:

```json
{
  "source": "identifier_extractor",
  "endpoint": null,
  "checked_at": "2026-05-26T00:00:00Z",
  "verification_mode": "offline",
  "metadata": null
}
```

Live DOI checks use `source: crossref` and store the Crossref endpoint. Live PMID checks use `source: ncbi_pubmed_esummary`, store the NCBI ESummary endpoint, and populate the `metadata` object when PubMed returns a record. Live arXiv checks use `source: arxiv_api`, store the arXiv API endpoint, and populate the same `metadata` field when arXiv returns an entry. Offline checks still record `checked_at`, but keep `endpoint` and `metadata` as `null` and `verification_mode` as `offline`.

## PubMed metadata

Live PMID checks can add:

```json
{
  "pmid": "23803847",
  "title": "...",
  "journal": "...",
  "publication_date": "2013 Jul",
  "publication_year": 2013,
  "authors": ["Author A", "Author B"],
  "doi": "10.xxxx/example",
  "pmcid": "PMC...",
  "publication_types": ["Journal Article"]
}
```

This enrichment is live-only and depends on NCBI ESummary responses.

## arXiv metadata

Live arXiv checks can add:

```json
{
  "arxiv_id": "2101.00001v1",
  "canonical_arxiv_id": "2101.00001",
  "title": "...",
  "abstract": "...",
  "authors": ["Author A", "Author B"],
  "categories": ["cs.LG"],
  "primary_category": "cs.LG",
  "published": "2021-01-01T00:00:00Z",
  "updated": "2021-01-02T00:00:00Z",
  "doi": null,
  "journal_ref": null
}
```

This enrichment is live-only and depends on the arXiv API Atom feed.

## Author citation profile

When `--author` or `--orcid` is supplied, live mode attempts to return:

```json
{
  "matched_name": "Jane Researcher",
  "author_id": "https://openalex.org/A...",
  "source": "openalex",
  "verified": true,
  "cited_by_count": 250,
  "works_count": 12,
  "h_index": 8,
  "i10_index": 6,
  "author_signal_score": 70,
  "candidate_count": 1,
  "candidates": [],
  "ambiguity_warning": null,
  "author_match_confidence": "name_single_candidate"
}
```

This author-level score is a publishing-signal indicator. It should not be treated as a measure of scientific truth, paper validity, or authorship identity unless the match is reviewed.

## Publishing-signal bands

| Band | Meaning |
|---|---|
| `strong_publishing_signal` | Verified scholarly identifier and/or substantial citation signal. |
| `moderate_publishing_signal` | Verifiable identifier or moderate citation signal. |
| `weak_or_unverified_signal` | Identifier found but live verification is absent or weak. |
| `low_publishing_signal` | Minimal citation evidence. |

## Local check

```bash
make citation-check
```

The check is offline-safe. It verifies that DOI, arXiv, PMID, and URL extraction work, that every reference carries provenance and metadata fields, that raw URL policy controls behave as expected, and that offline author-profile output remains explicitly unverified.

## Integration with STEM drift

The citation layer is intended to complement the STEM presence score. A strong STEM presence score indicates that the paper surface contains methods, data, validation, reproducibility, and progress signals. Citation verification adds evidence about whether references and submitter publishing signals are externally checkable.
