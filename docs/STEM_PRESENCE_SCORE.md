# STEM Presence Score

The STEM Presence Score is a deterministic, auditable metric for estimating how closely a paper, project, repository, or CV object remains aligned with core STEM progress.

The score is designed for public-facing portfolio curation. It does not judge scientific truth, peer-review quality, or impact. It measures whether the available public surface contains concrete STEM signals such as domain specificity, methods, reproducibility, validation, measurement, and output progress.

## Output fields

Each scored object receives a `stem_presence` object:

```json
{
  "score": 76,
  "drift_score": 24,
  "band": "core_stem",
  "rationale": "core_stem score 76/100 based on domain terms=...",
  "matched_domain_terms": [],
  "matched_method_terms": [],
  "matched_reproducibility_terms": [],
  "matched_progress_terms": [],
  "matched_drift_terms": []
}
```

`score` is a 0-100 estimate of STEM presence. `drift_score` is `100 - score` and represents drift from core STEM progress.

## Bands

| Band | Score range | Meaning |
|---|---:|---|
| `core_stem` | 75-100 | Strong evidence of STEM domain, methods, reproducibility, and concrete progress. |
| `stem_adjacent` | 55-74 | Clear STEM connection but missing one or more strong method/reproducibility/progress signals. |
| `mixed_or_transitional` | 35-54 | Some STEM language appears, but the surface may still be narrative, intake-stage, or underdeveloped. |
| `low_stem_presence` | 0-34 | Little public evidence of STEM progress or substantial drift language. |

## Scoring model

The scorer is vocabulary based and intentionally transparent. It gives weighted credit for four dimensions:

| Dimension | Weight | Examples |
|---|---:|---|
| Domain specificity | 35 | science, engineering, public health, biomedical, machine learning, dataset, algorithm |
| Methods and measurement | 30 | method, analysis, hypothesis, regression, validation, metric, robustness |
| Reproducibility | 20 | code, repository, manifest, model card, workflow, documentation, test |
| Progress/output | 15 | result, submitted, manuscript, peer review, figure, implemented, milestone |

A drift penalty of up to 25 points is applied when the public surface is dominated by non-evidence-bearing terms such as personal memoir, symbolic/esoteric framing, promotional language, speculative framing, or portfolio-only placeholders.

## Integration points

The metric is implemented in:

```text
scripts/stem_presence.py
```

It can score a paper or extracted public surface directly:

```bash
python3 scripts/stem_presence.py --pretty paper.md
cat paper.txt | python3 scripts/stem_presence.py --pretty
```

The living CV pipeline integrates the scorer through:

```text
scripts/stem_cv_curator.py
scripts/write_stem_presence_report.py
```

The generated dashboard is:

```text
research/stem_presence_report.md
```

## Local checks

Use these Make targets from the repository root:

```bash
make stem-presence-check
make stem-object-contract
make stem-report-contract
```

The contract checks confirm that generated project objects contain valid `stem_presence` metrics and that the Markdown dashboard matches the generated object JSON.

## Interpretation

Use the score as a triage signal. A low score usually means that the public README/status surface needs more methods, data, validation, or reproducibility detail. A high score means the public-facing project description is more likely to support credible STEM CV claims.
