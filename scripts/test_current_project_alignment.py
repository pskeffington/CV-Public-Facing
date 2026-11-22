#!/usr/bin/env python3
"""Regression checks for historical notes and stale current project surfaces."""

import json
import tempfile
import unittest
from pathlib import Path

from check_current_project_alignment import SURFACES, check


class CurrentProjectAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("data", "cv", "research"):
            (self.root / directory).mkdir()
        self.manifest = {
            "generated_on_note": "CART-TRACE retired; historical evidence retained.",
            "repos": [{"key": "arch", "repo": "example/arch_notebook", "title": "Arch Notebook"}],
        }
        self.write_manifest()
        for name, (prefix, suffix) in SURFACES.items():
            (self.root / name).write_text(prefix + "Arch Notebook" + suffix + "\n", encoding="utf-8")
        (self.root / "cv/one_page_profile_public.tex").write_text("Arch Notebook", encoding="utf-8")

    def write_manifest(self):
        (self.root / "data/pipeline_repos.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_historical_note_is_allowed(self):
        self.assertEqual(check(self.root), [])

    def test_retired_identity_fields_fail(self):
        for key in ("key", "repo", "title"):
            with self.subTest(key=key):
                original = self.manifest["repos"][0][key]
                self.manifest["repos"][0][key] = "CART-TRACE"
                self.write_manifest()
                self.assertTrue(check(self.root))
                self.manifest["repos"][0][key] = original

    def test_malformed_records_fail_closed(self):
        for record in (None, "legacy", {}, {"key": "arch", "repo": [], "title": "Arch Notebook"}):
            with self.subTest(record=record):
                self.manifest["repos"] = [record]
                self.write_manifest()
                self.assertTrue(check(self.root))

    def test_empty_or_invalid_manifest_fails(self):
        for manifest in ({}, [], {"repos": []}, {"repos": {}}):
            with self.subTest(manifest=manifest):
                self.manifest = manifest
                self.write_manifest()
                self.assertTrue(check(self.root))

    def test_stale_or_missing_generated_selection_fails(self):
        for name in SURFACES:
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_text(encoding="utf-8")
                path.write_text(original.replace("Arch Notebook", "CART-TRACE"), encoding="utf-8")
                self.assertTrue(check(self.root))
                path.unlink()
                self.assertTrue(check(self.root))
                path.write_text(original, encoding="utf-8")

    def test_extra_or_duplicate_selection_fails(self):
        for name, (prefix, suffix) in SURFACES.items():
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_text(encoding="utf-8")
                path.write_text(original + prefix + "Unapproved project" + suffix, encoding="utf-8")
                self.assertTrue(check(self.root))
                path.write_text(original * 2, encoding="utf-8")
                self.assertTrue(check(self.root))
                path.write_text(original, encoding="utf-8")

    def test_nonpublic_record_fails(self):
        self.manifest["repos"][0]["public_release"] = "blocked"
        self.write_manifest()
        self.assertTrue(check(self.root))

    def test_retired_profile_fails(self):
        (self.root / "cv/one_page_profile_public.tex").write_text("CART-TRACE", encoding="utf-8")
        self.assertTrue(check(self.root))


if __name__ == "__main__":
    unittest.main()
