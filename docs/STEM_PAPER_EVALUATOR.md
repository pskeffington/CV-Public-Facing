# STEM Paper Evaluator

The STEM paper evaluator is the package-level entry point for reviewing a submitted paper surface against STEM drift, citation integrity, and submitter publishing signals.

It combines three layers:

1. STEM presence and drift scoring from `scripts/stem_presence.py`.
2. Citation extraction and optional live verification from `scripts/stem_citation_verifier.py`.
3. A composite paper-package score that summarizes the submitted surface in one auditable JSON object.

## Script

```text
scripts/stem_paper_evaluator.py
```

## Offline use

```bash
python3 scripts/stem_paper_evaluator.py --pretty paper.md
cat paper.txt | python3 scripts/stem_paper_evaluator.py --pretty
```

Offline mode is deterministic and safe for CI. It extracts citation identifiers, scores STEM presence, and returns a composite score without querying external services.

## Live use

```bash
python3 scripts/stem_paper_evaluator.py --pretty --live --author "Jane Researcher" paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --orcid "0000-0000-0000-0000" paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --author "Jane Researcher" --max-author-candidates 5 paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --allow-url-host example.org paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --block-url-host private.example paper.md
```

Live mode can ping public citation endpoints and query author-level publishing signals. Author matching should be reviewed before being treated as identity-confirmed.

## Raw URL policy controls

Raw URL pings can be constrained during one-command paper review without disabling DOI, PMID, arXiv, or OpenAlex checks:

```bash
python3 scripts/stem_paper_evaluator.py --pretty --live --allow-url-host example.org paper.md
python3 scripts/write_stem_paper_review.py --live --allow-url-host example.org --out review.md paper.md
```

`--allow-url-host` restricts raw URL live pings to the listed host or its subdomains. `--block-url-host` prevents raw URL pings to the listed host or its subdomains. Both flags are repeatable. If both are supplied, the blocklist takes precedence.

Policy-blocked raw URL references remain in the raw citation payload, receive `verification_mode: live_policy_blocked`, and increment `policy_blocked_reference_count` in the publishing summary.

## Output object

```json
{
  "live": false,
  "stem_presence": {},
  "publishing_signal_summary": {},
  "composite_paper_score": {},
  "citation_verification": {}
}
```

## Composite score fields

```json
{
  "stem_presence_score": 76,
  "stem_drift_score": 24,
  "publishing_signal_score": 42,
  "composite_score": 68,
  "composite_drift_score": 32,
  "band": "credible_stem_paper_package",
  "rationale": "...",
  "review_flags": [
    "references_not_live_verified",
    "no_verified_author_signal"
  ]
}
```

The composite score weights STEM presence more heavily than citation context. Current weighting is 75% STEM presence and 25% publishing signal.

## Bands

| Band | Meaning |
|---|---|
| `strong_stem_paper_package` | Strong STEM surface with supporting citation/publishing context. |
| `credible_stem_paper_package` | Credible STEM signal with usable but possibly incomplete citation context. |
| `mixed_or_underverified_package` | Some STEM evidence but weak documentation, weak citation context, or incomplete verification. |
| `high_drift_or_low_evidence_package` | High drift or insufficient evidence for public STEM claims. |

## Publishing summary

The evaluator includes:

```json
{
  "reference_count": 3,
  "verified_reference_count": 0,
  "average_reference_score": 50.0,
  "author_signal_score": 0,
  "cited_by_count": null,
  "works_count": null,
  "h_index": null,
  "i10_index": null,
  "author_candidate_count": 0,
  "author_ambiguity_warning": null,
  "author_match_confidence": "offline_unverified",
  "policy_blocked_reference_count": 0,
  "source_provenance": [
    "reference:identifier_extractor:offline",
    "author_profile:openalex:offline_unverified"
  ]
}
```

Offline mode should usually have `verified_reference_count` equal to zero because it does not ping external services.

## Review flags

| Flag | Meaning |
|---|---|
| `high_stem_drift` | The STEM drift score is high enough to require closer review. |
| `no_references_extracted` | No DOI, arXiv, PMID, or URL references were extracted. |
| `references_not_live_verified` | References were extracted but not live-verified. This is expected in offline CI. |
| `reference_url_policy_blocked` | At least one raw URL reference was blocked by allowlist/blocklist policy. |
| `author_identity_ambiguous` | A live author-name lookup returned multiple candidates or an ambiguity warning. |
| `no_verified_author_signal` | No live author citation signal is available or the author signal score is zero. |
| `author_match_unconfirmed` | Author identity remains unconfirmed because the match is offline, missing, errored, or unavailable. |

## Provenance and ambiguity fields

`source_provenance` records where the evaluator's publishing signal came from. Offline entries use `reference:identifier_extractor:offline`. Live DOI checks may identify Crossref-derived evidence, live PMID checks can identify NCBI PubMed ESummary, live arXiv checks can identify the arXiv API, and policy-blocked raw URL references use `live_policy_blocked`.

`author_candidate_count`, `author_ambiguity_warning`, and `author_match_confidence` summarize OpenAlex author disambiguation. Name-based lookup can return several plausible candidates. ORCID-based lookup is preferred when available.

## Related systems matrix

The evaluator is benchmarked conceptually against related scholarly metadata and citation systems in:

```text
docs/STEM_EVALUATOR_LIT_REVIEW_MATRIX.md
```

That matrix documents adjacent capabilities from Crossref, OpenAlex, Semantic Scholar, PubMed / NCBI E-utilities, OpenCitations, scite-style citation-context systems, and retraction/integrity-signal systems. It also lists package gaps and next polish targets.

## Local check

```bash
make paper-evaluator-check
```

This check is offline-safe and verifies that a manuscript-like fixture produces a credible composite paper-package score with extracted citations and a valid evaluator output contract.

## Interpretation

Use this evaluator as a review triage object. It is not a peer-review substitute, plagiarism detector, authorship validator, or truth model. It is a structured way to identify whether a submitted paper package is close to core STEM progress and whether its citations and submitter publishing signals are externally checkable.
