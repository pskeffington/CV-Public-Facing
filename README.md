# Public CV and Research Report Renderer

**Paul A. Skeffington, MS, MPH** · [Public portfolio](https://www.skeffington.us/)

This repository produces a **public-safe academic CV, concise professional profile, index-safe CV, and research-status report** from reviewed public evidence. It is a document renderer and release pipeline, **not** the authoritative archive of underlying research, a private application workspace, or an automated hiring system.

## Verified public downloads

The links below follow the **latest successful GitHub Release**. Each release includes SHA-256 checksums; unsuccessful builds do not replace the last verified publication.

| Document | Current PDF |
|---|---|
| Academic CV | [Download](https://github.com/pskeffington/CV-Public-Facing/releases/latest/download/Paul_A_Skeffington_Academic_CV_Public.pdf) |
| One-page professional profile | [Download](https://github.com/pskeffington/CV-Public-Facing/releases/latest/download/Paul_A_Skeffington_One_Page_Profile_Public.pdf) |
| Index-safe public CV | [Download](https://github.com/pskeffington/CV-Public-Facing/releases/latest/download/Index_Safe_Public_Upload_CV.pdf) |
| Research-status report | [Download](https://github.com/pskeffington/CV-Public-Facing/releases/latest/download/Paul_A_Skeffington_Research_Status_Public.pdf) |

[View versioned releases](https://github.com/pskeffington/CV-Public-Facing/releases) · [View build history](https://github.com/pskeffington/CV-Public-Facing/actions/workflows/build-public-research-status.yml)

## Public professional and research materials

- [Public academic and research summary](Dartmouth_CV.md)
- [Public and civic service positioning — Latin](hire/FOR_HIRE_LATIN.md)
- [Public research project register](data/pipeline_repos.json)
- [Publication and research status sources](research/)
- [Current CV and profile templates](cv/)

The research portfolio emphasizes translational health data science, public-health systems, longitudinal data, biomedical methods, environmental health, and reproducible analysis. **CART-TRACE** is a principal synthetic-first translational-health research example; its descriptive methodological results are not clinical decision support. Research maturity and release eligibility follow the evidence and scope limits in the public manifest, not the appearance of a project on GitHub.

## How the renderer works

```text
approved public project sources
  -> allowlist and provenance checks
  -> public-safe CV/research objects
  -> LaTeX and Markdown render inputs
  -> four PDF documents
  -> verified GitHub Release
```

The source allowlist is `data/pipeline_repos.json`. Only explicitly admitted, publicly verifiable sources may feed published claims. Private applications, sensitive records, unsupported assertions, and private research data must not enter this repository. Recursive repository intake is disabled unless separately reviewed.

The `main` branch retains **source code, policies, templates, and curated public source records**. Generated PDFs are published as GitHub Release assets rather than committed to `main`. Actions artifacts are temporary build receipts. Some generated text sources remain tracked as historical snapshots; edit their source manifests or generators instead of treating those snapshots as authoritative.

## Repository map

| Path | Purpose |
|---|---|
| `cv/` | Academic CV, profile, and public-upload LaTeX templates |
| `research/` | Research report sources, project board, and source-ledger pointers |
| `data/` | Curated public project allowlist and public-safe job render objects |
| `scripts/` | Evidence, release-safety, generation, and validation tools |
| `.github/workflows/` | Verified build and publication workflow |
| `docs/` | Governance, research/reporting methods, operating guides |
| `hire/` | Public civic-service positioning |
| `documents/` | Local PDF build destination; PDFs are delivered via Releases |

## Build and validate

Requires Python, GNU Make, and a LaTeX distribution with `latexmk`. Some source-verification checks require public GitHub access.

```bash
make public-manifest-check
make public-visibility-check
make safety-surface-check
make public-package
```

Build a public-safe, role-specific package (without importing private application documents):

```bash
make job-cv-package JOB_OBJECT="neutral"
```

The [GitHub Actions workflow](.github/workflows/build-public-research-status.yml) builds, checks, and publishes the public package after successful verification. The separate publication job validates the expected PDFs and their checksums before creating a versioned release.

## Editorial and branch governance

The root README is an English-language navigation page. Other authored, non-pointer documents use Latin under the [Latin safeguards](docs/LATIN_SAFEGUARDS.md). Generated LaTeX, JSON narrative fields, and report templates are still subject to the [recorded Latin migration scope](docs/STATUS_CONVERSIONIS_LATINAE.md); a language marker or automated scan is not scholarly certification.

- [Imperium public-evidence and release protocol](docs/IMPERIUM_PROTOCOL.md)
- [Branch and repository-scope policy](docs/REGIMEN_RAMORUM.md)
- [Contributing instructions](CONTRIBUTING.md)
- [Public manifest and output contract](PUBLIC_MANIFEST.md)
- [Public release roadmap](docs/PUBLIC_RELEASE_ROADMAP.md)
- [Build and Actions operating guide](docs/LIVING_CV_ACTIONS.md)

Use short-lived, purpose-named branches and reviewed pull requests. The `main` branch is the release source of record; application drafts belong in a private applications repository, not in public feature branches. The repository does not certify degrees, employment, publication, clinical efficacy, or institutional adoption merely by rendering a claim.

## Reuse

This is a reproducible starting point for a GitHub-driven public CV. It contains profile-specific filenames, evidence boundaries, and LaTeX layouts; another researcher must review and replace those settings and project claims before publishing under a different identity.
