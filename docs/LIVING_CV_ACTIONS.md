# Living CV Actions Guide

This repository is the public build target for a living CV system. Project repositories remain the source of truth for their own current status, README, roadmap, and documentation surfaces. The public CV repository pulls those surfaces during its build and regenerates the public project board before compiling PDFs.

## Architecture

```text
source project repo push
  -> .github/workflows/notify-living-cv.yml
  -> repository_dispatch: living-cv-source-updated
  -> pskeffington/CV-Public-Facing
  -> make public-package
  -> scripts/update_living_cv.py
  -> generated public CV objects
  -> LaTeX PDF build
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

## Generated objects

The generator writes:

```text
cv/current_projects_public.tex
research/RESEARCH_STATUS.md
research/generated_project_board.tex
research/living_source_ledger.md
```

These are build objects. Edit `data/pipeline_repos.json` or the upstream project README/status files instead of hand-editing the generated files.

## Public build command

```bash
make public-package
```

The Makefile runs the living CV generator before preflight and LaTeX compilation.

## Public workflow

The public workflow is:

```text
.github/workflows/build-public-research-status.yml
```

It runs on:

- manual `workflow_dispatch`
- `repository_dispatch` event type `living-cv-source-updated`
- direct source edits inside this repository

The workflow is read-only for repository contents. It builds PDFs and uploads artifacts. It does not push generated files back to `main`, which prevents recursive build loops.

Artifacts:

```text
public-cv-package
generated-living-cv-sources
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

## Local check

From a local clone of this repository:

```bash
python3 scripts/update_living_cv.py
make public-package
```

Inspect:

```text
research/living_source_ledger.md
documents/
```
