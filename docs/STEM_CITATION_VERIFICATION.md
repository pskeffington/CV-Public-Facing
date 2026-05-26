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
```

Live mode can query:

| Signal | Source |
|---|---|
| DOI metadata and cited-by count | Crossref |
| URL/arXiv/PubMed endpoint reachability | public endpoint ping |
| Submitter author profile | OpenAlex |

## Per-reference provenance

Every extracted reference now carries audit provenance:

```json
{
  "source": "identifier_extractor",
  "endpoint": null,
  "checked_at": "2026-05-26T00:00:00Z",
  "verification_mode": "offline"
}
```

Live DOI checks use `source: crossref` and store the Crossref endpoint. Live PMID, arXiv, and URL checks store the public endpoint that was pinged. Offline checks still record `checked_at`, but keep `endpoint` as `null` and `verification_mode` as `offline`.

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
  "ambiguity_warning": null
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

The check is offline-safe. It verifies that DOI, arXiv, PMID, and URL extraction work, that every reference carries provenance fields, and that offline author-profile output remains explicitly unverified.

## Integration with STEM drift

The citation layer is intended to complement the STEM presence score. A strong STEM presence score indicates that the paper surface contains methods, data, validation, reproducibility, and progress signals. Citation verification adds evidence about whether references and submitter publishing signals are externally checkable.
