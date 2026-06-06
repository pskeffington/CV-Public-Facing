# Public CV Renderer

This repository builds the public-safe CV, one-page profile, index-safe upload CV, and research-status package for Paul A. Skeffington. It also serves as a cloneable public CV renderer for researchers who want a GitHub-driven, source-ledgered CV package.

The repository is intentionally public. It must contain only public-safe source text, public project summaries, generated public artifacts, and non-sensitive build metadata.

**Maintainer:** Paul Skeffington, MS, MPH  
**Repository status:** active public-safe CV and research-status renderer.  
**Last documentation refresh:** 2026-06-06

## Current operating model

`CV-Public-Facing` is the public renderer in the broader CV and application ecosystem.

```text
private CV claim controls
  -> public-safe CV/status rendering
  -> public portfolio surfaces
  -> application/job package alignment
```

The public project register is now an allowlist by default. The renderer reads `data/pipeline_repos.json`, applies public-release checks, generates LaTeX/Markdown source objects, and compiles PDFs. Recursive public repository intake is disabled unless explicitly reviewed and enabled.

## Build outputs

Generated PDF paths:

```text
documents/Paul_A_Skeffington_Academic_CV_Public.pdf
documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf
documents/Index_Safe_Public_Upload_CV.pdf
documents/Paul_A_Skeffington_Research_Status_Public.pdf
```

Selected job-package outputs are written under:

```text
dist/job_cv_packages/<selected-job>/
```

## Main commands

Build the neutral public package:

```bash
make public-package
```

Build a selected public-safe job package:

```bash
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="harvard-chan-director-data-analytics"
```

Run the main contract checks:

```bash
make public-manifest-check
make safety-surface-check
make stem-object-contract
make stem-report-contract
```

## GitHub Actions

The main workflow is:

```text
.github/workflows/build-public-research-status.yml
```

It supports manual `workflow_dispatch` with a `job_object` dropdown. The dropdown builds the public CV package and then wraps it in a selected public-safe job package with a brief and manifest.

Current job objects are controlled by:

```text
data/job_cv_objects.json
```

## Public-release boundaries

This repository should not contain private job packets, private source records, restricted project-family names, secrets, credentials, private paths, or sensitive operational details.

Public outputs may include only projects that satisfy all of the following:

- the project is present in the public allowlist;
- the release state is public;
- the project is not matched by the release-control hash registry;
- generated rendered sources pass the public-release guard;
- generated object contracts confirm no non-public project entered the public project list.

Internal scores and review metrics may remain in generated object JSON or internal ledgers, but they should not render into public PDFs.

## Start here

Read the public release roadmap:

```text
docs/PUBLIC_RELEASE_ROADMAP.md
```

Read the Actions guide:

```text
docs/LIVING_CV_ACTIONS.md
```

Read the first-test guide:

```text
docs/FIRST_TEST_JOB_CV_ACTION.md
```

Read the object schema:

```text
docs/STEM_CV_OBJECT_SCHEMA.md
```

## Clone and run for another public profile

```bash
git clone https://github.com/pskeffington/CV-Public-Facing.git public-cv-renderer
cd public-cv-renderer
STEM_CV_OWNER=<your-github-user> make public-package
ls documents/
```

The filenames are configured for this profile by default and can be renamed in the Makefile for another user.

## Object engine

The main object-generation entry point is:

```bash
make stem-cv
```

That runs:

```bash
python3 scripts/stem_cv_curator.py
```

The curator:

1. reads the public allowlist manifest;
2. fetches public README/status surfaces for allowed projects;
3. classifies public projects into CV sections;
4. creates repository, surface, project, and claim objects;
5. keeps internal scoring available for review contracts;
6. writes public LaTeX/Markdown render inputs without internal score labels;
7. writes release-control ledgers using non-sensitive identifiers.

## Development notes

The repo has no Python package manager file at this time. Build and validation are Makefile-driven. Generated public PDFs are workflow artifacts and are not pushed back to `main` by the workflow.
