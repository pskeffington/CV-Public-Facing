# Public Release Roadmap

## Purpose

This roadmap defines how the public CV renderer keeps public outputs synchronized with source repositories while keeping restricted material out of public CV, profile, research-status, source-ledger, and selected-job package artifacts.

## Current policy

The public renderer now uses a public allowlist model by default.

```text
data/pipeline_repos.json
  -> public allowlist entries
  -> optional recursive intake only when explicitly enabled
  -> release-control hash registry
  -> generated public CV objects
  -> public PDFs and selected job packages
```

Recursive public repository intake is disabled unless `allow_recursive_intake` is set to `true` after review. This keeps newly discovered public repositories from automatically appearing in public CV outputs.

## Release-control rules

Public outputs may include only entries that satisfy all of the following:

- the repository appears in the public allowlist;
- the entry has `public_release` set to `public` or omitted;
- the entry is not matched by the release-control hash registry;
- the rendered text passes the public release guard;
- the generated object contract confirms no non-public project object reached the public project list.

Restricted entries must be handled by hash or other non-sensitive identifiers only. Do not store restricted project names, private project names, or sensitive project-family labels in public documentation.

## Synchronization repair plan

### Phase 1 - Complete

- Add public-safe job-object dropdown packaging.
- Add selected-job package artifact generation.
- Add job-object registry validation.
- Add hashed public release guard.
- Add public allowlist metadata to `data/pipeline_repos.json`.
- Disable recursive intake by default.
- Filter restricted records before scoring, ledgers, object JSON, research status, and PDF sources.

### Phase 2 - Active

- Regenerate public CV outputs after release-control filtering.
- Inspect generated PDFs for restricted-material leakage.
- Confirm selected-job package artifacts do not contain restricted reporting.
- Confirm `blocked_release_ledger.md` reports only non-sensitive hash-prefix records.
- Confirm the public object JSON uses schema `stem-cv-curator/v0.3`.

### Phase 3 - Next

- Add a manifest contract check that fails if recursive intake is enabled without an explicit release-review flag.
- Add a generated-output scanner over `cv/current_projects_public.tex`, `research/RESEARCH_STATUS.md`, `research/generated_project_board.tex`, and `research/living_source_ledger.md` after curator generation.
- Add a public artifact review checklist to selected job packages.
- Add a process for promoting a new public project from intake to allowlist after review.

## New output update path

After changes to public project status or job-object packaging, run:

```bash
make safety-surface-check
make stem-cv
make stem-object-contract
make stem-report-contract
make public-package
```

For selected job packages, run:

```bash
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="harvard-chan-director-data-analytics"
```

The GitHub Actions dropdown performs the selected-job package path through `make job-cv-package`.

## Review checklist for new output

A new public output passes review when:

- the public CV PDFs are generated;
- the one-page profile remains concise and public-safe;
- the index-safe CV does not expose contact details;
- no restricted project-family names or adjacent descriptions appear;
- public methods avoid restricted wording;
- the research-status package contains only public allowlist projects;
- selected-job package briefs remain role-facing and public-safe;
- blocked records appear only as non-sensitive hash-prefix ledger entries.

## Documentation surfaces

The following files should stay synchronized:

```text
docs/LIVING_CV_ACTIONS.md
docs/FIRST_TEST_JOB_CV_ACTION.md
docs/PUBLIC_RELEASE_ROADMAP.md
data/pipeline_repos.json
scripts/stem_cv_curator.py
scripts/check_stem_object_contract.py
scripts/public_release_guard.py
scripts/check_public_release_guard.py
```

## Boundary

This repository is public. It should not contain private job packets, sensitive project names, restricted project-family labels, secrets, private paths, or private-source evidence. When in doubt, keep the material out of the public renderer and preserve it only in the private source repository or private application package.
