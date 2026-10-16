<!-- lingua: la -->
# Prima probatio — ratio fasciculi curriculi vitae pro munere selecto

## Propositum

Haec nota primam probationem manualem rationis qua fasciculus curriculi vitae publicus conficitur describit.

Ratio primum fasciculum publicum neutrum generat, deinde fasciculum ad munus delectum et publice tutum conficit. Neque fasciculos candidaturarum privatos neque testimonia privata importat.

## Ratio GitHub Actions

```text
.github/workflows/build-public-research-status.yml
```

Nomen in GitHub exhibitum:

```text
Build Public CV Package
```

## Res primae probationis

Primum rem neutram elige:

```text
neutral
```

Deinde rem Harvard Chan experire:

```text
harvard-chan-director-data-analytics
```

## Gradus probationis manualis

1. Repositorium in GitHub aperi.
2. Ad `Actions` transi.
3. `Build Public CV Package` elige.
4. `Run workflow` preme.
5. In indice `Public-safe job object to package` valorem `neutral` selige.
6. Rationem in ramo `main` exsequere.
7. Confirma exsecutionem sine errore absolutam esse.
8. Effectus depone et inspice.
9. Itera cum `harvard-chan-director-data-analytics`.

## Fasciculi exspectati

Pro probatione neutra, secundum nomina rationis hodiernae:

```text
linkedin-academic-cv-neutral
public-cv-package-neutral
selected-job-cv-package-neutral
public-render-sources-neutral
```

Pro probatione Harvard Chan:

```text
linkedin-academic-cv-harvard-chan-director-data-analytics
public-cv-package-harvard-chan-director-data-analytics
selected-job-cv-package-harvard-chan-director-data-analytics
public-render-sources-harvard-chan-director-data-analytics
```

## Contenta fasciculi muneris selecti

Fasciculus muneris selecti haec continere debet:

```text
dist/job_cv_packages/<selected-job>/Paul_A_Skeffington_Academic_CV_Public.pdf
dist/job_cv_packages/<selected-job>/Paul_A_Skeffington_One_Page_Profile_Public.pdf
dist/job_cv_packages/<selected-job>/Index_Safe_Public_Upload_CV.pdf
dist/job_cv_packages/<selected-job>/Paul_A_Skeffington_Research_Status_Public.pdf
dist/job_cv_packages/<selected-job>/PUBLIC_SAFE_JOB_BRIEF.md
dist/job_cv_packages/<selected-job>/manifest.json
```

## Examina ante generationem

Ratio exsequitur:

```bash
make job-cv-package JOB_OBJECT="<selected>"
```

Hoc praeceptum fasciculum publicum ordinarium generat et confirmat:

- registrum rerum munerum exstare;
- rem electam in registro exstare;
- omnem rem campis necessariis instructam esse;
- electiones in indice demisso clavibus registri respondere;
- primam electionem valori praedefinito congruere;
- documenta PDF publica ante compositionem fasciculi muneris exstare.

## Condicio probationis prosperae

Prima probatio succedit si:

- ratio sine errore finitur;
- quattuor genera effectuum adsunt;
- `selected-job-cv-package-*` continet `PUBLIC_SAFE_JOB_BRIEF.md` et `manifest.json`;
- nullus textus candidaturae privatae in effectu publico reperitur;
- effectus PDF fasciculo neutro respondent, nisi forma LaTeX ad munus accommodata postea consulto addatur.

## Limes

Haec ratio documenta publica pro re muneris selecta colligit. Haec ratio nondum fontes LaTeX ad singula munera plene accommodat. Probatio praesentis gradus electionem tutam, compositionem fasciculi, nomina effectuum, indicem JSON et relationem publice tutam de munere examinat.
