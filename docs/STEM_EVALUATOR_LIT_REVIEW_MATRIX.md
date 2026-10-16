<!-- lingua: la -->
# Tabula comparativa studiorum et instrumentorum ad aestimationem STEM

Haec tabula rationem localem, quae congruentiam cum disciplinis STEM, citationes et fasciculos scientificos aestimat, cum instrumentis academicis similibus comparat.

## Ambitus

Instrumentum locale neque indices bibliographicos neque recognitionem collegarum neque detectionem plagii neque bases datorum integritatis scientificae substituere vult. Munus angustius est: rationem examinabilem, reproducibilem et ad exportationem publicam tutam praebere, qua curricula vitae STEM publica et scripta submissa primum inspiciantur.

## Tabula comparativa

| Systema vel fons | Munus praecipuum | Similitudo | Lacuna aut cautio | Munus coniunctionis |
|---|---|---|---|---|
| Crossref REST API | Metadata DOI, inscriptiones bibliographicae et accessus JSON REST | Convenit ad DOI et metadata citationum verificanda | Qualitas pendet ex rebus depositis; identitas auctoris nec omnia contexta citationum semper solvuntur | Primarium instrumentum DOI |
| OpenAlex | Rete operum, auctorum, institutionum, numerorum citationum, h-index et i10-index | Convenit ad indicia publicationum auctoris | Disambiguatio auctorum interdum incerta est; recognitione humana eget | Fons signorum publicationis auctoris |
| Semantic Scholar Graph API | Rete scriptorum et auctorum cum metricis citationum | Fons proximus ad amplificandas res bibliographicas | Limites API et campi propriam coniunctionem requirunt; nondum institutum est | Instrumentum alterum futurum |
| PubMed / NCBI E-utilities | Identificatores et metadata biomedica cum PMID et PMCID | Convenit ad scripta biomedica verificanda | Praecipue biomedicinae et scientiis vitae, non omnibus STEM, inservit | Verificatio PMID |
| OpenCitations / COCI | Rete citationum DOI ad DOI et metadata aperta | Convenit ad relationes citationum apertas examinandas | Comprehensio pendet ex fontibus apertis et identificatoribus | Fons futurus citationum apertarum |
| Systemata contextus citationum similia scite | Distinguunt citationes sustinentes, contradicentes vel memorantes | Affinia aestimationi qualitatis relationum citationum | Saepe proprietaria; ratio localis sensum citationum nondum classificat | Modulus facultativus futurus |
| Signa integritatis similia Retraction Watch / Crossmark | Status retractationis, correctionis et renovationis | Auxilium ad scripta retractata vel correcta indicanda | Interpretationem prudentem et API proprias requirit | Custodia futura integritatis |
| Evaluator localis STEM CV Curator | Mensura STEM sine nexu, extractio citationum, verificatio facultativa, nota composita | Ratio perspicua et deterministica | Recognitionem collegarum non substituit; identitas auctoris et numeri citationum examinandi sunt | Custodia testimoniorum CV et scriptorum |

## Instrumenta et status

| Facultas | Status hodiernus | Instrumentum | Renovatio sequens |
|---|---|---|---|
| Aestimatio textus STEM | Instituta | `scripts/stem_presence.py` | Vocabularia disciplinarum configurabilia |
| Tabula STEM indicis operum | Instituta | `scripts/write_stem_presence_report.py` | Historia mutationum inter exsecutiones |
| Extractio DOI | Instituta | `scripts/stem_citation_verifier.py` | Probationes normalizationis signorum DOI |
| Metadata DOI externa | Instituta, facultativa | Crossref | Diem interrogationis et finem fontis in effectu servare |
| Extractio PMID | Instituta | `scripts/stem_citation_verifier.py` | Amplificatio metadata NCBI |
| Extractio arXiv | Instituta | `scripts/stem_citation_verifier.py` | Amplificatio metadata arXiv |
| Extractio URL et responsio finis | Instituta, facultativa | Interrogatio finis publici | Regulae permissionis et vetiti URL |
| Numerus citationum auctoris | Instituta, facultativa | OpenAlex | Monita de identitate incerta et candidatis |
| Numerus operum | Instituta, facultativa | OpenAlex | Campus fiduciae fontis |
| h-index / i10-index | Instituta, facultativa | OpenAlex | Textus de origine metrica |
| Nota composita scripti | Instituta | `scripts/stem_paper_evaluator.py` | Probatio schematis JSON |
| Classificatio contextus citationum | Nondum instituta | N/A | Heuristica localis facultativa vel coniunctor alterius fontis |
| Status retractationis/correctionis | Nondum institutus | N/A | Nexus ad Crossmark vel Retraction Watch |
| Reconciliatio citationum inter fontes | Nondum instituta | N/A | Comparatio OpenAlex, Crossref et Semantic Scholar |

## Consequentiae consilii

Instrumentum localiter et sine nexu externo operari debet in CI et generationibus CV publicis. Verificatio externa tantum expresse petatur, quoniam servitia citationum numerum interrogationum restringere, responsa mutare aut plures auctores similes indicare possunt.

Proxima emendanda sunt indicia originis fontium, monita de identitate auctoris incerta et probatio structurae JSON pro effectu composito aestimatoris.

## Fontes et nexus servati

- Documenta Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Documenta de auctoribus OpenAlex: https://developers.openalex.org/api-reference/authors
- Documenta Semantic Scholar Graph API: https://api.semanticscholar.org/api-docs/graph
- Documenta NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- Scriptum OpenCitations COCI: https://arxiv.org/abs/1904.06052
- Scriptum de indice OpenCitations: https://arxiv.org/abs/2408.02321
