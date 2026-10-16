#!/usr/bin/env python3
"""Probationes custodiae ambitus repositorii publici."""

from __future__ import annotations

import unittest

from check_repository_scope import check_paths


class PublicRepositoryScopeTests(unittest.TestCase):
    def test_current_public_source_layout_is_allowed(self) -> None:
        self.assertEqual(
            check_paths([
                "README.md",
                "Dartmouth_CV.md",
                "cv/academic_cv_public.tex",
                "data/pipeline_repos.json",
                "docs/REGIMEN_RAMORUM.md",
                "hire/FOR_HIRE_LATIN.md",
                "research/RESEARCH_STATUS.md",
                "scripts/check_repository_scope.py",
                "documents/.gitkeep",
                ".github/workflows/build-public-research-status.yml",
            ]),
            [],
        )

    def test_private_job_application_is_not_public_scope(self) -> None:
        findings = check_paths(["applications/plymouth_human_services/resume.md"])
        self.assertEqual(len(findings), 1)
        self.assertIn("directorium", findings[0])

    def test_generated_documents_are_release_assets(self) -> None:
        findings = check_paths([
            "documents/CV.pdf",
            "cv/academic_cv_public.pdf",
            "research/research_status.pdf",
        ])
        self.assertEqual(len(findings), 3)

    def test_unreviewed_root_file_is_not_implicitly_public(self) -> None:
        self.assertEqual(len(check_paths(["job_packet.md"])), 1)

    def test_path_escape_is_forbidden(self) -> None:
        self.assertEqual(len(check_paths(["docs/../../secret.md"])), 1)


if __name__ == "__main__":
    unittest.main()
