# CV-Public-Facing Ecosystem Alignment

Author: Paul Skeffington, MS, MPH  
Status: public-facing alignment note  
Last updated: 2026-05-26

## Purpose

This note aligns `CV-Public-Facing` with the broader Portfolio, private CV, ML Role Matcher, and audit-tooling ecosystem.

This repository remains the public-safe renderer. It should turn approved repository surfaces, claim objects, and status objects into public CV/status outputs without inventing unsupported claims.

## Ecosystem Position

```text
private CV claim controls
  -> public-safe CV object engine
  -> public CV/profile/research-status outputs
  -> Portfolio proof-packet hub
  -> ML Role Matcher role-match / audit-chain artifacts
```

## Source of Truth Boundaries

```text
Private claim control: pskeffington/CV
Public rendering: pskeffington/CV-Public-Facing
Portfolio proof packet hub: pskeffington/Portfolio
Audit-specific controls: pskeffington/authentication-audit-compiler
```

This repo should not become the sole source of truth for private claims. It should render public-safe objects from approved inputs.

## Shared Object Vocabulary

The existing STEM CV objects should remain compatible with the Portfolio/ML Role Matcher vocabulary:

```text
RepositoryObject
RepoSurfaceObject
ProjectObject
ClaimObject
SourceObject
PublicSurfaceObject
OutputObject
DriftScoreObject
```

Recommended additions for ecosystem fluidity:

```text
source_ids
claim_ids
public_safety_boundary
review_status
generator_name
generator_version
use_boundary
```

## Public-Safe Claim Rule

No public-facing sentence should be generated unless it can point to at least one of:

```text
public repository surface
approved claim ledger entry
public-safe source extract
generated project/status object
fixture-only label clearly declared
```

## Integration With ML Role Matcher

ML Role Matcher produces role-match and audit-chain artifacts in `pskeffington/Portfolio/tools/ml_role_matcher`.

CV-Public-Facing can consume public-safe summaries from those artifacts only when they are clearly bounded as:

```text
portfolio evidence
role-matching fixture
public-safe technical project summary
not autonomous hiring output
```

## Integration With Authentication Audit Compiler

Authentication-audit outputs should enter this public-facing repo only as generalized, public-safe professional claims.

Do not render:

```text
live findings
sensitive authentication details
credentials
private logs
exploit paths
restricted infrastructure identifiers
```

## Drift Controls

The public CV/status engine should continue to flag drift when:

```text
repository surface lacks structured status
claim lacks source
claim exceeds public-safe evidence
project status is stale
paper/citation signal is unverified
private detail appears in public output
```

## Immediate Alignment Tasks

```text
1. Add optional source_ids and claim_ids to generated public objects where practical.
2. Map Portfolio flagship tracks to ProjectObject records.
3. Treat ML Role Matcher outputs as evidence artifacts, not hiring decisions.
4. Add authentication-audit-compiler as an audit tooling project only after public-safe summary exists.
5. Preserve public/private boundaries from the private CV repo.
```

## Use Boundary

This repository generates public-safe CV, profile, and research-status outputs. It should not publish private source material or treat role-matching fixture scores as hiring decisions.
