<!-- lingua: la -->
# Ordo operum ad editionem publicam

## Propositum

Hic ordo describit quomodo instrumentum publicum curriculi vitae effectus suos cum repositoriis fontium concordet, ita tamen ut res restrictae in curriculum vitae, descriptiones breves, relationes investigationum, registra fontium et fasciculos munerum selectorum non inserantur.

## Lex praesens

Instrumentum publicum indice fontium admissorum utitur, nisi aliter expresse decernitur.

```text
data/pipeline_repos.json
  -> public allowlist entries
  -> optional recursive intake only when explicitly enabled
  -> release-control hash registry
  -> generated public CV objects
  -> public PDFs and selected job packages
```

Lectio recursiva repositoriorum publicorum non exercetur, nisi `allow_recursive_intake` post recognitionem ad `true` mutatur. Ita repositoria nuper reperta non statim inter opera in curriculo vitae publico apparent.

## Condiciones divulgationis

Effectus publici tantum res includant quae omnes condiciones sequentes implent:

- repositorium in indice publice admisso invenitur;
- valor `public_release` est `public` vel abest;
- res a registro hash ad cohibendam divulgationem non impeditur;
- textus effectus custodiam publicae editionis superat;
- examen structurale confirmat nullam rem privatam in indicem operum publicorum pervenisse.

De rebus restrictis tantum hashes aut alia indicia non sensitiva serventur. Nomina operum restrictorum, repositoriorum privatorum vel familiarum operum sensibilium in documentis publicis non scribantur.

## Ordo operum ad concordiam renovandam

### Pars I — perfecta

- Selectio per indicem demissum rerum munerum publice tutarum instituta.
- Generatio fasciculorum pro munere electo instituta.
- Validatio registri rerum munerum addita.
- Custodia editionis publicae per hashes addita.
- Metadata indicis publici admissorum in `data/pipeline_repos.json` addita.
- Lectio recursiva per praedefinitionem inhibita.
- Res restrictae ante aestimationes, registra, JSON, relationes et fontes PDF excluduntur.

### Pars II — in progressu

- Effectus publicos post exclusionem rerum restrictarum iterum generare.
- Documenta PDF generata inspicere, ne res restrictae pateant.
- Confirmare fasciculos munerum selectorum indicia restricta non continere.
- Confirmare `blocked_release_ledger.md` tantum praefixa hash non sensitiva referre.
- Confirmare fasciculum JSON publicum ad schema `stem-cv-curator/v0.3` pertinere.

### Pars III — sequens

- Examen indicis addere quod deficit si lectio recursiva sine signo recognitionis divulgationis permittitur.
- Inspectorem effectuum generatorum ad `cv/current_projects_public.tex`, `research/RESEARCH_STATUS.md`, `research/generated_project_board.tex` et `research/living_source_ledger.md` post generationem curatoris addere.
- Indicem inspectionis effectuum publicorum fasciculis munerum addere.
- Rationem promovere qua novum opus post recognitionem in indicem publicum admittitur.

## Via renovandi effectus

Post mutationes status operum publicorum aut fasciculorum munerum exsequere:

```bash
make safety-surface-check
make stem-cv
make stem-object-contract
make stem-report-contract
make public-package
```

Pro fasciculis munerum selectorum:

```bash
make job-cv-package JOB_OBJECT="neutral"
make job-cv-package JOB_OBJECT="harvard-chan-director-data-analytics"
```

Index selectoris GitHub Actions praeceptum `make job-cv-package` exsequitur.

## Index recognitionis novi effectus

Novus effectus publicus probatur cum:

- documenta PDF curriculi publici generata sunt;
- descriptio unius paginae brevis et publice tuta manet;
- forma ad indicem apta indicia contactus non exponit;
- nomina familiarum operum restrictarum nec descriptiones vicinae apparent;
- methodi publicae verba restricta vitant;
- relatio investigationum tantum opera in indice publico admissa continet;
- relationes munerum selectorum ad munera pertinent et publice tutae sunt;
- res vetitae tantum praefixis hash non sensitivis in registro referuntur.

## Documenta concordanda

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

## Limes publicus

Hoc repositorium publicum est. Fasciculos candidaturarum privatos, nomina operum sensibilium, titulos familiarum restrictarum, secreta, vias privatas et testimonia fontium privatorum non recipiat. In dubio, res e instrumento publico excludatur et tantum in fonte privato vel fasciculo candidaturae privato servetur.
