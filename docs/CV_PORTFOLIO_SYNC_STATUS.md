# CV / Portfolio Synchronization Status

**Review date:** 2026-08-06  
**Scope:** private CV workspace, public CV renderer, Portfolio evidence index, and Google Drive distribution copies

## Source-of-truth hierarchy

1. `pskeffington/CV` is the private claim-controlled master for CV and resume content.
2. `pskeffington/Portfolio` is the cross-repository project and evidence index. Project status should be promoted into CV prose only after the supporting repository evidence is reviewable and the claim boundary is clear.
3. `pskeffington/CV-Public-Facing` is the public-safe renderer. It should receive only claims and project summaries cleared for public release.
4. Google Drive is a distribution and coordination layer for rendered or review copies. Drive copies should be regenerated from the reconciled GitHub sources rather than edited as independent masters.

## Current reconciliation finding

The Portfolio repository advanced materially after the July 3 documentation refresh. On July 21-22, it added and expanded the portfolio valuation-manifest standard, cross-repository manifest validation, deterministic validation tests, registry reconciliation, exception handling, and Phase 1 validation/data-integrity status documentation.

Those changes strengthen the evidence-governance layer but do not, by themselves, create new CV claims. They support stronger language around reproducible evidence controls, cross-repository validation, source-to-claim governance, deterministic checks, and portfolio-level reconciliation.

## CV promotion rule

A portfolio item may enter the master CV when its description can be stated as:

**Problem -> Method -> Deliverable -> Intended use**

and when the status language is supported by repository evidence.

Use conservative stage terms such as:

- active
- developing
- in preparation
- under review
- validated internally
- external validation pending

Avoid converting internal valuation, readiness, scoring, or architecture metadata into claims of market value, production readiness, institutional adoption, clinical effectiveness, or external validation.

## Public-export rule

The public renderer should contain only public-safe project names, methods, outputs, and status statements. Private paths, restricted evidence, private job materials, internal valuation ranges, implementation-sensitive details, and unsupported impact claims remain outside the public CV.

## Google Drive synchronization

The currently located Drive CV artifacts predate the July 21-22 portfolio reconciliation work. They should be treated as historical distribution copies until rebuilt from the reconciled GitHub sources.

Next distribution cycle:

1. reconcile private CV claims against Portfolio evidence;
2. update the public-safe project register and CV source;
3. build the master and public CV artifacts;
4. review rendered PDFs for claim and layout consistency;
5. replace or supersede the corresponding Google Drive copies with date-stamped exports.

## Immediate documentation priorities

- refresh repository README status language where it still reflects the July 3 state;
- review the master CV research/project section against the current Portfolio evidence index;
- review the public CV project register for items whose status has matured or changed;
- keep the NLSY79, WASH/rural infrastructure, biomedical methods, and evidence-governance lines distinct enough to remain credible while presenting one coherent research identity;
- keep public-facing language scholarly, civic-facing, research-oriented, non-operational, and explicit about limitations.
