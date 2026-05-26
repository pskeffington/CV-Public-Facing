# STEM CV Curator

STEM CV Curator is a cloneable, GitHub-driven CV package for machine-learning, public-health, biomedical-data, and broader STEM researchers. It scans a researcher's active GitHub repositories, reads public README/status surfaces, creates a structured CV object layer, scores STEM presence/drift, checks citation and publishing signals, evaluates submitted paper packages, and renders public-safe CV, profile, and research-status outputs.

This repository also contains Paul A. Skeffington's public CV configuration, but the package is designed so another researcher can clone it and run it against their own GitHub account.

**Maintainer:** Paul Skeffington, MS, MPH  
**Repository status:** active public-safe CV/status generation package.  
**Last documentation refresh:** 2026-05-26

## Current update — 2026-05-26

The package remains the public-facing CV and research-status renderer for the active repository set. The immediate documentation priority is to keep README/status surfaces across source repositories structured enough for the object engine to classify projects, preserve public-safety boundaries, score drift from core STEM progress, check citation/publishing signals, evaluate submitted paper packages, and regenerate current-project outputs without hand-written drift.

## Clone and run for your own GitHub

```bash
git clone https://github.com/pskeffington/CV-Public-Facing.git stem-cv-curator
cd stem-cv-curator
STEM_CV_OWNER=<your-github-user> make public-package
ls documents/
```

Generated PDF paths:

```text
documents/Paul_A_Skeffington_Academic_CV_Public.pdf
documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf
documents/Index_Safe_Public_Upload_CV.pdf
documents/Paul_A_Skeffington_Research_Status_Public.pdf
```

The filenames are currently template defaults and can be renamed in the Makefile for a new user.

## Start here

Read the STEM package guide:

```text
docs/STEM_CV_CURATOR.md
```

Read the object schema:

```text
docs/STEM_CV_OBJECT_SCHEMA.md
```

Read the STEM presence/drift scoring guide:

```text
docs/STEM_PRESENCE_SCORE.md
```

Read the citation verification guide:

```text
docs/STEM_CITATION_VERIFICATION.md
```

Read the composite paper evaluator guide:

```text
docs/STEM_PAPER_EVALUATOR.md
```

Read the evaluator literature/tooling matrix:

```text
docs/STEM_EVALUATOR_LIT_REVIEW_MATRIX.md
```

Read the Actions guide:

```text
docs/LIVING_CV_ACTIONS.md
```

Read the generated public research board:

```text
research/RESEARCH_STATUS.md
```

Read the generated STEM presence dashboard:

```text
research/stem_presence_report.md
```

## Object engine

The main package entry point is:

```bash
make stem-cv
```

That runs:

```bash
python3 scripts/stem_cv_curator.py
```

The curator:

1. Scans the configured GitHub owner's active public repositories.
2. Reads public README/status surfaces.
3. Merges curated overrides from `data/pipeline_repos.json`.
4. Classifies repositories into STEM CV sections.
5. Creates `RepositoryObject`, `RepoSurfaceObject`, `ProjectObject`, and `ClaimObject` records.
6. Scores every project with `StemPresenceScorer`.
7. Writes the object JSON and LaTeX/Markdown render inputs.

## STEM presence/drift scoring

The repository includes a standalone, auditable scorer for estimating how closely a paper, README, status file, or extracted public surface remains aligned with core STEM progress:

```bash
python3 scripts/stem_presence.py --pretty paper.md
cat paper.txt | python3 scripts/stem_presence.py --pretty
```

The scorer returns a 0-100 `score`, a `drift_score` equal to `100 - score`, a band, a rationale, and matched evidence terms. It is intended as a triage metric for public-facing CV quality, not as a substitute for peer review, scientific validity, or impact assessment.

Portfolio-level scoring is generated with:

```bash
make stem-presence-report
```

Metric and report contracts can be checked with:

```bash
make stem-presence-check
make stem-object-contract
make stem-report-contract
```

## Citation and publishing-signal checks

Citation and submitter publishing signals are handled by:

```text
scripts/stem_citation_verifier.py
```

Offline mode extracts DOI, arXiv, PMID, and URL references without network access:

```bash
python3 scripts/stem_citation_verifier.py --pretty paper.md
```

Live mode can ping public scholarly endpoints and query author-level citation signals:

```bash
python3 scripts/stem_citation_verifier.py --pretty --live --author "Jane Researcher" paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --orcid "0000-0000-0000-0000" paper.md
```

The author profile can include cited-by count, works count, h-index, i10-index, and an `author_signal_score`. This is a review aid for STEM drift and publishing context, not a claim that the submitted paper is valid or that an author identity match is final.

Run the offline-safe citation verifier contract with:

```bash
make citation-check
```

