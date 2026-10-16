#!/usr/bin/env python3
"""Probationes unitatis pro custodia linguae Latinae."""
from __future__ import annotations

import unittest

from check_latin_safeguards import MARK, audit, is_pointer_only, suspicious_english_lines


class LatinSafeguardTests(unittest.TestCase):
    def test_pure_upstream_feeder_is_exempt(self) -> None:
        source = "# Fontes\n\n[Fons](https://example.org/study)\n- https://example.org/other\n"
        self.assertTrue(is_pointer_only(source))
        self.assertEqual(audit("docs/upstream_references.md", source)[0], "feeder")

    def test_mixed_pointer_and_commentary_is_not_feeder(self) -> None:
        source = "# Relatio\n[Fons](https://example.org/study)\nHaec verba ab auctore scripta sunt.\n"
        self.assertFalse(is_pointer_only(source))
        self.assertEqual(audit("docs/author_commentary.md", source)[0], "violation")

    def test_verified_latin_marked_document_passes(self) -> None:
        source = MARK + "\n# Investigatio\n\nHaec relatio fontes publicos et methodos in codice enumerat.\n"
        self.assertEqual(audit("docs/research_note.md", source), ("compliant", []))

    def test_marker_does_not_hide_english_prose(self) -> None:
        source = MARK + "\n# Note\n\nThis document presents the report and explains how the project is reviewed.\n"
        status, lines = audit("docs/fake_latin.md", source)
        self.assertEqual(status, "violation")
        self.assertEqual(lines, [4])

    def test_literal_source_quotation_and_code_fence_are_preserved(self) -> None:
        source = (
            MARK + "\n# Testimonia\n"
            "> This document presents the report and explains how the project is reviewed.\n"
            + chr(96) * 3 + "text\n"
            "This document presents the report and explains how the project is reviewed.\n"
            + chr(96) * 3 + "\n"
            "Quod scriptum e fonte integro servatur.\n"
        )
        self.assertEqual(suspicious_english_lines(source), [])

    def test_legacy_document_is_reported_not_approved(self) -> None:
        status, lines = audit("research/RESEARCH_STATUS.md", "# Status investigationum generatus\n")
        self.assertEqual((status, lines), ("pending", []))

    def test_root_readme_only_is_exempt(self) -> None:
        self.assertEqual(audit("README.md", "Public-facing orientation")[0], "exempt")
        self.assertEqual(audit("docs/README.md", "Public-facing orientation")[0], "violation")

    def test_source_ledger_is_feeder(self) -> None:
        self.assertEqual(audit("research/living_source_ledger.md", "Generated source ledger")[0], "feeder")


if __name__ == "__main__":
    unittest.main()
