<!-- lingua: la -->
# Curator curriculi vitae STEM

`STEM CV Curator` est instrumentum ad res curriculi vitae ordinandas, quo fasciculus publicus continenter renovari potest. Investigator disciplinarum mathematicarum, scientiae datorum biomedicorum, salutis publicae vel ceterarum STEM repositorium exscribere potest, rationem GitHub propriam indicare, atque res curriculi vitae publice tutas ex repositoriis activis generare.

## Exemplar exscribendi et exsequendi

```bash
git clone https://github.com/pskeffington/CV-Public-Facing.git stem-cv-curator
cd stem-cv-curator
STEM_CV_OWNER=<your-github-user> make public-package
```

Instrumentum repositoria publica activa domini GitHub constituti inspicit, fontes `README` et status legit, res ordinatas CV creat, fontes LaTeX reddit et fasciculum PDF publicum componit.

## Configuratio

Dominus praedefinitus hic servatur:

```text
data/pipeline_repos.json
```

Dominus sine mutatione fasciculi substitui potest:

```bash
STEM_CV_OWNER=<your-github-user> make stem-cv
```

Inspectio repositoriorum privatorum per praedefinitionem inhibetur. Exemplis localibus, ubi ius aditus recte constitutum est, hanc facultatem solum sub tutela privata adhibe:

```bash
STEM_CV_OWNER=<your-github-user> STEM_CV_INCLUDE_PRIVATE=true GH_TOKEN=<token> make stem-cv
```

Nulla indicia privata ex tali inspectione in effectum publicum promoveantur.

## Fontes recepti

Curator documenta communia statum operum describentia examinat:

```text
README.md
PROJECT_STATUS.md
ROADMAP.md
REPRODUCIBILITY.md
CHANGELOG.md
docs/**
```

Exceptiones curatae in `data/pipeline_repos.json` manent. Eae adhibentur ut repositorium repertum in rem operis accuratius descriptam convertatur.

## Effectus

```text
data/stem_cv_objects.json
cv/current_projects_public.tex
research/RESEARCH_STATUS.md
research/generated_project_board.tex
research/living_source_ledger.md
research/living_repo_scan.md
```

Compositor ex fontibus LaTeX generatis documenta PDF deinde conficit.

## Ordo rerum

```text
GitHub owner
  -> RepositoryObject
  -> RepoSurfaceObject
  -> ProjectObject
  -> ClaimObject
  -> CVSectionObject
  -> RenderTargetObject
```

## Classificatio repositoriorum

Curator repositoria secundum nomina et textus `README` vel status in partes CV STEM dividit.

| Pars | Indicia communia |
|---|---|
| Instrumenta discendi machinarii et investigationis reproducibilis | `ml`, `machine learning`, `model-card`, `benchmark`, `classifier`, `regression`, `neural` |
| Salus publica, infrastructura et res ad ambitum pertinentes | `health`, `WASH`, `water`, `practicum`, `emergency`, `preparedness` |
| Data biomedica et methodi signorum imaginumque | `ECG`, `PET`, `radiomics`, `cancer`, `signal`, `imaging`, `clinical` |
| Methodi computationales et examen securitatis | `cipher`, `topology`, `identity`, `abuse`, `safety`, `risk`, `evaluation` |
| Index archivi et historiae publicae | `archive`, `Bonaventure`, `Hebrew`, `reliquary`, `transcription` |
| Repositoria noviter inventa | Valor praedefinitus, ubi nulla alia classis convenit |

## Custodiae assertionum

Curator cautus est:

- `source_supported`: fontes `README` aut status adsunt.
- `repo_supported`: repositorium exstat, sed documenta status utilia desunt.
- Repositoria reperta ut res ingressus notantur, donec recognita sint.
- Res ingressus generatae non pro publicationibus, muneribus, praemiis aut certificationibus habeantur.

## Promotio repositorii reperti

In `data/pipeline_repos.json` inscriptionem curatoriam adde:

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

Haec exempla JSON ad convenientiam cum codicibus hodiernis immutata servantur. Tum exsequere:

```bash
make public-package
```

## GitHub Actions

Ratio publica eodem curatore ante compilationem PDF utitur. Repositoria fontium nuntios `repository_dispatch` mittere possunt; instrumentum etiam exsecutiones manuales sustinet. Lectio recursiva solum post recognitionem admittitur.
