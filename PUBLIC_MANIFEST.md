# Public CV and Research Manifest

Status: visitor-facing public repository.

## Public source files

| File | Purpose |
|---|---|
| `research/RESEARCH_STATUS.md` | Public-readable research storyboard, project status board, and major-needs register |
| `research/research_status.tex` | Public-safe printable LaTeX source for the research-status PDF |
| `.github/workflows/build-public-research-status.yml` | Visible public GitHub Actions workflow that builds the research-status PDF |
| `Makefile` | Local public build target for visitors |

## Generated / expected files

| File | Purpose | Source status |
|---|---|---|
| `documents/Paul_A_Skeffington_Academic_CV_Public.pdf` | Public academic CV | Generated from private `CV` export workflow |
| `documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf` | Public one-page professional profile | Generated from private `CV` export workflow |
| `documents/Paul_A_Skeffington_Research_Status_Public.pdf` | Printable public research-status report | Buildable directly in this public repository |

## Public build command

```bash
make research-status
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
```
