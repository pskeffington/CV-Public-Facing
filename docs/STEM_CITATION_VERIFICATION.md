<!-- lingua: la -->
# Verificatio citationum STEM

Instrumentum verificationis citationum STEM probationes integritatis fontium et signa publicationis scientificae rationi STEM addit.

Duas quaestiones distinctas examinat:

1. Utrum scriptum vel documentum operis submissum identificatores citationum verificabiles habeat.
2. Utrum auctor scriptorum vestigia publicationis et citationum extra hunc fasciculum observabilia habeat.

Instrumentum consulto cautum est. Ratio sine nexu externo identificatores extrahit et notas tantum ex ipsis identificatoribus computat. Ratio cum nexu externo expresse petitur atque fontes academicos publicos adit.

## Instrumentum

```text
scripts/stem_citation_verifier.py
```

## Extractio citationum

| Genus | Exemplum |
|---|---|
| DOI | `10.1038/nature12373` |
| arXiv | `arXiv:2101.00001` |
| PMID | `PMID: 23803847` |
| URL | `https://example.org/reproducibility-manifest` |

## Ratio sine nexu externo

```bash
python3 scripts/stem_citation_verifier.py --pretty paper.md
cat paper.txt | python3 scripts/stem_citation_verifier.py --pretty
```

Haec ratio citationes inventas et notas cautas de signis publicationis reddit, sed fontes non quasi directe verificatos notat.

## Ratio cum nexu externo

```bash
python3 scripts/stem_citation_verifier.py --pretty --live paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --author "Jane Researcher" paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --orcid "0000-0000-0000-0000" paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --author "Jane Researcher" --max-author-candidates 5 paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --allow-url-host example.org paper.md
python3 scripts/stem_citation_verifier.py --pretty --live --block-url-host private.example paper.md
```

Fontes publici exquiri possunt:

| Signum | Fons |
|---|---|
| Metadata DOI et numerus citationum | Crossref |
| Metadata PMID | NCBI PubMed ESummary |
| Metadata arXiv | arXiv API Atom |
| Responsio inscriptionis URL | Admissio ad finem publicum, secundum regulas URL |
| Vestigia publicationum auctoris | OpenAlex |

## Custodia inscriptionum URL

Probatio inscriptionum URL separatim coerceri potest, dum examina DOI, PMID, arXiv et OpenAlex servantur:

```bash
python3 scripts/stem_citation_verifier.py --live --allow-url-host example.org paper.md
python3 scripts/stem_citation_verifier.py --live --block-url-host private.example paper.md
```

`--allow-url-host` probationes directas ad dominia enumerata eorumque subdominia restringit. `--block-url-host` interrogationes ad illa dominia prohibet. Utraque optio iterari potest; cum ambae ponuntur, vetitum praevalet. Citationes URL a regula prohibitae in effectu manent, sed `verified: false`, `verification_mode: live_policy_blocked` et signum `url_policy_blocked` accipiunt.

## Origo cuiusque citationis

Quaeque citatio extracta haec indicia inspectionis servat:

```json
{
  "source": "identifier_extractor",
  "endpoint": null,
  "checked_at": "2026-05-26T00:00:00Z",
  "verification_mode": "offline",
  "metadata": null
}
```

Pro DOI cum nexu externo `source: crossref` atque finis Crossref servantur. Pro PMID `source: ncbi_pubmed_esummary` et finis NCBI ESummary servantur, et `metadata` implentur si index PubMed repertus est. Pro arXiv `source: arxiv_api` et finis arXiv servantur, atque `metadata` ex fonte impleri possunt. In ratione sine nexu dies `checked_at` manet, sed `endpoint` et `metadata` sunt `null`, et `verification_mode` est `offline`.

## Metadata PubMed

Examinatio PMID cum nexu haec addere potest:

```json
{
  "pmid": "23803847",
  "title": "...",
  "journal": "...",
  "publication_date": "2013 Jul",
  "publication_year": 2013,
  "authors": ["Author A", "Author B"],
  "doi": "10.xxxx/example",
  "pmcid": "PMC...",
  "publication_types": ["Journal Article"]
}
```

Haec amplificatio nexum externum et responsa NCBI ESummary requirit.

## Metadata arXiv

Examinatio arXiv cum nexu haec addere potest:

```json
{
  "arxiv_id": "2101.00001v1",
  "canonical_arxiv_id": "2101.00001",
  "title": "...",
  "abstract": "...",
  "authors": ["Author A", "Author B"],
  "categories": ["cs.LG"],
  "primary_category": "cs.LG",
  "published": "2021-01-01T00:00:00Z",
  "updated": "2021-01-02T00:00:00Z",
  "doi": null,
  "journal_ref": null
}
```

Haec amplificatio responsa arXiv API Atom requirit.

## Index citationum auctoris

Si `--author` vel `--orcid` adhibetur, ratio cum nexu haec referre conatur:

```json
{
  "matched_name": "Jane Researcher",
  "author_id": "https://openalex.org/A...",
  "source": "openalex",
  "verified": true,
  "cited_by_count": 250,
  "works_count": 12,
  "h_index": 8,
  "i10_index": 6,
  "author_signal_score": 70,
  "candidate_count": 1,
  "candidates": [],
  "ambiguity_warning": null,
  "author_match_confidence": "name_single_candidate"
}
```

Haec nota indicium publicationis tantum est; neque veritatem scientificam neque validitatem scripti neque identitatem auctoris confirmat sine recognitione convenientiae.

## Classes signorum publicationis

| Classis | Interpretatio |
|---|---|
| `strong_publishing_signal` | Identifier academicus verificatus vel argumenta citationum multa |
| `moderate_publishing_signal` | Identifier verificabilis vel signa citationum mediocria |
| `weak_or_unverified_signal` | Identifier repertus, sed verificatio externa deest aut tenuis est |
| `low_publishing_signal` | Pauca testimonia citationum |

## Probatio localis

```bash
make citation-check
```

Probatio sine nexu externo tuto currit. Extractionem DOI, arXiv, PMID et URL, conservationem originis et camporum metadata, regulas admissionis URL et statum explicitum `unverified` indiciorum auctoris examinat.

## Coniunctio cum aestimatione STEM

Verificatio citationum mensuram praesentiae STEM complet. Nota alta praesentiae STEM significat scriptum signa methodorum, datorum, validationis, reproductionis et progressus exhibere. Verificatio citationum addit testimonia de fontibus et de signis publicationis quae extra scriptum examinari possunt.
