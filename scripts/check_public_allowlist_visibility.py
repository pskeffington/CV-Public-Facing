#!/usr/bin/env python3
"""Fail closed unless every CV allowlist repository is verified public.

The public CV manifest is a release allowlist, not merely a discovery list.
Every repository admitted to it must resolve through the GitHub API and report
`private: false`. API failure, missing metadata, or private visibility blocks
the public build rather than falling back to an assumed-public state.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pipeline_repos.json"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
BLOCKED_RELEASE_VALUES = {"blocked", "deny", "private", "restricted", "internal_only"}


def fetch_repo(full_name: str) -> tuple[bool, dict | str]:
    url = f"https://api.github.com/repos/{urllib.parse.quote(full_name, safe='/')}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "public-cv-allowlist-visibility-check",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
            return True, payload
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # fail closed on network/parse errors
        return False, str(exc)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures: list[str] = []
    checked = 0

    for entry in manifest.get("repos", []):
        release = str(entry.get("public_release", "public")).strip().lower()
        if release in BLOCKED_RELEASE_VALUES:
            continue

        full_name = str(entry.get("repo", "")).strip()
        if not full_name:
            failures.append("manifest entry missing repo name")
            continue

        checked += 1
        ok, result = fetch_repo(full_name)
        if not ok:
            failures.append(f"{full_name}: visibility could not be verified ({result})")
            continue

        assert isinstance(result, dict)
        if result.get("private") is not False:
            failures.append(f"{full_name}: repository is not verified public")

        returned_name = str(result.get("full_name", ""))
        if returned_name.lower() != full_name.lower():
            failures.append(f"{full_name}: API identity mismatch ({returned_name or 'missing full_name'})")

    if failures:
        print("Public allowlist visibility check failed.", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 2

    print(f"Public allowlist visibility check passed for {checked} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
