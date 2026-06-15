# Living CV Actions Guide

This repository is the public build target for a living CV system. Project repositories remain the source of truth for their public status surfaces. The public CV repository uses the allowlist in `data/pipeline_repos.json`, applies release-control checks, regenerates the public project board, and compiles PDFs.

## Architecture

```text
public allowlist update
  -> data/pipeline_repos.json
  -> release-control checks
  -> make public-package
  -> public-safe CV, profile, upload CV, and research-status PDFs
  -> workflow artifacts
```

Manual job-object packaging uses the same public-safe build path:

```text
manual workflow_dispatch
  -> select job_object dropdown
  -> make job-cv-package JOB_OBJECT=<selected>
  -> public package PDFs
  -> selected job package brief and manifest
  -> workflow artifacts
```

## Source of truth

The living CV project inventory is controlled by:

```text
data/pipeline_repos.json
```

For each public project, the manifest records a stable key, repository name, public title, status bucket, public-safe summary, near-term needs, release state, and source files to inspect.

The generator treats the manifest as a public allowlist by default. Recursive public intake is disabled unless `allow_recursive_intake` is deliberately enabled after review. The manifest remains intentionally conservative: source repositories can mature without automatically creating public CV claims.

The manual job-package dropdown is controlled by:

```text
data/job_cv_objects.json
```

Those job objects are public-safe rendering hints only. They do not import private application packets, private source records, or unsupported role claims.

## Generated objects

The generator writes:

```text
cv/current_projects_public.tex
research/RESEARCH_STATUS.md
research/generated_project_board.tex
research/living_source_ledger.md
research/living_repo_scan.md
research/blocked_release_ledger.md
data/stem_cv_objects.json
```

The selected job-package builder writes:

```text
dist/job_cv_packages/<selected-job>/PUBLIC_SAFE_JOB_BRIEF.md
dist/job_cv_packages/<selected-job>/manifest.json
dist/job_cv_packages/<selected-job>/*.pdf
```

Generated files are build objects. Edit `data/pipeline_repos.json`, `data/job_cv_objects.json`, or upstream public README/status files instead of hand-editing generated outputs.

## Public build commands

Neutral public package:

```bash
make public-package
```

Selected public-safe job package:

```bash
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="harvard-chan-director-data-analytics"
make job-cv-package JOB_OBJECT="cdc-foundation-data-modernization-senior-advisor"
```

Release-control and object-contract checks:

```bash
make safety-surface-check
make stem-object-contract
make stem-report-contract
```

The Makefile runs the living CV generator before preflight and LaTeX compilation. The job-package target also validates the job object registry and workflow dropdown contract.

## Public workflow

The public workflow is:

```text
.github/workflows/build-public-research-status.yml
```

It runs on manual `workflow_dispatch` with a `job_object` dropdown, repository dispatch from approved public surfaces, and direct source edits inside this repository.

The workflow is read-only for repository contents. It builds PDFs and uploads artifacts. It does not push generated files back to `main`, which prevents recursive build loops.

Manual dropdown options currently include:

```text
neutral
harvard-chan-director-data-analytics
indeed-data-scientist-iii
rockland-trust-data-architect
navsea-sstm-data-science
valo-health-staff-data-scientist
cdc-foundation-data-modernization-senior-advisor
```

The CDC Foundation object renders under the public-safe title `CDC Foundation - Data Modernization Senior Advisor`. It is intended for public health informatics, data modernization, workforce upskilling, data governance, technical assistance, and reproducible analytics framing, while excluding private packet language and unsupported employment or authority claims.

Artifacts are named by selected object:

```text
public-cv-package-<job_object>
selected-job-cv-package-<job_object>
generated-living-cv-sources-<job_object>
```

## First manual test

Use this test order:

1. Run `Build Public CV Package` with `job_object=neutral`.
2. Confirm the three expected artifacts are present.
3. Confirm `selected-job-cv-package-neutral` contains `PUBLIC_SAFE_JOB_BRIEF.md` and `manifest.json`.
4. Run again with `job_object=harvard-chan-director-data-analytics`.
5. Confirm the selected package uses the Harvard Chan public-safe brief and does not expose private job packet content.
6. Run again with `job_object=cdc-foundation-data-modernization-senior-advisor`.
7. Confirm the selected package uses the CDC Foundation public-safe title and does not expose private application packet language.

The detailed first-test note lives at:

```text
docs/FIRST_TEST_JOB_CV_ACTION.md
```

The public release roadmap lives at:

```text
docs/PUBLIC_RELEASE_ROADMAP.md
```

## Recursion control

The system avoids recursive loops by following these rules:

- Source repos notify the public CV repo.
- The public CV repo builds artifacts.
- The public CV workflow does not commit generated files back to itself.
- Ordinary `github-actions[bot]` push events are skipped.
- Concurrency cancels duplicate in-progress public builds.
- Recursive intake remains disabled unless reviewed and intentionally enabled.

## Adding a new project repository

1. Add the project to `data/pipeline_repos.json`.
2. Confirm the project has a public-safe README or status file.
3. Set or confirm `public_release` is `public`.
4. Run `make safety-surface-check`.
5. Run `make public-package`.
6. Inspect generated PDFs and source ledgers.
7. Add public update notification only if ongoing refresh is needed.
8. Run the public CV workflow manually once to confirm the new project appears in the generated source artifact.

## Adding a new job object

1. Add the new key to `data/job_cv_objects.json`.
2. Use only public-safe rendering hints.
3. Add the same key to the workflow dropdown options.
4. Run `make job-cv-object-check`.
5. Run the manual workflow with the new object.

## Local check

From a local clone of this repository:

```bash
python3 scripts/stem_cv_curator.py
make public-package
make job-cv-object-check
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="cdc-foundation-data-modernization-senior-advisor"
```

Inspect:

```text
research/living_source_ledger.md
research/blocked_release_ledger.md
documents/
dist/job_cv_packages/
```
