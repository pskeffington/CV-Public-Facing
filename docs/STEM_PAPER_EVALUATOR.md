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
```

Live mode can ping public citation endpoints and query author-level publishing signals. Author matching should be reviewed before being treated as identity-confirmed.

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
  "rationale": "..."
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
  "i10_index": null
}
```

Offline mode should usually have `verified_reference_count` equal to zero because it does not ping external services.

## Local check

```bash
make paper-evaluator-check
```

This check is offline-safe and verifies that a manuscript-like fixture produces a credible composite paper-package score with extracted citations.

## Interpretation

Use this evaluator as a review triage object. It is not a peer-review substitute, plagiarism detector, authorship validator, or truth model. It is a structured way to identify whether a submitted paper package is close to core STEM progress and whether its citations and submitter publishing signals are externally checkable.
