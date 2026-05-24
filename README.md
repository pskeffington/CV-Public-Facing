# Paul A. Skeffington — Public CV and Research Status

This repository is the public-facing CV and research-status surface. It is designed for visitors who want a sanitized public CV package plus a concise snapshot of current research work, what is complete, what is pending validation, what is out for review, and what each project still needs.

## Start here

Read the public research board:

```text
research/RESEARCH_STATUS.md
```

Read the public for-hire and civic engagement page:

```text
hire/FOR_HIRE_LATIN.md
```

Build the full public package:

```bash
make public-package
```

Generated PDF paths:

```text
documents/Paul_A_Skeffington_Academic_CV_Public.pdf
documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf
documents/Paul_A_Skeffington_Research_Status_Public.pdf
```

## Public pull path

```bash
git clone https://github.com/pskeffington/CV-Public-Facing.git
cd CV-Public-Facing
make public-package
ls documents/
```

## Public repository structure

```text
cv/
  academic_cv_public.tex
  one_page_profile_public.tex
research/
  RESEARCH_STATUS.md
  research_status.tex
hire/
  FOR_HIRE_LATIN.md
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
Build Public CV Package
```

That workflow compiles the public-safe Academic CV, One-Page Profile, and Research Status LaTeX sources, then uploads all three printable PDFs as a workflow artifact named:

```text
public-cv-package
```

## Boundary

This repository contains public-safe CV/status source files, public-safe Markdown, repository metadata, and compiled public artifacts. The private `CV` repository remains the source-of-truth for master CV files, evidence ledgers, claim controls, private source extracts, and internal editing history.

Manual edits to generated PDF artifacts may be overwritten by the private export workflow. Public source files in `cv/` and `research/` are intended to remain visible and reviewable.
