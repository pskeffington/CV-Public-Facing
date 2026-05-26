# Public CV and Research Manifest

Status: visitor-facing public repository with a rebuildable, living public CV package.

## Public source files

| File | Purpose |
|---|---|
| `cv/academic_cv_public.tex` | Public-safe Academic CV LaTeX source |
| `cv/one_page_profile_public.tex` | Public-safe One-Page Profile LaTeX source |
| `cv/public_upload_cv.tex` | Index-safe CV variant for upload contexts requiring reduced personal identifiers |
| `cv/current_projects_public.tex` | Generated current-project register used by public CV outputs |
| `cv/publication_pipeline_public.tex` | Shared publication-status register used by public CV outputs |
| `data/pipeline_repos.json` | Living CV manifest listing pipeline repositories and public status surfaces |
| `research/RESEARCH_STATUS.md` | Generated public-readable research storyboard, project status board, and major-needs register |
| `research/generated_project_board.tex` | Generated printable project board source used by the research-status PDF |
| `research/living_source_ledger.md` | Generated ledger of README/status files checked by the living CV generator |
| `research/research_status.tex` | Public-safe printable LaTeX source for the research-status PDF |
| `scripts/update_living_cv.py` | Manifest-driven generator that pulls public README/status surfaces from pipeline repositories |
| `.github/workflows/build-public-research-status.yml` | Public GitHub Actions workflow that builds the full public CV package and accepts living-CV dispatch events |
| `Makefile` | Local public build targets for visitors |

## Generated / expected files

| File | Purpose | Source status |
|---|---|---|
| `documents/Paul_A_Skeffington_Academic_CV_Public.pdf` | Public academic CV | Buildable directly in this public repository |
| `documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf` | Public one-page professional profile | Buildable directly in this public repository |
| `documents/Index_Safe_Public_Upload_CV.pdf` | Identifier-reduced upload CV | Buildable directly in this public repository |
| `documents/Paul_A_Skeffington_Research_Status_Public.pdf` | Printable public research-status report | Buildable directly in this public repository |

## Public build command

```bash
make public-package
```

The build first regenerates living CV objects from `data/pipeline_repos.json` and the current public README/status files in the listed repositories.

## Public workflow behavior

The public GitHub Actions workflow is read-only for repository contents. It builds public PDFs and uploads them as the `public-cv-package` artifact. It also uploads `generated-living-cv-sources` so the regenerated public project objects can be inspected after each dispatch/build.

The workflow uses a concurrency group and skips ordinary `github-actions[bot]` push events. This prevents recursive public-build loops while preserving manual `workflow_dispatch`, `repository_dispatch`, and normal source-edit builds.

## Source-repo notification behavior

Pipeline repositories can include `.github/workflows/notify-living-cv.yml`. On README/status/docs changes, that workflow sends a `repository_dispatch` event named `living-cv-source-updated` to this repository when the source repo has a configured `LIVING_CV_DISPATCH_TOKEN` secret.

## Public-safe rule

This repository may contain public-facing Markdown, public-safe LaTeX, repository metadata, generated public CV objects, and compiled public artifacts.

Do not commit:

- private LaTeX source files
- private claim ledgers
- private source extracts
- addresses, phone numbers, personal email accounts, home-site details, operational site layouts, or sensitive infrastructure details
- unverified publication, grant, appointment, award, or certification claims

## Pull command

```bash
git pull --ff-only
make public-package
```
