# Public CV and Research Manifest

Status: visitor-facing public repository with a rebuildable public CV package.

## Public source files

| File | Purpose |
|---|---|
| `cv/academic_cv_public.tex` | Public-safe Academic CV LaTeX source |
| `cv/one_page_profile_public.tex` | Public-safe One-Page Profile LaTeX source |
| `research/RESEARCH_STATUS.md` | Public-readable research storyboard, project status board, and major-needs register |
| `research/research_status.tex` | Public-safe printable LaTeX source for the research-status PDF |
| `.github/workflows/build-public-research-status.yml` | Visible public GitHub Actions workflow that builds the full public CV package |
| `Makefile` | Local public build targets for visitors |

## Generated / expected files

| File | Purpose | Source status |
|---|---|---|
| `documents/Paul_A_Skeffington_Academic_CV_Public.pdf` | Public academic CV | Buildable directly in this public repository |
| `documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf` | Public one-page professional profile | Buildable directly in this public repository |
| `documents/Paul_A_Skeffington_Research_Status_Public.pdf` | Printable public research-status report | Buildable directly in this public repository |

## Public build command

```bash
make public-package
```

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
