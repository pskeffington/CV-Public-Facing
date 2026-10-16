<!-- lingua: la -->
# Index publicus curriculi vitae et investigationum

**Status:** repositorium publicum lectoribus apertum; fasciculus curriculi vitae publici ex fontibus iterum generari potest.

## Fontes publici

| Fasciculus | Usus |
|---|---|
| `cv/academic_cv_public.tex` | Fons LaTeX curriculi vitae academici publici |
| `cv/one_page_profile_public.tex` | Fons LaTeX brevis descriptionis unius paginae |
| `cv/public_upload_cv.tex` | Forma ad indicem apta, paucioribus indiciis personalibus |
| `cv/current_projects_public.tex` | Index operum praesentium generatus |
| `cv/publication_pipeline_public.tex` | Index communis statuum publicationis |
| `data/pipeline_repos.json` | Index repositoriorum et statuum publicorum |
| `research/RESEARCH_STATUS.md` | Relatio generata de statu investigationum et necessitatibus maioribus |
| `research/generated_project_board.tex` | Fons LaTeX tabulae operum generatae |
| `research/living_source_ledger.md` | Registrum fontium `README` et statuum inspectorum |
| `research/research_status.tex` | Fons LaTeX relationis publicae de investigationibus |
| `scripts/update_living_cv.py` | Instrumentum quod fontes publicos e repositoriis indicatis legit |
| `.github/workflows/build-public-research-status.yml` | Ratio GitHub Actions ad fasciculum publicum generandum et nuntios recipiendos |
| `Makefile` | Praecepta generationis localis |

## Effectus exspectati

| Fasciculus | Usus | Status fontis |
|---|---|---|
| `documents/Paul_A_Skeffington_Academic_CV_Public.pdf` | Curriculum vitae academicum publicum | In hoc repositorio generari potest |
| `documents/Paul_A_Skeffington_One_Page_Profile_Public.pdf` | Descriptio professionalis unius paginae | In hoc repositorio generari potest |
| `documents/Index_Safe_Public_Upload_CV.pdf` | Curriculum cum paucioribus indiciis personalibus | In hoc repositorio generari potest |
| `documents/Paul_A_Skeffington_Research_Status_Public.pdf` | Relatio imprimenda de statu investigationum | In hoc repositorio generari potest |

## Praeceptum generationis

```bash
make public-package
```

Instrumentum primum res curriculi vitae ex `data/pipeline_repos.json` et ex fontibus `README` vel statuum in repositoriis indicatis iterum generat.

## Operatio GitHub Actions

Ratio publica documenta repositorii tantum legit. Fasciculos PDF generat et sub nomine `public-cv-package` inter effectus laboris servat. Fontes generatos etiam in fasciculo `public-render-sources` colligit, ut post quamque generationem inspici possint.

Concursus exsecutionum coercetur; mutationes ordinariae actoris `github-actions[bot]` praetermittuntur, ne repetitio infinita generationis oriatur. Praecepta `workflow_dispatch`, `repository_dispatch` et mutationes ordinariae fontium servantur.

## Nuntii e repositoriis fontium

Repositoria fontium continere possunt `.github/workflows/notify-living-cv.yml`. Mutatis `README`, statu vel documentis, haec ratio nuntium `repository_dispatch`, generis `living-cv-source-updated`, mittit, si secretum `LIVING_CV_DISPATCH_TOKEN` rite constitutum est.

## Lex tutelae publicae

In hoc repositorio licent documenta Markdown publica, LaTeX purgatum, metadata repositorii, res curriculi generatae atque documenta PDF publica.

Ne includantur:

- fontes LaTeX privati;
- registra assertionum privata;
- excerpta fontium privatorum;
- inscriptiones domicilii, numeri telephonici, epistulae personales, dispositiones situs domestici aut infrastructurae sensibiles;
- assertiones nondum probatae de publicationibus, stipendiis investigationis, muneribus, praemiis aut certificationibus.

Documenta propria non directoria Latine scribantur; nexus ad fontes superiores et syntaxis machinarum servetur.

## Renovatio localis

```bash
git pull --ff-only
make public-package
```
