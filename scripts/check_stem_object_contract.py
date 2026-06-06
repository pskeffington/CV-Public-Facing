#!/usr/bin/env python3
"""Contract checks for generated STEM CV object JSON."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OBJECTS_PATH = ROOT / "data" / "stem_cv_objects.json"


@dataclass(frozen=True)
class ObjectContractResult:
    """Result object for generated-object contract validation."""

    passed: bool
    errors: list[str]
    project_count: int
    schema: str
    blocked_release_records: int

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "project_count": self.project_count,
            "schema": self.schema,
            "blocked_release_records": self.blocked_release_records,
        }


class StemObjectContractChecker:
    """Validate generated objects, release controls, and STEM presence metrics."""

    REQUIRED_SCORE_KEYS = {
        "score",
        "drift_score",
        "band",
        "rationale",
        "matched_domain_terms",
        "matched_method_terms",
        "matched_reproducibility_terms",
        "matched_progress_terms",
        "matched_drift_terms",
    }

    VALID_BANDS = {
        "core_stem",
        "stem_adjacent",
        "mixed_or_transitional",
        "low_stem_presence",
    }

    VALID_SCHEMAS = {
        "stem-cv-curator/v0.2",
        "stem-cv-curator/v0.3",
    }

    def __init__(self, objects_path: Path = OBJECTS_PATH) -> None:
        self.objects_path = objects_path

    def run(self) -> ObjectContractResult:
        errors: list[str] = []
        if not self.objects_path.exists():
            return ObjectContractResult(False, [f"Missing generated object file: {self.objects_path}"], 0, "", 0)

        payload = self._load_payload(errors)
        if payload is None:
            return ObjectContractResult(False, errors, 0, "", 0)

        schema = str(payload.get("schema", ""))
        if schema not in self.VALID_SCHEMAS:
            errors.append(f"Expected schema in {sorted(self.VALID_SCHEMAS)}, found {schema or '<missing>'}")

        projects = payload.get("projects", [])
        if not isinstance(projects, list):
            errors.append("Top-level projects field is not a list")
            projects = []
        if not projects:
            errors.append("Generated object file contains no projects")

        blocked_records = payload.get("blocked_release_records", [])
        if schema == "stem-cv-curator/v0.3" and not isinstance(blocked_records, list):
            errors.append("blocked_release_records field is not a list")
            blocked_records = []

        for index, project in enumerate(projects):
            self._check_project(index, project, errors)

        blocked_count = len(blocked_records) if isinstance(blocked_records, list) else 0
        return ObjectContractResult(not errors, errors, len(projects), schema, blocked_count)

    def _load_payload(self, errors: list[str]) -> dict[str, Any] | None:
        try:
            loaded = json.loads(self.objects_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {self.objects_path}: {exc}")
            return None
        if not isinstance(loaded, dict):
            errors.append("Generated object file root is not a JSON object")
            return None
        return loaded

    def _check_project(self, index: int, project: Any, errors: list[str]) -> None:
        if not isinstance(project, dict):
            errors.append(f"Project {index} is not an object")
            return

        project_id = str(project.get("project_id", f"index-{index}"))
        release = str(project.get("public_release", "public")).lower()
        if release != "public":
            errors.append(f"Project {project_id} has non-public release state inside public projects: {release}")

        stem_presence = project.get("stem_presence")
        if not isinstance(stem_presence, dict):
            errors.append(f"Project {project_id} is missing stem_presence object")
            return

        missing = sorted(self.REQUIRED_SCORE_KEYS - stem_presence.keys())
        if missing:
            errors.append(f"Project {project_id} stem_presence missing keys: {', '.join(missing)}")

        score = stem_presence.get("score")
        drift_score = stem_presence.get("drift_score")
        band = stem_presence.get("band")

        if not isinstance(score, int) or not 0 <= score <= 100:
            errors.append(f"Project {project_id} has invalid score: {score}")
        if not isinstance(drift_score, int) or not 0 <= drift_score <= 100:
            errors.append(f"Project {project_id} has invalid drift_score: {drift_score}")
        if isinstance(score, int) and isinstance(drift_score, int) and score + drift_score != 100:
            errors.append(f"Project {project_id} score and drift_score do not sum to 100")
        if band not in self.VALID_BANDS:
            errors.append(f"Project {project_id} has invalid band: {band}")


def main() -> int:
    result = StemObjectContractChecker().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
