# Paul A. Skeffington — Public CV and Research Status

This repository is the public-facing CV and research-status surface. It is designed for visitors who want to see a sanitized snapshot of current research work, what is complete, what is pending validation, what is out for review, and what each project still needs.

## Start here

Read the public research board:

```text
research/RESEARCH_STATUS.md
```

Printable build target:

```bash
make research-status
```

Generated PDF path:

```text
documents/Paul_A_Skeffington_Research_Status_Public.pdf
```

## Public pull path

```bash
git clone https://github.com/pskeffington/CV-Public-Facing.git
cd CV-Public-Facing
make research-status
ls documents/
```

## Public repository structure

```text
research/
  RESEARCH_STATUS.md
  research_status.tex
documents/
  Paul_A_Skeffington_Academic_CV_Public.pdf
  Paul_A_Skeffington_One_Page_Profile_Public.pdf
  Paul_A_Skeffington_Research_Status_Public.pdf
.github/workflows/
  build-public-research-status.yml
PUBLIC_MANIFEST.md
Makefile
README.md
```

## Public workflow

The public repository has its own GitHub Actions workflow:

```text
Build Public Research Status
```

That workflow compiles the public-safe research-status LaTeX source and uploads the printable PDF as a workflow artifact.

## Boundary

This repository contains public-safe status material and compiled public artifacts. The private `CV` repository remains the source-of-truth for master CV files, evidence ledgers, claim controls, private source extracts, and internal editing history.

Manual edits to generated PDF artifacts may be overwritten by the private export workflow. Public source files in `research/` are intended to remain visible and reviewable.
