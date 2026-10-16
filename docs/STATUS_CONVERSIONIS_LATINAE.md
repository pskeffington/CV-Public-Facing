<!-- lingua: la -->
# Status conversionis in linguam Latinam

**Dies recensionis:** 2026-10-16  
**Repositorium:** `pskeffington/CV-Public-Facing`

## Partes confectae

Documenta Markdown manu conscripta in radice, in directorio `docs/` et in directorio `hire/` Latine conversa sunt, nominibus propriis, titulis operum, identificatoribus technicis et citationibus integris servatis. `README.md` radicis manet exceptio lectoribus destinata.

`research/living_source_ledger.md` est index directorius ad fontes superiores; ne pro narratione nova habeatur.

Examen automaticum `scripts/check_latin_safeguards.py` requirit signum `<!-- lingua: la -->` et sententias manifesto Anglicas, post signum positum, detegere conatur. Probationes unitatis in `scripts/test_latin_safeguards.py` sunt. Signum et index vocabularii linguam per se non certificant; recognitio humana adhuc necessaria est.

## Altera recognitio grammaticae — 2026-10-16

Documenta Latina ab auctore conscripta iterum lecta sunt, et locutiones selectae ratione grammaticae, perspicuitatis atque constantiae vocabulorum emendatae sunt. Recognitio haec praecipue attigit:

- curriculum vitae brevius (`Dartmouth_CV.md`) et regulas conferendi (`CONTRIBUTING.md`);
- documenta de concordia systematum, fontibus curriculi vitae et custodia editionis publicae;
- praecepta exsecutionis fasciculorum, indicem rerum et descriptiones instrumentorum STEM;
- notam de munere UNH et normam vocabularii Latini.

Praecipue correcti sunt casus nominum, concordia verborum, structura sententiarum et vocabula technica male translata. Voces quae sunt partes codicis, nomina optionum, inscriptiones viarum, claves JSON et citationes e fontibus non mutatae sunt.

Normae repositorii `trans-latin` ad mutationes observandas et consuetudinem recensionis comparandam consuluntur. Quia illae normae imprimis ad transcriptionem testium historicorum pertinent, **non** habentur pro instrumento automatico quod Latinitatem recentem perfecte probet. Haec recognitio editorialis certificationem philologicam externam non constituit.

## Opera restantia — non pro conformibus habenda

| Genus | Fontes | Ratio emendandi |
|---|---|---|
| Relatio Markdown generata | `research/RESEARCH_STATUS.md` | Fontes et exemplaria in `scripts/stem_cv_curator.py` atque `scripts/update_living_cv.py` corrigenda |
| Narrationes LaTeX | `cv/*.tex`, `research/*.tex` | Verba propria et tituli ad publicum Latine reddenda; mandata LaTeX servanda |
| Narrationes in JSON | `data/pipeline_repos.json`, `data/job_cv_objects.json` | Campi narrationis convertendi, clavibus ac valoribus selectionis intactis |
| Relationes generatae | `scripts/build_job_cv_package.py`, `scripts/write_stem_paper_review.py`, `scripts/write_stem_presence_report.py` | Textus in exemplaribus generationis Latine ponendus |
| Commentarii technici | `scripts/*.py`, `.github/workflows/*.yml`, `Makefile` | Commentarii auctoris et nuntii ad humanum lectorem vertendi, sine mutatione codicis |

Hi loci gradum transitionis indicant; non probatur omnes iam Latine redditos esse. Res generatae non manu solum mutentur, nam nova generatio mutationes amitteret.

## Exceptiones perpetuae

- `README.md` principale, ad navigationem simplicem.
- Fasciculi qui tantum ad fontes superiores ducunt, et citationes vel inscriptiones fontium.
- Claves JSON, nomina variabilium, voces ad rationem systematis pertinentes, DOI, URL, mandata, citationes integrae, syntaxis LaTeX et nomina institutionum.

## Custodia prior publicationem

1. Fontes probatos et fines assertionum servare.
2. Prosa nova propria Latine parare, codice et nexibus non corruptis.
3. `python3 scripts/test_latin_safeguards.py` exsequi.
4. `python3 scripts/check_latin_safeguards.py` exsequi.
5. Probationes editionis publicae et compositionis PDF exsequi.
6. Documenta finalia humana recognitione probare.

Omnis defectus instrumentorum impediens corrigendus est antequam plena conformitas declarari possit.
