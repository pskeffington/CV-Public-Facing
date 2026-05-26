#!/usr/bin/env python3
"""Validate the generated STEM presence Markdown report."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "research" / "stem_presence_report.md"
OBJECTS_PATH = ROOT / "data" / "stem_cv_objects.json"


@dataclass(frozen=True)
class ReportContractResult:
    passed: bool
    errors: list[str]
    project_rows: int
    expected_projects: int

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "project_rows": self.project_rows,
            "expected_projects": self.expected_projects,
        }


class StemPresenceReportChecker:
    """Contract checker for the generated STEM presence report."""

    REQUIRED_SECTIONS = [
        "# STEM Presence Report",
        "## Portfolio summary",
        "## Band counts",
        "## Project scores",
    ]

    REQUIRED_TABLE_HEADER = "| Project | Repository | Section | Maturity | STEM score | Drift score | Band | Rationale |"

    def __init__(self, report_path: Path = REPORT_PATH, objects_path: Path = OBJECTS_PATH) -> None:
        self.report_path = report_path
        self.objects_path = objects_path

    def run(self) -> ReportContractResult:
        errors: list[str] = []
        text = self._read_report(errors)
        expected_projects = self._expected_project_count(errors)
        if text:
            self._check_sections(text, errors)
            self._check_summary(text, errors)
        project_rows = self._count_project_rows(text)
        if expected_projects and project_rows != expected_projects:
            errors.append(f"Expected {expected_projects} project score rows, found {project_rows}")
        return ReportContractResult(not errors, errors, project_rows, expected_projects)

    def _read_report(self, errors: list[str]) -> str:
        if not self.report_path.exists():
            errors.append(f"Missing STEM presence report: {self.report_path}")
            return ""
        text = self.report_path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append("STEM presence report is empty")
        return text

    def _expected_project_count(self, errors: list[str]) -> int:
        if not self.objects_path.exists():
            errors.append(f"Missing object JSON: {self.objects_path}")
            return 0
        payload = json.loads(self.objects_path.read_text(encoding="utf-8"))
        projects = payload.get("projects", [])
        if not isinstance(projects, list):
            errors.append("Object JSON projects field is not a list")
            return 0
        return len(projects)

    def _check_sections(self, text: str, errors: list[str]) -> None:
        for section in self.REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"Missing report section: {section}")
        if self.REQUIRED_TABLE_HEADER not in text:
            errors.append("Missing project score table header")

    def _check_summary(self, text: str, errors: list[str]) -> None:
        for label in ["Project count", "Average STEM presence score", "Average drift score"]:
            if label not in text:
                errors.append(f"Missing summary label: {label}")
        if not re.search(r"- `[^`]+`: \d+", text):
            errors.append("Missing band count entries")

    @staticmethod
    def _count_project_rows(text: str) -> int:
        count = 0
        for line in text.splitlines():
            if line.startswith("| ") and " | `" in line and " |" in line:
                if not line.startswith("| Project ") and not line.startswith("|---"):
                    count += 1
        return count


def main() -> int:
    result = StemPresenceReportChecker().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
