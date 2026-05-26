# STEM CV Curator

STEM CV Curator is the object engine behind this living CV package. It is designed so a machine-learning, public-health, biomedical-data, or broader STEM researcher can clone the repository, point it at their GitHub account, and generate a public-safe CV object layer from active repositories.

## Clone-and-run use case

```bash
git clone https://github.com/pskeffington/CV-Public-Facing.git stem-cv-curator
cd stem-cv-curator
STEM_CV_OWNER=<your-github-user> make public-package
```

The build scans the configured GitHub owner's active public repositories, reads public README/status surfaces, creates structured CV objects, renders LaTeX inputs, and builds the public PDF package.

## Configuration

The default owner is stored in:

```text
data/pipeline_repos.json
```

A user can override it without editing files:

```bash
STEM_CV_OWNER=<your-github-user> make stem-cv
```

Private repository scanning is off by default. It can be enabled only when a suitable GitHub token is available:

```bash
STEM_CV_OWNER=<your-github-user> \
STEM_CV_INCLUDE_PRIVATE=true \
GH_TOKEN=<token> \
make stem-cv
```

## Inputs

The curator checks common public status surfaces:

```text
README.md
PROJECT_STATUS.md
ROADMAP.md
REPRODUCIBILITY.md
CHANGELOG.md
docs/**
```

Curated overrides live in `data/pipeline_repos.json`. These should be used to strengthen a discovered repository into a polished CV project object.

## Outputs

The object engine writes:

```text
data/stem_cv_objects.json
cv/current_projects_public.tex
research/RESEARCH_STATUS.md
research/generated_project_board.tex
research/living_source_ledger.md
research/living_repo_scan.md
```

The LaTeX/PDF build then consumes the generated `.tex` files.

## Object pipeline

```text
GitHub owner
  -> RepositoryObject
  -> RepoSurfaceObject
  -> ProjectObject
  -> ClaimObject
  -> CVSectionObject
  -> RenderTargetObject
```

## Repository classification

The curator classifies repositories into STEM CV sections using repo names and README/status text:

| Section | Typical signals |
|---|---|
| Machine Learning and Reproducible Research Tools | `ml`, `machine learning`, `model-card`, `benchmark`, `classifier`, `regression`, `neural` |
| Public Health, Infrastructure, and Environmental Evidence | `health`, `WASH`, `water`, `practicum`, `emergency`, `preparedness` |
| Biomedical Data and Signal/Imaging Methods | `ECG`, `PET`, `radiomics`, `cancer`, `signal`, `imaging`, `clinical` |
| Computational Methods and Safety Evaluation | `cipher`, `topology`, `identity`, `abuse`, `safety`, `risk`, `evaluation` |
| Archive and Public-History Indexing | `archive`, `Bonaventure`, `Hebrew`, `reliquary`, `transcription` |
| Discovered Repository Intake | default for unclassified public repositories |

## Claim gates

The curator treats claims conservatively:

- A claim is `source_supported` when README/status files are available.
- A claim is `repo_supported` when the repository exists but lacks useful status surfaces.
- Discovered repositories are marked as intake objects until curated.
- Generated intake objects should not be treated as publication, employment, award, or certification claims.

## How to promote an intake repo

Add a curated entry to `data/pipeline_repos.json`:

```json
{
  "key": "example-ml-project",
  "repo": "owner/example-ml-project",
  "title": "Example ML project",
  "status": "Active machine-learning methods repository",
  "summary": "Public machine-learning workspace for reproducible modeling and benchmark development.",
  "needs": "Add model card, benchmark target, validation checks, and public-safe results boundary.",
  "cv_section": "machine_learning",
  "source_files": ["README.md", "PROJECT_STATUS.md", "ROADMAP.md"]
}
```

Then run:

```bash
make public-package
```

## GitHub Actions

The public workflow runs the same object engine before compiling PDFs. Source repositories can notify the CV package through `repository_dispatch`, but the package also supports direct manual runs and scheduled scans.
