<!-- lingua: la -->
# Ordo operum ad editionem publicam

## Propositum

Hic ordo describit quomodo instrumentum publicum curriculi vitae effectus suos cum repositoriis fontium concordet, ita tamen ut res restrictae in curriculum vitae, descriptiones breves, relationes investigationum, registra fontium et fasciculos munerum selectorum non inserantur.

## Reparatio hodierna post coniunctionem — 2026-11-22

Fons initii est `eec77d2426a03bf13ac357efcb49ebf0e23c7c81`; [quaestio #7](https://github.com/pskeffington/CV-Public-Facing/issues/7) correctionem et recognitionem regit. Haec pars statum hodiernum definit; rationes paginarum pristinae infra tantum historiam decisionum servant.

| Res | Causa observata | Correctio et testimonium |
|---|---|---|
| Selectio operum | Custodia totum JSON quaerebat atque nomen historicum in `generated_on_note` pro opere praesenti habebat; imagines textuales in ramo etiam veteres erant. | `check_current_project_alignment.py` campos `repos[].key`, `repo`, `title` et correspondentiam trium effectuum examinat. Octo probationes indicia historica admittunt, res autem veteres, additas, duplicatas, absentes vel male formatas reiciunt. |
| Lingua consilii SEO | `docs/SEO_ROLLOUT.md` post petitionem #5 Anglice mansit sine signo linguae. | Textus re vera Latine redditus est; octo probationes custodiae et examen documentorum nullam violationem repererunt. Relatio generata Anglica adhuc in indice conversionis pendet. |
| Status operum et experientiae | Pagina introductoria opus historicum praecipuum nominabat; metadata limitem unius paginae adhuc posuerant. | Arch Notebook in selectione hodierna exhibetur; CART-TRACE sub historia tantum servatur. Experientia integra et nomen stabile fasciculi retinentur sine limite unius paginae. |
| Divulgatio documentorum | Probationes petitionum PDF inter effectus publicos mittebant, quamquam officium editionis praetermittebatur. | Tres gradus PDF et fasciculorum mittendorum cum officio editionis eandem condicionem requirunt: exsecutio manualis, `main`, `neutral`, consensus expressus et commit plenus congruens. Quinque casus negativi publicationis localiter reiecti sunt; casus congruens admissus est. |

**Status: `REVIEW`.** [Petitio #8](https://github.com/pskeffington/CV-Public-Facing/pull/8) correctionem continet; neque coniuncta neque divulgata est. Probationes locales iam superatae sunt: ambitus repositorii, custodia editionis, index novem fontium publicorum cum viginti duobus hash impeditis, octo probationes concordiae et octo probationes Latinae. Ad commit `26248025e06d9ba0b6be7d72febb5b205c6ae2ae`, [compilatio integra](https://github.com/pskeffington/CV-Public-Facing/actions/runs/45084780134) et [custodia ambitus atque linguae](https://github.com/pskeffington/CV-Public-Facing/actions/runs/45084780110) feliciter completae sunt. Tres gradus PDF mittendorum et officium editionis praetermissi sunt; effectus publicus tantum fontes textuales continuit.

Quattuor PDF eiusdem commit in probatione non publica composita sunt: curriculum academicum quattuor paginas, descriptio professionalis duas, forma ad indicem apta tres et relatio investigationum tres habuerunt. Inspectio duodecim paginarum munera pristina, honorem, statum manuscripti ante submissionem, Arch Notebook inter opera hodierna et CART-TRACE inter historica confirmavit. Duos defectus formae deprehendit: titulum subdivisionis in fine paginae sine prima re et titulum longum cum statu in descriptione professionali male divisis. Forma communis spatium ante subdivisionem reservat et statum longae rei in lineam propriam transfert; typographia relationis ad duas parvas excessiones marginis temperandas accommodatur. Haec correctio alteram compilationem et inspectionem candidati exacti requirit. Testimonium finale, commit, hashes et condiciones restantes in quaestione #7 atque petitione #8 referuntur.

Commit instrumenti generationis et fontes ex repositoriis lecti distinguendi sunt. Exsecutio ordinaria novem fontes publicos tunc praesentes legit; commit huius repositorii solus revisionem omnium fontium externorum non figit. Fontes TeX re vera compositi et hashes documentorum ad singulam probationem servantur; ante divulgationem nova lectio fontium novam recognitionem requirit.

Generatio loci novem res produxit et prima verificatio visibilitatis novem repositoria publica comprobavit. Repetita verificatio in eadem exsecutione responsa HTTP 403 accepit et compositionem, ut oportuit, sistit; haec exsecutio tota prospera non habetur. Via exemplaris Arch Notebook ad fontem publicum verum `archive/research.databases/sample_connections.sql` correcta est. Tres fontes eius per API GitHub denuo lecti sunt; novem effectus generati nunc concordant. Custodiae in CI feliciter repetitae sunt; nulla custodia propter defectum loci remissa est.

### Condiciones exitus

1. `make job-cv-package JOB_OBJECT=neutral` cum custodiis integris feliciter perficiatur.
2. Novem opera inter indicem, curriculum generatum, tabulam et relationem congruant; Arch Notebook adsit, opus historicum in selectionem praesentem ne redeat.
3. Quattuor documenta PDF pagina per paginam inspiciantur; munera, investigatio, honores et status manuscripti ante submissionem serventur.
4. In petitione coniungendi omnes gradus PDF mittendorum et officium editionis praetermittantur.
5. Post recognitionem tantum curator licentiam commit certi det. Compilatio, coniunctio rami et licentia divulgandi res distinctae manent.

### Divulgatio et revocatio

Valor `publish_verified_pdfs` per praedefinitionem `false` manet. Mutationes fontium et nuntii ordinarii novas editiones non creant. Si compilatio vel recognitio deficit, ultima editio comprobata et nexus eius servantur; candidatus corrigatur et iterum examinetur. Nulla nova editio PDF hac reparatione sola permittitur.

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
- descriptio professionalis publice tuta manet et experientiam legitimam sine limite unius paginae servat;
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

## Recognitio nova — 2026-11-22

- Repositorium publicum `pskeffington/arch_notebook` indicibus fontium admissorum additum est; documentum `README.md` et codex Rust ac SQLite probationem facultatum describunt.
- Novae descriptiones Rust et SQL tantum ad facultates in fonte publico inspectas referuntur. Facultates futuras vel iudicium externum de fructu non affirmant.
- Relationes privatae, experimenta localia nondum comprobata, atque condiciones instrumentorum adhuc imperfectorum ab hoc instrumento publico excluduntur.
- **Status: recognitio pendet.** Exsecutiones `make safety-surface-check`, `make stem-cv`, `make public-package`, examen PDF et inspectio Latinitatis ante editionem necessariae sunt.
- Nullus fasciculus PDF nec nova editio publica hac sola mutatione comprobata est.

## Consilium paginarum pristinum, revocatum — 2026-11-22

- Prima compilatio fasciculi publici in ramo recognitionis perfecta est; officium divulgationis documentorum a probatione `pull_request` recte exclusum est.
- Inspectio visiva ostendit exemplar `One_Page_Profile_Public.pdf`, quamquam unius paginae nomine inscriptum, **duas paginas** continuisse. Numerus paginarum tum vitio falso attributus est; nomen pristinum solum limitem non imponit.
- Fons `cv/one_page_profile_public.tex` ad brevem expositionem operum publicorum, scientiae Rust et SQLite, educationis ac peritiae professionalis redactum est; indicia privatorum operum non sunt inclusa.
- Custodia unius paginae tum addita postea revocata est, ut experientia legitima retineretur. Hodie integritas textus et forma paginarum, non una pagina necessaria, probantur.
- **Status: probatione pendet.** Nova compilatio et inspectio visiva requiruntur. Editio publica, tag et translatio ad situm publicum nondum permissae sunt.

## Corrigenda: opera antiqua, textus professionales — 2026-11-22

CART-TRACE e indice operum nunc selectarum remotum est. Repositorium historicum manet, sed in nova editione curriculi vitae tamquam opus praecipuum non proponitur. Arch Notebook in eius locum ponitur. Exemplar publicum ad priorem descriptionem experientiae laboris, administrationis societatis et investigationis revocatum est; finis unius paginae **non** deletionem munerum legitimorum efficere debet. Custodia novissima integritatem textus experientiae in PDF potius quam numerum paginarum examinat. Compilatio novi fasciculi et recognitio imaginum adhuc necessariae sunt.
