#!/usr/bin/env python3
"""Offline parser checks for PubMed and arXiv metadata enrichment."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_citation_verifier import CitationVerifier  # noqa: E402


@dataclass(frozen=True)
class ReferenceMetadataParserCheckResult:
    passed: bool
    errors: list[str]
    pubmed_title: str | None
    arxiv_title: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "pubmed_title": self.pubmed_title,
            "arxiv_title": self.arxiv_title,
        }


class ReferenceMetadataParserCheck:
    PUBMED_FIXTURE = {
        "result": {
            "23803847": {
                "title": "Example public health article.",
                "fulljournalname": "Example Journal of Public Health",
                "source": "Ex J Public Health",
                "pubdate": "2013 Jul",
                "authors": [
                    {"name": "Smith J"},
                    {"name": "Doe A"},
                ],
                "articleids": [
                    {"idtype": "doi", "value": "10.1000/example"},
                    {"idtype": "pmc", "value": "PMC123456"},
                ],
                "pubtype": ["Journal Article"],
            }
        }
    }

    ARXIV_FIXTURE = """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:arxiv='http://arxiv.org/schemas/atom'>
  <entry>
    <id>http://arxiv.org/abs/2101.00001v1</id>
    <updated>2021-01-02T00:00:00Z</updated>
    <published>2021-01-01T00:00:00Z</published>
    <title> Example arXiv machine learning paper </title>
    <summary> This paper reports a reproducible method and validation metrics. </summary>
    <author><name>Researcher A</name></author>
    <author><name>Researcher B</name></author>
    <arxiv:doi>10.1000/arxiv.example</arxiv:doi>
    <arxiv:journal_ref>Example Journal 1 (2021)</arxiv:journal_ref>
    <category term='cs.LG' />
    <category term='stat.ML' />
  </entry>
</feed>
"""

    def run(self) -> ReferenceMetadataParserCheckResult:
        errors: list[str] = []
        pubmed = CitationVerifier._pubmed_metadata("23803847", self.PUBMED_FIXTURE)
        arxiv = CitationVerifier._arxiv_metadata("2101.00001v1", self.ARXIV_FIXTURE)

        if not isinstance(pubmed, dict):
            errors.append("PubMed parser did not return metadata")
            pubmed = {}
        if not isinstance(arxiv, dict):
            errors.append("arXiv parser did not return metadata")
            arxiv = {}

        self._expect(pubmed, "title", "Example public health article.", errors)
        self._expect(pubmed, "journal", "Example Journal of Public Health", errors)
        self._expect(pubmed, "publication_year", 2013, errors)
        self._expect(pubmed, "doi", "10.1000/example", errors)
        self._expect(pubmed, "pmcid", "PMC123456", errors)
        if pubmed.get("authors") != ["Smith J", "Doe A"]:
            errors.append("PubMed authors were not parsed as expected")

        self._expect(arxiv, "arxiv_id", "2101.00001v1", errors)
        self._expect(arxiv, "canonical_arxiv_id", "2101.00001", errors)
        self._expect(arxiv, "title", "Example arXiv machine learning paper", errors)
        self._expect(arxiv, "primary_category", "cs.LG", errors)
        self._expect(arxiv, "doi", "10.1000/arxiv.example", errors)
        self._expect(arxiv, "journal_ref", "Example Journal 1 (2021)", errors)
        if arxiv.get("authors") != ["Researcher A", "Researcher B"]:
            errors.append("arXiv authors were not parsed as expected")
        if arxiv.get("categories") != ["cs.LG", "stat.ML"]:
            errors.append("arXiv categories were not parsed as expected")

        return ReferenceMetadataParserCheckResult(
            passed=not errors,
            errors=errors,
            pubmed_title=pubmed.get("title") if isinstance(pubmed.get("title"), str) else None,
            arxiv_title=arxiv.get("title") if isinstance(arxiv.get("title"), str) else None,
        )

    @staticmethod
    def _expect(payload: dict[str, object], key: str, expected: object, errors: list[str]) -> None:
        if payload.get(key) != expected:
            errors.append(f"Expected {key}={expected!r}, found {payload.get(key)!r}")


def main() -> int:
    result = ReferenceMetadataParserCheck().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
