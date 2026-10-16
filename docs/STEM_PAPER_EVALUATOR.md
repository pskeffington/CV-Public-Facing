<!-- lingua: la -->
# Aestimator scriptorum STEM

Instrumentum `STEM Paper Evaluator` est praecipua via ad scripta submissa examinanda secundum congruentiam cum disciplinis STEM, integritatem citationum et indicia publicationum auctoris.

Tres partes componit:

1. Praesentiam STEM et declinationem per `scripts/stem_presence.py`.
2. Extractionem citationum et verificationem externam facultativam per `scripts/stem_citation_verifier.py`.
3. Notam compositam totius fasciculi scripti, in una re JSON examinabili.

## Instrumentum

```text
scripts/stem_paper_evaluator.py
```

## Usus sine nexu externo

```bash
python3 scripts/stem_paper_evaluator.py --pretty paper.md
cat paper.txt | python3 scripts/stem_paper_evaluator.py --pretty
```

Haec ratio deterministica et ad CI apta est. Identificatores citationum extrahit, praesentiam STEM metitur et notam compositam reddit, sine interrogationibus servitiorum externorum.

## Usus cum nexu externo

```bash
python3 scripts/stem_paper_evaluator.py --pretty --live --author "Jane Researcher" paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --orcid "0000-0000-0000-0000" paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --author "Jane Researcher" --max-author-candidates 5 paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --allow-url-host example.org paper.md
python3 scripts/stem_paper_evaluator.py --pretty --live --block-url-host private.example paper.md
python3 scripts/stem_paper_evaluator.py --pretty --stem-weight 0.85 --publishing-weight 0.15 paper.md
```

Ratio externa fines citationum publicos interrogare et indicia publicationis auctoris petere potest. Si auctor per nomen tantum reperitur, convenientia identitatis prius ab homine recognoscenda est.

## Custodia inscriptionum URL

Interrogationes URL cohiberi possunt sine intermissione examinandi DOI, PMID, arXiv et OpenAlex:

```bash
python3 scripts/stem_paper_evaluator.py --pretty --live --allow-url-host example.org paper.md
python3 scripts/write_stem_paper_review.py --live --allow-url-host example.org --out review.md paper.md
```

Optio `--allow-url-host` interrogationes ad dominia enumerata et subdominia eorum restringit. `--block-url-host` ea vetat. Utraque optio iterari potest; regula vetiti, si ambae adsunt, praevalet.

Citationes URL a regula prohibitae in effectu bruto manent, valorem `verification_mode: live_policy_blocked` accipiunt atque `policy_blocked_reference_count` in summario augent.

## Res effectus

```json
{
  "live": false,
  "review_configuration": {},
  "stem_presence": {},
  "publishing_signal_summary": {},
  "composite_paper_score": {},
  "citation_verification": {}
}
```

## Registrum configurationis

Quisque effectus aestimatoris rationem qua generatus est retinet:

```json
{
  "live": false,
  "max_author_candidates": 5,
  "composite_stem_weight": 0.75,
  "composite_publishing_weight": 0.25,
  "reference_signal_weight": 0.65,
  "author_signal_weight": 0.35,
  "allowed_url_hosts": [],
  "blocked_url_hosts": [],
  "external_services_enabled": [
    "local_stem_presence",
    "identifier_extractor"
  ]
}
```

In ratione externa `external_services_enabled` etiam `crossref`, `ncbi_pubmed_esummary`, `arxiv_api`, `openalex` et `raw_url_ping` continere potest. Hoc registrum inspectionem JSON et Markdown reproducibilem facit.

## Pondera computationis

Nota composita per praedefinitionem praesentiam STEM maiori pondere aestimat:

```text
composite_score = STEM presence * 0.75 + publishing_signal * 0.25
publishing_signal = average_reference_score * 0.65 + author_signal_score * 0.35
```

Pondera summa ad examen sensibilitatis mutari possunt:

```bash
python3 scripts/stem_paper_evaluator.py --pretty --stem-weight 0.85 --publishing-weight 0.15 paper.md
python3 scripts/write_stem_paper_review.py --stem-weight 0.85 --publishing-weight 0.15 --out review.md paper.md
```

Pondera accepta ante computationem normalizantur et in `review_configuration` servantur. Pondera inter citationes et auctorem nunc fixa sunt ad 0.65 et 0.35.

## Campi notae compositae

```json
{
  "stem_presence_score": 76,
  "stem_drift_score": 24,
  "publishing_signal_score": 42,
  "composite_score": 68,
  "composite_drift_score": 32,
  "band": "credible_stem_paper_package",
  "rationale": "...",
  "review_flags": [
    "references_not_live_verified",
    "no_verified_author_signal"
  ]
}
```

