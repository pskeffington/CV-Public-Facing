<!-- lingua: la -->
# Praecepta rationis curriculi vitae viventis

Hoc repositorium destinatur ad generationem publicam curriculi vitae viventis. Repositoria singulorum operum fontes principales statuum suorum publicorum manent. Instrumentum publicum indice permisso `data/pipeline_repos.json` utitur, permissiones divulgationis examinat, tabulam operum iterum generat et documenta PDF componit.

## Structura

```text
public allowlist update
  -> data/pipeline_repos.json
  -> release-control checks
  -> make public-package
  -> public-safe CV, profile, upload CV, and research-status PDFs
  -> workflow artifacts
```

Compositio manualis fasciculi muneris eadem via publica tuta utitur:

```text
manual workflow_dispatch
  -> select job_object dropdown
  -> make job-cv-package JOB_OBJECT=<selected>
  -> public package PDFs
  -> selected job package brief and manifest
  -> workflow artifacts
```

## Fons principalis

Index operum vivus hoc fasciculo regitur:

```text
data/pipeline_repos.json
```

Pro unoquoque opere publico index clavem stabilem, nomen repositorii, titulum publicum, classem status, summarium publice tutum, necessitates proximas, statum divulgationis et nomina fontium inspiciendorum servat.

Instrumentum generans per praedefinitionem tantum fontes ex indice publice admisso recipit. Lectio recursiva non permittitur, nisi `allow_recursive_intake` post recognitionem consulto admittitur. Hoc consilio status repositorii maturior novas assertiones in curriculo publico sponte non creat.

Index selector munerum manualis hoc fasciculo regitur:

```text
data/job_cv_objects.json
```

Res munerum sunt indicia tantum ad praesentandum publice tuta. Fasciculos candidaturarum privatos, testimonia privata nec assertiones de muneribus non probatas importare non debent.

## Res generatae

Instrumentum creat:

```text
cv/current_projects_public.tex
research/RESEARCH_STATUS.md
research/generated_project_board.tex
research/living_source_ledger.md
research/living_repo_scan.md
research/blocked_release_ledger.md
data/stem_cv_objects.json
```

Compositor fasciculorum munerum creat:

```text
dist/job_cv_packages/<selected-job>/PUBLIC_SAFE_JOB_BRIEF.md
dist/job_cv_packages/<selected-job>/manifest.json
dist/job_cv_packages/<selected-job>/*.pdf
```

Hi effectus sunt res generationis. `data/pipeline_repos.json`, `data/job_cv_objects.json` aut fontes publicos superiores emenda potius quam effectus generatos manu mutare.

## Praecepta generationis publicae

Fasciculus publicus neuter:

```bash
make public-package
```

Fasciculus muneris electi:

```bash
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="harvard-chan-director-data-analytics"
make job-cv-package JOB_OBJECT="cdc-foundation-data-modernization-senior-advisor"
```

Probationes tutelae et structurae:

```bash
make safety-surface-check
make stem-object-contract
make stem-report-contract
```

`Makefile` prius res curriculi vitae generat, deinde inspectionem et compilationem LaTeX exsequitur. Praeceptum muneris etiam registrum rerum munerum et correspondentiam indicis selectoris examinat.

## Ratio publica GitHub Actions

```text
.github/workflows/build-public-research-status.yml
```

Ratio per `workflow_dispatch` manuale cum indice `job_object`, per nuntios `repository_dispatch` e fontibus approbatis et per mutationes fontium huius repositorii incipit.

Hic processus repositorium solum legit; documenta PDF fabricat et effectus in GitHub Actions servat. Res generatas ad ramum `main` non mittit, ne circuitus generationis repetatur.

Electiones manuales hodiernae:

```text
neutral
harvard-chan-director-data-analytics
indeed-data-scientist-iii
rockland-trust-data-architect
valo-health-staff-data-scientist
unh-adjunct-homeland-security
cdc-foundation-data-modernization-senior-advisor
```

Res CDC Foundation sub titulo publico `CDC Foundation - Data Modernization Senior Advisor` redditur. Argumenta sanitatis informaticae, renovationis datorum, instructionis operariorum, gubernationis datorum, auxilii technici et analyticae reproductibilis spectat, non verba candidaturae privata neque assertiones de auctoritate aut munere sine probatione.

Effectus pro munere electo nominantur:

```text
linkedin-academic-cv-<job_object>
public-cv-package-<job_object>
selected-job-cv-package-<job_object>
public-render-sources-<job_object>
```

## Prima probatio manualis

1. Rationem `Build Public CV Package` cum `job_object=neutral` exsequere.
2. Confirma quattuor genera effectuum exstare.
3. Confirma `selected-job-cv-package-neutral` `PUBLIC_SAFE_JOB_BRIEF.md` et `manifest.json` continere.
4. Itera cum `job_object=harvard-chan-director-data-analytics`.
5. Confirma fasciculum electum relationem publice tutam Harvard Chan servare nec textum privatum revelare.
6. Itera cum `job_object=cdc-foundation-data-modernization-senior-advisor`.
7. Confirma titulum publicum CDC Foundation congruere nec verba fasciculi privati apparere.

Praecepta probationis pleniora:

```text
docs/FIRST_TEST_JOB_CV_ACTION.md
```

Ordo editionis publicae:

```text
docs/PUBLIC_RELEASE_ROADMAP.md
```

## Custodia repetitionis

Systema circuitus infinitos his praeceptis vitat:

- repositoria fontium instrumentum publicum certiorem faciunt;
- instrumentum publicum fasciculos generat;
- ratio publica effectus ad se ipsam non committit;
- mutationes actoris `github-actions[bot]` ordinariae praetermittuntur;
- concurrentia generationes duplicatas adhuc agentes tollit;
- lectio recursiva sine recognitione expresse facta vetatur.

## Additio novi repositorii operis

1. Rem in `data/pipeline_repos.json` insere.
2. Confirma `README` vel statum publice tutum adesse.
3. Confirma `public_release` ad `public` pertinere.
4. `make safety-surface-check` exsequere.
5. `make public-package` exsequere.
6. Documenta PDF et registra fontium inspice.
7. Nuntium mutationis publicae tantum si renovatio assidua necessaria est adde.
8. Rationem publicam semel manualiter exsequere, ut res nova in fontibus generatis appareat.

## Additio novae rei muneris

1. Clavem novam in `data/job_cv_objects.json` insere.
2. Tantum indicia publica tuta adhibe.
3. Eandem clavem in indice selectoris GitHub Actions adde.
4. `make job-cv-object-check` exsequere.
5. Rationem manualem cum nova re exsequere.

## Probatio localis

In exemplari locali repositorii:

```bash
python3 scripts/stem_cv_curator.py
make public-package
make job-cv-object-check
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="cdc-foundation-data-modernization-senior-advisor"
```

Haec inspice:

```text
research/living_source_ledger.md
research/blocked_release_ledger.md
documents/
dist/job_cv_packages/
```
