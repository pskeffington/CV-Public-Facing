#!/usr/bin/env python3
"""Validate the public CV allowlist manifest contract."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "pipeline_repos.json"

VALID_RELEASE_STATES = {"public", "blocked", "deny", "private", "restricted", "internal_only"}
PUBLIC_REQUIRED_FIELDS = {
    "key",
    "repo",
    "title",
    "status",
    "summary",
    "needs",
    "cv_section",
    "source_files",
}
HASH_PATTERN = re.compile(r"^[a-f0-9]{64}$")
KEY_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class ManifestCheckResult:
    passed: bool
    errors: list[str]
    public_entries: int
    blocked_hashes: int
    recursive_intake: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "public_entries": self.public_entries,
            "blocked_hashes": self.blocked_hashes,
            "recursive_intake": self.recursive_intake,
        }


class PublicManifestContractChecker:
    """Checks public allowlist shape before generated outputs are built."""

    def __init__(self, manifest_path: Path = MANIFEST_PATH) -> None:
        self.manifest_path = manifest_path

    def run(self) -> ManifestCheckResult:
        errors: list[str] = []
        payload = self._load_payload(errors)
        if payload is None:
            return ManifestCheckResult(False, errors, 0, 0, False)

        scan = payload.get("scan", {})
        if not isinstance(scan, dict):
            errors.append("scan field must be an object")
            scan = {}

        recursive = bool(scan.get("allow_recursive_intake", False))
        if recursive and not bool(scan.get("recursive_intake_reviewed", False)):
            errors.append("allow_recursive_intake requires recursive_intake_reviewed=true")

        if bool(scan.get("include_private_repos", False)):
            errors.append("include_private_repos must remain false in the public renderer")

        blocked_hashes = scan.get("blocked_repo_hashes", [])
        if not isinstance(blocked_hashes, list):
            errors.append("blocked_repo_hashes must be a list")
            blocked_hashes = []
        for digest in blocked_hashes:
            if not isinstance(digest, str) or not HASH_PATTERN.fullmatch(digest):
                errors.append("blocked_repo_hashes must contain only sha256 hex digests")

        if "blocked_repos" in scan:
            errors.append("blocked_repos plaintext list is not allowed in the public manifest")

        entries = payload.get("repos", [])
        if not isinstance(entries, list):
            errors.append("repos field must be a list")
            entries = []

        seen_keys: set[str] = set()
        public_entries = 0
        for index, entry in enumerate(entries):
            self._check_entry(index, entry, seen_keys, errors)
            if isinstance(entry, dict) and str(entry.get("public_release", "public")).strip().lower() == "public":
                public_entries += 1

        if public_entries == 0:
            errors.append("manifest must include at least one public allowlist entry")

        return ManifestCheckResult(not errors, errors, public_entries, len(blocked_hashes), recursive)

    def _load_payload(self, errors: list[str]) -> dict[str, Any] | None:
        if not self.manifest_path.exists():
            errors.append(f"missing manifest: {self.manifest_path.relative_to(ROOT)}")
            return None
        try:
            loaded = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON: {exc}")
            return None
        if not isinstance(loaded, dict):
            errors.append("manifest root must be an object")
            return None
        return loaded

    def _check_entry(self, index: int, entry: Any, seen_keys: set[str], errors: list[str]) -> None:
        if not isinstance(entry, dict):
            errors.append(f"repos[{index}] must be an object")
            return

        key = str(entry.get("key", ""))
        if not KEY_PATTERN.fullmatch(key):
            errors.append(f"repos[{index}] has invalid key: {key or '<missing>'}")
        if key in seen_keys:
            errors.append(f"duplicate repo key: {key}")
        seen_keys.add(key)

        release = str(entry.get("public_release", "public")).strip().lower()
        if release not in VALID_RELEASE_STATES:
            errors.append(f"{key} has invalid public_release: {release}")

        if release == "public":
            missing = sorted(PUBLIC_REQUIRED_FIELDS - entry.keys())
            if missing:
                errors.append(f"{key} missing public fields: {', '.join(missing)}")
            source_files = entry.get("source_files")
            if not isinstance(source_files, list) or not source_files:
                errors.append(f"{key} requires non-empty source_files list")
        else:
            errors.append(f"non-public repo entry must not remain in public repos list: {key}")


def main() -> int:
    result = PublicManifestContractChecker().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