Pondus STEM 75 ex centum, signorum publicationis 25 ex centum est in ratione praedefinita. Contextus citationum non est mensura absoluta veritatis scientificae.

## Classes

| Classis | Interpretatio |
|---|---|
| `strong_stem_paper_package` | Argumenta STEM firma cum citationibus et signis publicationis fulcientibus |
| `credible_stem_paper_package` | Argumenta STEM credibilia, quamvis testimonia citationum aliqua deesse possint |
| `mixed_or_underverified_package` | Argumenta STEM partialia, documenta tenuia vel verificatio imperfecta |
| `high_drift_or_low_evidence_package` | Magna declinatio aut parum testimoniorum ad assertiones STEM publicas |

## Summarium publicationis

Evaluator continet:

```json
{
  "reference_count": 3,
  "verified_reference_count": 0,
  "average_reference_score": 50.0,
  "author_signal_score": 0,
  "cited_by_count": null,
  "works_count": null,
  "h_index": null,
  "i10_index": null,
  "author_candidate_count": 0,
  "author_ambiguity_warning": null,
  "author_match_confidence": "offline_unverified",
  "policy_blocked_reference_count": 0,
  "source_provenance": [
    "reference:identifier_extractor:offline",
    "author_profile:openalex:offline_unverified"
  ]
}
```

Sine interrogationibus externis valor `verified_reference_count` plerumque nullus est; ratio externa non currit.

## Signa admonitionis

| Signum | Interpretatio |
|---|---|
| `high_stem_drift` | Declinatio STEM satis magna est ut accuratior inspectio requiratur |
| `no_references_extracted` | Nulla citatio DOI, arXiv, PMID aut URL reperta |
| `references_not_live_verified` | Citationes repertae sunt, sed non externis fontibus verificatae; hoc in CI sine nexu exspectatur |
| `reference_url_policy_blocked` | Una vel plures inscriptiones URL a regula permissionis aut vetiti inhibitae |
| `author_identity_ambiguous` | Investigatio nominis auctoris plures candidatos aut dubitationem rettulit |
| `no_verified_author_signal` | Nulla nota citationum auctoris externe verificata adest aut nota est nulla |
| `author_match_unconfirmed` | Identitas auctoris nondum confirmata, quia conventio abest, errat vel sine nexu est |

## Relatio Markdown

Instrumentum relationis eodem evaluatore utitur et configurationem, notas, signa, originem probationum atque tabulam citationum reddit:

```bash
python3 scripts/write_stem_paper_review.py --title "Submitted manuscript" --out review.md paper.md
python3 scripts/write_stem_paper_review.py --live --allow-url-host example.org --out review.md paper.md
python3 scripts/write_stem_paper_review.py --stem-weight 0.85 --publishing-weight 0.15 --out review.md paper.md
```

## Origo et dubia identitas

`source_provenance` fontes signorum publicationis servat. Sine nexu `reference:identifier_extractor:offline` adhibetur. Verificatio externa DOI ad Crossref, PMID ad NCBI PubMed ESummary, arXiv ad API arXiv referri potest. Citationes URL a regula prohibitae `live_policy_blocked` portant.

Campi `author_candidate_count`, `author_ambiguity_warning` et `author_match_confidence` dubitationem de identitate auctoris ex OpenAlex declarant. Investigatio per nomen plures personas similes reperire potest. Ubi praesto est, ORCID praeferatur.

## Tabula systematum propinquorum

Instrumentum cum systematibus litterarum et citationum comparatur in:

```text
docs/STEM_EVALUATOR_LIT_REVIEW_MATRIX.md
```

Tabula facultates Crossref, OpenAlex, Semantic Scholar, PubMed/NCBI E-utilities, OpenCitations, systematum contextus citationum similium scite et systematum retractationis vel integritatis exponit. Lacunas instrumenti et melioramenta futura etiam indicat.

## Probationes locales

```bash
make paper-evaluator-check
make paper-review-check
```

Hae probationes sine nexu currunt. Confirmant instrumentum ex scripto ficto ad similitudinem manuscripti notam compositam, structuram JSON validam et relationem Markdown cum configuratione, ponderibus et originibus generare.

## Fines interpretationis

Evaluator est auxilium prioritatum recensionis, non substitutum recognitionis academicae, inspector plagii, certificator auctoritatis vel index veritatis. Structura adiuvat ad intellegendum num fasciculus scientiam STEM demonstrat et num citationes ac signa publicationis auctoris externe verificari possunt.
