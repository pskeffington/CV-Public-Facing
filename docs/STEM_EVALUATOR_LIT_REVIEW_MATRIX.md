# STEM Evaluator Literature and Tooling Matrix

This matrix compares the package's STEM drift, citation-verification, and paper-package evaluation layer with adjacent scholarly infrastructure.

## Scope

The local package is not trying to replace bibliographic indexes, peer review, plagiarism detection, or research-integrity databases. Its role is narrower: provide a clone-safe, auditable triage object for public-facing STEM CV and submitted-paper review.

## Comparison matrix

| System / source | Core function | Similarity to this package | Gap / caution | Best integration role |
|---|---|---|---|---|
| Crossref REST API | DOI metadata lookup, bibliographic records, member-deposited metadata, JSON REST access | Strong match for DOI verification and reference-level metadata | Metadata quality depends on deposits; not all citation contexts or author identities are resolved | Primary DOI verification layer |
| OpenAlex | Open scholarly graph with works, authors, institutions, cited-by counts, works counts, h-index, i10-index | Strong match for submitter-level citation and author footprint scoring | Author disambiguation can be imperfect; matches need review | Author publishing-signal provider |
| Semantic Scholar Graph API | Paper and author graph fields including citation and influential-citation style metrics | Strong adjacent source for paper/author graph enrichment | API limits and field choices require explicit integration; not currently implemented | Future secondary verifier / cross-check |
| PubMed / NCBI E-utilities | Biomedical identifier and metadata access for PMID/PMCID-linked literature | Strong match for biomedical paper verification | Scope is biomedical/life-science biased; not general STEM | PMID verification and biomedical-specific evidence |
| OpenCitations / COCI | Open DOI-to-DOI citation graph and open citation metadata | Strong match for open citation graph checks | Coverage varies by open-reference availability and identifiers | Future open-citation graph provider |
| scite-style citation context systems | Citation-context classification, e.g., supporting, contrasting, mentioning | Conceptually similar to drift-quality review because citation context matters | Often commercial/proprietary; local package currently does not classify citation sentiment/context | Future optional citation-context module |
| Retraction Watch / Crossmark-style integrity signals | Retraction/correction/update status and post-publication integrity context | Complements STEM drift review by flagging compromised or corrected literature | Requires careful source-specific APIs and interpretation | Future retraction/integrity guardrail |
| Local STEM CV Curator evaluator | Offline-first STEM presence, citation extraction, optional live reference/author signals, composite score | Transparent, deterministic, clone-safe triage workflow | Not a peer-review substitute; author identity and citation counts must be reviewed | Package-level paper and CV evidence gate |

## Functional coverage

| Capability | Current package status | Current implementation | Next polish target |
|---|---|---|---|
| STEM surface scoring | Implemented | `scripts/stem_presence.py` | Add configurable domain vocabularies by field |
| Portfolio STEM dashboard | Implemented | `scripts/write_stem_presence_report.py` | Add trend history over generated runs |
| DOI extraction | Implemented | `scripts/stem_citation_verifier.py` | Add DOI normalization tests for edge punctuation |
| DOI live metadata check | Implemented, optional | Crossref live mode | Store source timestamp and endpoint in output |
| PMID extraction | Implemented | `scripts/stem_citation_verifier.py` | Add NCBI E-utilities metadata enrichment |
| arXiv extraction | Implemented | `scripts/stem_citation_verifier.py` | Add arXiv API metadata enrichment |
| URL extraction and reachability | Implemented, optional | live endpoint ping | Add allowlist/denylist controls for private review |
| Author cited-by count | Implemented, optional | OpenAlex live mode | Add ambiguity warnings and candidate list |
| Works count | Implemented, optional | OpenAlex live mode | Add source confidence field |
| h-index / i10-index | Implemented, optional | OpenAlex live mode | Add metric provenance text in output |
| Composite paper-package score | Implemented | `scripts/stem_paper_evaluator.py` | Add JSON schema contract for evaluator output |
| Citation context classification | Not implemented | N/A | Add optional scite-like local heuristic or provider adapter |
| Retraction/correction status | Not implemented | N/A | Add Crossmark/Retraction Watch-compatible signal layer |
| Multi-source citation reconciliation | Not implemented | N/A | Add OpenAlex + Crossref + Semantic Scholar comparison mode |

## Design implications

The package should remain offline-first for CI and public-safe CV builds. Live checks should remain explicit because citation APIs can rate-limit, change responses, or return ambiguous author matches.

The next useful refinements are source provenance fields, ambiguity warnings for author lookup, and a JSON contract check for the composite paper evaluator output.

## Source notes

- Crossref REST API documentation: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- OpenAlex author object documentation: https://developers.openalex.org/api-reference/authors
- Semantic Scholar Graph API documentation: https://api.semanticscholar.org/api-docs/graph
- NCBI E-utilities documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- OpenCitations COCI paper: https://arxiv.org/abs/1904.06052
- OpenCitations Index paper: https://arxiv.org/abs/2408.02321
