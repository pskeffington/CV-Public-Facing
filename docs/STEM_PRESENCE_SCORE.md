<!-- lingua: la -->
# Nota praesentiae disciplinarum STEM

Nota `STEM Presence Score` est mensura deterministica et examinabilis quae aestimat quantum scriptum, opus, repositorium aut res curriculi vitae cum progressu scientiae, technologiae, ingeniariae et mathematicae (STEM) congruat.

Haec nota ad ordinanda testimonia publici indicis operum destinatur. Veritatem scientificam, qualitatem recognitionis academicorum aut effectum socialem non iudicat. Solum indicat utrum documentum publicum argumenta STEM concreta praebeat: disciplinam definitam, methodos, reproductionem, validationem, mensuras atque effectus traditos.

## Campi effectuum

Quaeque res aestimata obiectum `stem_presence` accipit:

```json
{
  "score": 76,
  "drift_score": 24,
  "band": "core_stem",
  "rationale": "core_stem score 76/100 based on domain terms=...",
  "matched_domain_terms": [],
  "matched_method_terms": [],
  "matched_reproducibility_terms": [],
  "matched_progress_terms": [],
  "matched_drift_terms": []
}
```

Valor `score` inter 0 et 100 praesentiam STEM aestimat; `drift_score` ex `100 - score` computatur et declinationem a progressu disciplinarum indicat.

## Classes

| Classis | Intervallum | Interpretatio |
|---|---:|---|
| `core_stem` | 75–100 | Argumenta firma disciplinae, methodorum, reproductionis et progressus concreti |
| `stem_adjacent` | 55–74 | Connexio clara cum STEM, sed una vel plures probationes methodi vel progressus desunt |
| `mixed_or_transitional` | 35–54 | Quaedam indicia STEM apparent; narratio tamen rudis vel adhuc in primo evolutionis gradu esse potest |
| `low_stem_presence` | 0–34 | Pauca indicia publica progressus STEM vel magna declinatio a testimoniis |

## Ratio computationis

Computatio in vocabulario nititur atque consulto perspicua est. Quattuor partes ponderantur:

| Pars | Pondus | Exempla notionum |
|---|---:|---|
| Disciplina definita | 35 | scientia, ingeniaria, salus publica, biomedicina, disciplina machinarum, copia datorum, algorithmus |
| Methodi et mensurae | 30 | methodus, analysis, hypothesis, regressio, validatio, mensura, robur |
| Reproducibilitas | 20 | codex, repositorium, index, descriptio exemplaris, processus, documenta, probatio |
| Progressus et effectus | 15 | eventus, scriptum submissum, exemplar manuscripti, recognitio collegarum, figura, opus perfectum, terminus |

Poena declinationis usque ad 25 puncta additur ubi documenta publica potissimum memoriam personalem, symbola, sermonem promotionis, coniecturas aut tantum locos vacuos sine probatione exhibent.

## Instrumenta coniuncta

Mensura in hoc codice exstat:

```text
scripts/stem_presence.py
```

Scriptum vel documentum publicum separatim examinari potest:

```bash
python3 scripts/stem_presence.py --pretty paper.md
cat paper.txt | python3 scripts/stem_presence.py --pretty
```

Ratio curriculi vitae his instrumentis utitur:

```text
scripts/stem_cv_curator.py
scripts/write_stem_presence_report.py
```

Relatio generata:

```text
research/stem_presence_report.md
```

## Probationes locales

In radice repositorii exsequere:

```bash
make stem-presence-check
make stem-object-contract
make stem-report-contract
```

Probationes structurales confirmant res generatas mensuras `stem_presence` validas continere et tabulam Markdown cum rebus JSON congruere.

## Interpretatio et limites

Haec mensura signum ad prioritatem recognitionis constituendam est, non iudicium personae. Nota humilis saepe significat documentum `README` vel statum publicum plura de methodis, datis, validatione aut reproductione requirere. Nota alta significat narrationem publicam argumentis technicis ad curriculum vitae STEM facilius fulciri posse. Nulla nota scientiae veritatem vel aptitudinem hominis per se probat.
