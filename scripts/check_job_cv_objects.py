#!/usr/bin/env python3
"""Validate public-safe job CV objects and workflow dropdown choices."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "job_cv_objects.json"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "build-public-research-status.yml"
REQUIRED_FIELDS = {
    "label",
    "output_slug",
    "role_family",
    "profile_emphasis",
    "public_safe_focus",
    "tailoring_notes",
    "exclusions",
}


class CheckError(Exception):
    """Raised when the public-safe job object contract fails."""


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise CheckError(f"missing registry: {REGISTRY_PATH.relative_to(ROOT)}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def read_workflow_options() -> list[str]:
    if not WORKFLOW_PATH.exists():
        raise CheckError(f"missing workflow: {WORKFLOW_PATH.relative_to(ROOT)}")

    lines = WORKFLOW_PATH.read_text(encoding="utf-8").splitlines()
    options: list[str] = []
    inside_options = False
    for line in lines:
        stripped = line.strip()
        if stripped == "options:":
            inside_options = True
            continue
        if inside_options:
            if stripped.startswith("-"):
                options.append(stripped[1:].strip().strip('"').strip("'"))
                continue
            if stripped and not line.startswith("          "):
                break
    return options


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    objects = registry.get("job_objects")
    if not isinstance(objects, dict) or not objects:
        return ["registry has no job_objects map"]

    default = registry.get("default_job_object")
    if default not in objects:
        errors.append("default_job_object is missing from job_objects")

    for object_id, obj in objects.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", object_id):
            errors.append(f"invalid object id: {object_id}")
        if not isinstance(obj, dict):
            errors.append(f"job object is not a map: {object_id}")
            continue
        missing = sorted(REQUIRED_FIELDS - obj.keys())
        if missing:
            errors.append(f"{object_id} missing fields: {', '.join(missing)}")
        for list_field in ("public_safe_focus", "exclusions"):
            if not isinstance(obj.get(list_field), list) or not obj.get(list_field):
                errors.append(f"{object_id} requires non-empty list field: {list_field}")
        slug = obj.get("output_slug")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9_]+", slug):
            errors.append(f"{object_id} output_slug must be lowercase snake-style text")
    return errors


def validate_workflow_options(registry: dict[str, Any], options: list[str]) -> list[str]:
    errors: list[str] = []
    object_ids = set(registry.get("job_objects", {}).keys())
    option_ids = set(options)
    if not options:
        errors.append("workflow has no job_object dropdown options")
    missing_from_workflow = sorted(object_ids - option_ids)
    missing_from_registry = sorted(option_ids - object_ids)
    if missing_from_workflow:
        errors.append("registry objects missing from workflow dropdown: " + ", ".join(missing_from_workflow))
    if missing_from_registry:
        errors.append("workflow dropdown values missing from registry: " + ", ".join(missing_from_registry))
    if options and options[0] != registry.get("default_job_object"):
        errors.append("first workflow option should match default_job_object")
    return errors


def main() -> int:
    registry = load_registry()
    options = read_workflow_options()
    errors = validate_registry(registry) + validate_workflow_options(registry, options)
    if errors:
        print("job CV object check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2
    print(f"job CV object check passed: {len(options)} workflow options validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
