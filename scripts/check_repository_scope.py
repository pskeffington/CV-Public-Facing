#!/usr/bin/env python3
"""Custodia ambitus: fasciculi in historia publica ad munus repositorii pertineant."""

from __future__ import annotations

import pathlib
import subprocess
import sys
from collections.abc import Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]

ROOT_FILES = frozenset({
    ".gitattributes",
    ".gitignore",
    "CONTRIBUTING.md",
    "Dartmouth_CV.md",
    "Makefile",
    "PUBLIC_MANIFEST.md",
    "README.md",
    "portfolio_valuation_manifest.json",
})
ROOT_DIRS = frozenset({
    ".github",
    "cv",
    "data",
    "docs",
    "documents",
    "hire",
    "research",
    "scripts",
})
BINARY_OUTPUT_EXTENSIONS = frozenset({
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".zip",
    ".tar",
    ".exe",
})


def check_paths(paths: Iterable[str]) -> list[str]:
    """Vias ab indice Git acceptas ad fines editionis publicae examinat."""
    findings: list[str] = []
    for path in sorted(set(paths)):
        if not path:
            continue
        p = pathlib.PurePosixPath(path)
        if p.is_absolute() or ".." in p.parts:
            findings.append(f"{path}: via extra repositorium")
            continue
        if len(p.parts) == 1:
            if path not in ROOT_FILES:
                findings.append(f"{path}: fasciculus radicis non admissus")
            continue
        if p.parts[0] not in ROOT_DIRS:
            findings.append(f"{path}: directorium ab ambitu publico alienum")
            continue
        if p.parts[0] == "documents" and path != "documents/.gitkeep":
            findings.append(f"{path}: effectus generationis in historia non servandus")
            continue
        if p.suffix.lower() in BINARY_OUTPUT_EXTENSIONS:
            findings.append(f"{path}: effectus binarius ad GitHub Releases pertinet")
    return findings


def main() -> int:
    paths = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8").split("\0")
    findings = check_paths(paths)
    for finding in findings:
        print("Violatio ambitus publici: " + finding, file=sys.stderr)
    if findings:
        return 2
    print(f"Custodia ambitus publici: {sum(bool(p) for p in paths)} fasciculi examinati.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
