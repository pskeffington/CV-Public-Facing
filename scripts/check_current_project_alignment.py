#!/usr/bin/env python3
"""Check current selections without treating historical metadata as intake."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from stem_cv_curator import tex_escape

ROOT = Path(__file__).resolve().parents[1]
RETIRED = "cart-trace"
SURFACES = {
    "cv/current_projects_public.tex": (r"\cvrole{", "}"),
    "research/generated_project_board.tex": (r"\project{", "}"),
    "research/RESEARCH_STATUS.md": ("#### ", " - "),
}


def check(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads((root / "data/pipeline_repos.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Cannot read current project manifest: {exc}"]
    if not isinstance(manifest, dict) or not isinstance(manifest.get("repos"), list):
        return ["Manifest must contain a repos list."]
    entries = manifest["repos"]
    titles: list[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"Project record {index} is not an object.")
            continue
        fields = [entry.get(key) for key in ("key", "repo", "title")]
        if any(not isinstance(value, str) or not value.strip() for value in fields):
            errors.append(f"Project record {index} lacks a valid key, repo or title.")
            continue
        if any(RETIRED in value.casefold() for value in fields):
            errors.append(f"Retired project appears in current manifest record {index}.")
        if entry.get("public_release", "public") != "public":
            errors.append(f"Current manifest record {index} is not public.")
        titles.append(entry["title"])
    if not titles or len(titles) != len(set(titles)):
        errors.append("Current project titles must be nonempty and unique.")
    for name, (prefix, suffix) in SURFACES.items():
        try:
            text = (root / name).read_text(encoding="utf-8")
        except OSError:
            errors.append(f"Missing current selection surface: {name}")
            continue
        if RETIRED in text.casefold():
            errors.append(f"Retired project appears in current selection surface: {name}")
        if text.count(prefix) != len(titles):
            errors.append(f"Selection count differs from manifest in {name}.")
        for title in titles:
            rendered = tex_escape(title) if name.endswith(".tex") else title
            if text.count(prefix + rendered + suffix) != 1:
                errors.append(f"Expected one selection for {title} in {name}.")
    try:
        profile = (root / "cv/one_page_profile_public.tex").read_text(encoding="utf-8")
        if RETIRED in profile.casefold():
            errors.append("Retired project appears in the curated public profile.")
    except OSError:
        errors.append("Missing curated public profile.")
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("Current public project alignment failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Current public project alignment passed; historical metadata retained.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
