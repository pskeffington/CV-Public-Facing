# Auth Eco Integration

Author: Paul Skeffington, MS, MPH  
Status: public-renderer integration note  
Last updated: 2026-05-26

## Purpose

This document aligns `CV-Public-Facing` with the broader Auth Eco ecosystem defined in:

```text
Portfolio/docs/ECOSYSTEM_ALIGNMENT.md
```

`CV-Public-Facing` is the public-safe renderer. It should consume public repository surfaces, public-safe claim objects, and curated overrides without inventing unsupported claims or leaking private-source evidence.

## Ecosystem Role

```text
CV private claim controls
  -> public-safe CV/status rendering
  -> portfolio proof packets
  -> role-matching and audit-chain artifacts
```

This repository owns the public rendering layer:

```text
public CV
one-page profile
research status board
STEM presence/drift report
repository scan
public-safe source ledger
```

## Shared Object Flow

```text
public repository surface
  -> RepositoryObject
  -> RepoSurfaceObject
  -> ProjectObject
  -> ClaimObject
  -> PublicSurfaceObject
  -> rendered CV/status output
```

Where private CV evidence is relevant, only public-safe claim wording should cross into this repository.

## Required Fields for Compatible Objects

```text
object_id
object_type
repository_id
project_id
source_ids
claim_ids
output_id
generator_name
generator_version
generated_at
review_status
use_boundary
public_safety_boundary
```

## Public-Safety Boundaries

Allowed output boundaries:

```text
public
public_safe_summary
fixture_only
```

Inputs or notes that are private, restricted, or redacted should remain in the private CV workspace or in local-only review artifacts.

## Drift Rules

This repository should flag or avoid:

```text
public CV claim not present in a public repo surface or public-safe claim object
repository status older than the rendered public status page
manuscript status overstated
benchmark scaffold described as validated comparison
private source language copied into public output
role-match output treated as autonomous selection evidence
```

## Current Integration Points

```text
data/stem_cv_objects.json
research/RESEARCH_STATUS.md
research/living_source_ledger.md
research/living_repo_scan.md
research/stem_presence_report.md
cv/current_projects_public.tex
scripts/stem_cv_curator.py
scripts/stem_presence.py
scripts/stem_paper_evaluator.py
```

## Next Alignment Tasks

```text
1. Add explicit `public_safety_boundary` fields to generated public objects where missing.
2. Track source repository README modified dates in public status outputs.
3. Add claim IDs when a public project summary maps to private CV claim-ledger claims.
4. Keep README/status language synchronized with Portfolio's cross-repository evidence index.
5. Add a contract test for Auth Eco required fields.
```

## Boundary Statement

This repository is public-facing. It should not receive or expose private application exports, service records, screenshots, dashboards, source PDFs, credentials, sensitive system layouts, or private technical identifiers.