## Composite paper-package evaluation

The one-command evaluator for submitted paper packages is:

```text
scripts/stem_paper_evaluator.py
```

It combines STEM presence, STEM drift, citation extraction/verification, and submitter publishing signals into one JSON review object:

```bash
python3 scripts/stem_paper_evaluator.py --pretty paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --author "Jane Researcher" paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --orcid "0000-0000-0000-0000" paper.md
```

Run its offline-safe contract with:

```bash
make paper-evaluator-check
```

## Similar systems and roadmap

The package includes a short literature/tooling matrix for comparable scholarly metadata, citation, author-impact, and paper-screening functions:

```text
docs/STEM_EVALUATOR_LIT_REVIEW_MATRIX.md
```

The matrix compares the local evaluator with Crossref, OpenAlex, Semantic Scholar, PubMed / NCBI E-utilities, OpenCitations, scite-style citation-context systems, and retraction/integrity-signal systems. It also lists near-term polish targets such as provenance fields, author-ambiguity warnings, multi-source citation reconciliation, and an evaluator-output schema contract.

## Main outputs

```text
data/stem_cv_objects.json
cv/current_projects_public.tex
research/RESEARCH_STATUS.md
research/generated_project_board.tex
research/living_source_ledger.md
research/living_repo_scan.md
research/stem_presence_report.md
```

## Full public package build

```bash
make public-package
```

The full build runs the STEM object engine, STEM presence report generation, metric contract checks, citation verifier checks, composite paper evaluator checks, preflight checks, sanitization checks, LaTeX compilation, and PDF export.

## Configuration

The default owner and curated project overrides live in:

```text
data/pipeline_repos.json
```

Override the owner at runtime:

```bash
STEM_CV_OWNER=<your-github-user> make public-package
```

Private repository scanning is off by default. To include private repos, provide a token and opt in explicitly:

```bash
STEM_CV_OWNER=<your-github-user> \
STEM_CV_INCLUDE_PRIVATE=true \
GH_TOKEN=<token> \
make stem-cv
```

## GitHub Actions

The public workflow is:

```text
.github/workflows/build-public-research-status.yml
```

It accepts:

- manual `workflow_dispatch`
- `repository_dispatch` event type `living-cv-source-updated`
- direct source edits inside this repository

Pipeline repositories can use `.github/workflows/notify-living-cv.yml` to notify this package when README, status, roadmap, changelog, or docs files change.

Artifacts:

```text
public-cv-package
generated-living-cv-sources
```

The generated-source artifact includes the living CV sources, living scan ledger, and STEM presence report.

## Public safety checks

The public build runs preflight checks before compiling PDFs. These checks verify that shared project and publication-status sources are wired into the CV outputs, that old hand-written project blocks have not returned, that every generated project carries a valid STEM presence object, that the STEM presence dashboard matches the object JSON, that citation extraction and offline author-profile contracts pass, that the composite paper evaluator returns a credible package score for a manuscript-like fixture, and that public and index-safe sanitization rules pass before PDF generation.

## Repository structure

```text
cv/
  academic_cv_public.tex
  one_page_profile_public.tex
  public_upload_cv.tex
  current_projects_public.tex
  publication_pipeline_public.tex
data/
  pipeline_repos.json
  stem_cv_objects.json
docs/
  STEM_CV_CURATOR.md
  STEM_CV_OBJECT_SCHEMA.md
  STEM_PRESENCE_SCORE.md
  STEM_CITATION_VERIFICATION.md
  STEM_PAPER_EVALUATOR.md
  STEM_EVALUATOR_LIT_REVIEW_MATRIX.md
  LIVING_CV_ACTIONS.md
research/
  RESEARCH_STATUS.md
  generated_project_board.tex
  living_source_ledger.md
  living_repo_scan.md
  stem_presence_report.md
  research_status.tex
scripts/
  stem_cv_curator.py
  stem_presence.py
  stem_citation_verifier.py
  stem_paper_evaluator.py
  write_stem_presence_report.py
  check_stem_presence.py
  check_stem_citation_verifier.py
  check_stem_paper_evaluator.py
  check_stem_object_contract.py
  check_stem_presence_report.py
  update_living_cv.py
  preflight_public_package.sh
  check_public_sanitization.sh
  check_index_safe_upload.sh
.github/workflows/
  build-public-research-status.yml
Makefile
README.md
```

## Boundary

The package generates public-safe CV/status source files, public-safe Markdown, repository metadata, object JSON, metric reports, citation-verification outputs, paper-evaluation outputs, and compiled public artifacts. Users should keep private claim ledgers, raw data, sensitive sources, addresses, phone numbers, and operational details outside public outputs unless they explicitly configure a private-only workflow.
