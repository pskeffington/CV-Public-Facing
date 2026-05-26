# Public CV and Research Manifest

Status: visitor-facing public repository with a rebuildable public CV package.

## Public source files

| File | Purpose |
|---|---|
| `cv/academic_cv_public.tex` | Public-safe Academic CV LaTeX source |
| `cv/one_page_profile_public.tex` | Public-safe One-Page Profile LaTeX source |
| `cv/public_upload_cv.tex` | Index-safe CV variant for upload contexts requiring reduced personal identifiers |
| `cv/current_projects_public.tex` | Shared current-project register used by public CV outputs |
| `cv/publication_pipeline_public.tex` | Shared publication-status register used by public CV outputs |
| `research/RESEARCH_STATUS.md` | Public-readable research storyboard, project status board, and major-needs register |
| `research/generated_project_board.tex` | Printable project board source used by the research-status PDF |
| `research/research_status.tex` | Public-safe printable LaTeX source for the research-status PDF |
| `.github/workflows/build-public-research-status.yml` | Visible public GitHub Actions workflow that builds the full public CV package |
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

## Public workflow behavior

The public GitHub Actions workflow is read-only for repository contents. It builds public PDFs and uploads them as the `public-cv-package` artifact. It does not commit generated outputs back to `main`.

The workflow uses a concurrency group and skips ordinary `github-actions[bot]` push events. This prevents recursive public-build loops while preserving manual `workflow_dispatch` runs and normal source-edit builds.

## Public-safe rule

This repository may contain public-facing Markdown, public-safe LaTeX, repository metadata, and compiled public artifacts.

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
