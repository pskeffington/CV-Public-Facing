# Living CV Actions Guide

This repository is the public build target for a living CV system. Project repositories remain the source of truth for their own current status, README, roadmap, and documentation surfaces. The public CV repository pulls those surfaces during its build and regenerates the public project board before compiling PDFs.

## Architecture

```text
source project repo push
  -> .github/workflows/notify-living-cv.yml
  -> repository_dispatch: living-cv-source-updated
  -> pskeffington/CV-Public-Facing
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

For each project, the manifest records:

- stable project key
- GitHub repository full name
- public CV title
- status bucket
- public-safe summary
- near-term needs
- source files to inspect

The generator reads that manifest and checks public README/status surfaces from each project repository. The manifest remains intentionally conservative: source repositories can mature without automatically creating strong CV claims.

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
```

The Makefile runs the living CV generator before preflight and LaTeX compilation. The job-package target also validates the job object registry and workflow dropdown contract.

## Public workflow

The public workflow is:

```text
.github/workflows/build-public-research-status.yml
```

It runs on:

- manual `workflow_dispatch` with a `job_object` dropdown;
- `repository_dispatch` event type `living-cv-source-updated`;
- direct source edits inside this repository.

The workflow is read-only for repository contents. It builds PDFs and uploads artifacts. It does not push generated files back to `main`, which prevents recursive build loops.

Manual dropdown options currently include:

```text
neutral
harvard-chan-director-data-analytics
indeed-data-scientist-iii
rockland-trust-data-architect
navsea-sstm-data-science
valo-health-staff-data-scientist
```

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

The detailed first-test note lives at:

```text
docs/FIRST_TEST_JOB_CV_ACTION.md
```

## Source repository notifier

Each pipeline source repo can include:

```text
.github/workflows/notify-living-cv.yml
```

The notifier watches README/status/docs changes and sends a dispatch event to this public CV repository.

Recommended watched paths:

```yaml
paths:
  - 'README.md'
  - 'PROJECT_STATUS.md'
  - 'REPRODUCIBILITY.md'
  - 'ROADMAP.md'
  - 'CHANGELOG.md'
  - 'docs/**'
```

Some repositories may also watch `notes/**`, `references/**`, or manuscript-support documentation when those files represent public status surfaces.

## Required secret

Each source repository needs an Actions secret:

```text
LIVING_CV_DISPATCH_TOKEN
```

The token must be able to call the GitHub REST API endpoint for repository dispatch events on:

```text
pskeffington/CV-Public-Facing
```

If the token is missing, the source workflow should skip dispatch safely rather than fail the source repository build.

## Dispatch payload

The source repository sends:

```json
{
  "event_type": "living-cv-source-updated",
  "client_payload": {
    "source_repo": "owner/repo",
    "source_sha": "commit-sha"
  }
}
```

The current public CV generator does not require the payload to build; it regenerates the full manifest each time. The payload is retained for traceability and future filtering.

## Recursion control

The system avoids recursive loops by following these rules:

- Source repos notify the public CV repo.
- The public CV repo builds artifacts.
- The public CV workflow does not commit generated files back to itself.
- Ordinary `github-actions[bot]` push events are skipped.
- Concurrency cancels duplicate in-progress public builds.

## Adding a new project repository

1. Add the project to `data/pipeline_repos.json`.
2. Confirm the project has a public-safe README or status file.
3. Add `.github/workflows/notify-living-cv.yml` to the project repository.
4. Add the `LIVING_CV_DISPATCH_TOKEN` secret to the source repository.
5. Run the public CV workflow manually once to confirm the new project appears in the generated source artifact.

## Adding a new job object

1. Add the new key to `data/job_cv_objects.json`.
2. Use only public-safe rendering hints.
3. Add the same key to the workflow dropdown options.
4. Run `make job-cv-object-check`.
5. Run the manual workflow with the new object.

## Local check

From a local clone of this repository:

```bash
python3 scripts/update_living_cv.py
make public-package
make job-cv-object-check
make job-cv-package JOB_OBJECT="neutral"
```

Inspect:

```text
research/living_source_ledger.md
documents/
dist/job_cv_packages/
```
