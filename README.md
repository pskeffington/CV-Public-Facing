# Public CV Renderer

This repository builds the public-safe CV, one-page profile, index-safe upload CV, and research-status package for Paul A. Skeffington. It also serves as a cloneable public CV renderer for researchers who want a GitHub-driven, source-ledgered CV package.

The repository is intentionally public. It must contain only public-safe source text, public project summaries, generated public artifacts, and non-sensitive build metadata.

**Maintainer:** Paul Skeffington, MS, MPH  
**Repository status:** active public-safe CV and research-status renderer.  
**Last documentation refresh:** 2026-08-21

## Public-Interest Research Boundary

This repository is maintained for public-interest research, scholarly documentation, reproducible professional presentation, and public-safe portfolio evidence. It supports transparent CV generation, verified public project summaries, source-ledgered claims, and human-reviewed career or scholarship materials.

It does not publish private job packets, private source records, restricted project-family names, secrets, credentials, private paths, sensitive implementation details, private review scores, or automated hiring decisions. Outputs are intended to support documentation, quality review, and public scholarly presentation.

## Current Research Status

The current public portfolio is centered on translational health data science, longitudinal clinical data, biomedical signal and imaging methods, public-health systems research, reproducible analytics, and source-bounded evidence translation.

**CART-TRACE is the principal public translational-health data-science anchor.** Its public capstone package has reached final scholarly freeze after synthetic-first development of deterministic 30-day post-infusion hospital care-trajectory reconstruction, utilization metrics, provenance-preserving transformations, explicit missingness behavior, reproducibility controls, and computational validation against controlled synthetic truth. The project remains retrospective and descriptive and does not function as clinical decision support.

CART-TRACE also contains a separate synthetic administrative access-gating research extension. That extension is tracked as a developing methods object and is not promoted here as evidence of clinical eligibility determination, payer authorization, financial clearance, treatment readiness, or institutional workflow validation.

Current work in this repository emphasizes public-safe rendering, source-bounded claims, transparent limitations, and human-reviewed outputs. The renderer does not promote a public CV claim unless the corresponding project is explicitly allowlisted and passes public-release controls.

### Current Stage

- Stage: Active public renderer / professional evidence surface
- Evidence status: Public project summaries and source-bounded CV claims are maintained through the public allowlist and release controls
- Primary translational-health evidence source: `pskeffington/CART-TRACE`
- CART-TRACE evidence state: frozen synthetic capstone package approved for public portfolio use; access-gating extension remains a candidate research-method object
- Data status: Public-safe source text, public project summaries, generated artifacts, and non-sensitive build metadata only
- Primary limitation: Requires continued release review as portfolio projects mature and authenticated cross-repository validation is completed upstream

### Recent Progress

- Reconciled CART-TRACE from thesis-scaffold language to its final frozen synthetic capstone evidence state
- Preserved separation between the frozen capstone and the newer synthetic administrative access-gating extension
- Reframed the public portfolio around longitudinal clinical data, translational health data science, reproducible evidence, biomedical methods, and public-health systems analysis
- Removed the legacy NAVSEA public job object and its GitHub Actions selector to keep the public renderer research- and civilian-facing
- Public research entries remain source-ledgered and bounded by upstream evidence state
- NLSY79 status remains under peer review with reproducible model and sample-audit language
- McDowell rural water/wastewater work remains a completed applied public-health project with final oral/media delivery tracked separately
- Humanitarian WASH work remains separated from rural infrastructure work so methods and application claims do not collapse into one evidence object
- Public-release boundaries remain enforced; internal valuation and scoring do not render into public CV outputs

### Next Actions

- Rebuild the neutral public package from the reconciled CART-TRACE evidence sources
- Review rendered PDFs for translational-health positioning, claim status, and layout consistency
- Keep `data/pipeline_repos.json` synchronized with mature public project evidence
- Add release-review receipts where appropriate
- Replace older distribution copies with date-stamped exports from the reconciled build

## Current Operating Model

`CV-Public-Facing` is the public renderer in the broader CV and application ecosystem.

```text
validated public research evidence
  -> public-safe CV/status rendering
  -> public portfolio surfaces
  -> application/job package alignment
```

The public project register is an allowlist by default. The renderer reads `data/pipeline_repos.json`, applies public-release checks, generates LaTeX/Markdown source objects, and compiles PDFs. Recursive public repository intake is disabled unless explicitly reviewed and enabled.

Internal scoring remains a build-review aid only. It does not belong in final public PDFs. The public research-status report ends with a skill-scan appendix that summarizes market-ready skill demonstrations and separates developing skills into a training-stage section.

## Build Outputs

Generated PDF paths:

```text
documents/Paul_A_Skeffington_Academic_CV_Public.pdf
documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf
documents/Index_Safe_Public_Upload_CV.pdf
documents/Paul_A_Skeffington_Research_Status_Public.pdf
```

The skill-scan appendix source is:

```text
cv/skill_scan_report_public.tex
```

It is included at the bottom of:

```text
research/research_status.tex
```

Selected job-package outputs are written under:

```text
dist/job_cv_packages/<selected-job>/
```

## Main Commands

Build the neutral public package:

```bash
make public-package
```

Build a selected public-safe job package:

```bash
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="harvard-chan-director-data-analytics"
make job-cv-package JOB_OBJECT="cdc-foundation-data-modernization-senior-advisor"
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

It supports manual `workflow_dispatch` with a `job_object` dropdown. The dropdown builds the public CV package, then wraps the selected public-safe job object in a brief, manifest, and artifact bundle.

Current job objects are controlled by:

```text
data/job_cv_objects.json
```

Current selectable objects include:

```text
neutral
harvard-chan-director-data-analytics
indeed-data-scientist-iii
rockland-trust-data-architect
valo-health-staff-data-scientist
unh-adjunct-homeland-security
cdc-foundation-data-modernization-senior-advisor
```

The CDC Foundation object is titled `CDC Foundation - Data Modernization Senior Advisor` and is scoped to public-safe public health informatics, data modernization, technical assistance, workforce upskilling, data governance, and reproducible analytics framing.

## Public-Release Boundaries

This repository should not contain private job packets, private source records, restricted project-family names, secrets, credentials, private paths, or sensitive implementation details.

Public outputs may include only projects that satisfy all of the following:

- the project is present in the public allowlist;
- the release state is public;
- the project is not matched by the release-control hash registry;
- generated rendered sources pass the public-release guard;
- generated object contracts confirm no non-public project entered the public project list.

Internal scores and review metrics may remain in generated object JSON or internal ledgers, but they should not render into public PDFs. Public skill evidence should be presented only as a skill-scan appendix with mature skills listed as market-ready and developing skills listed as training-stage.

## Start Here

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

Read the CV/Portfolio synchronization status:

```text
docs/CV_PORTFOLIO_SYNC_STATUS.md
```

## Clone and Run for Another Public Profile

```bash
git clone https://github.com/pskeffington/CV-Public-Facing.git public-cv-renderer
cd public-cv-renderer
STEM_CV_OWNER=<your-github-user> make public-package
ls documents/
```

The filenames are configured for this profile by default and can be renamed in the Makefile for another user.

## Object Engine

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

## Development Notes

The repo has no Python package manager file at this time. Build and validation are Makefile-driven. Generated public PDFs are workflow artifacts and are not pushed back to `main` by the workflow.
