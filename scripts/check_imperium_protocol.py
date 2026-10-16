#!/usr/bin/env python3
"""Public CV baseline Imperium governance gate; never processes private data."""
from __future__ import annotations
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXCLUDED = {"README.md"}
# These are prohibited *uses* in public artifacts, not mere mentions in policy docs.
FORBIDDEN = (
    re.compile(r"(?i)\\b(?:social[_ -]?credit|imperium[_ -]?score|historical[_ -]?rank)[_ -]?(?:for[_ -]?)?(?:hiring|eligibility|employment|admission|promotion|compensation)\\b"),
    re.compile(r"(?i)\\b(?:automated|algorithmic)\\s+(?:employment|hiring|eligibility)\\s+(?:decision|approval|rejection)\\b"),
)
EXTENSIONS = {".md", ".tex", ".json", ".yml", ".yaml", ".py", ".sh"}
IGNORED_PREFIXES = (".git/", "documents/", "dist/")
def main() -> int:
    paths = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True).stdout.decode().split("\\0")
    problems = []
    in_scope = 0
    for name in paths:
        if not name or name in EXCLUDED or name.startswith(IGNORED_PREFIXES):
            continue
        p = ROOT / name
        if not p.is_file() or p.suffix.lower() not in EXTENSIONS:
            continue
        data = p.read_text(encoding="utf-8", errors="replace")
        # Reference-only files whose content consists exclusively of links are upstream pointers.
        meaningful = [s.strip() for s in data.splitlines() if s.strip() and not s.lstrip().startswith("#")]
        if meaningful and all(s.startswith(("https://", "http://", "../")) for s in meaningful):
            continue
        in_scope += 1
        # Check active statements only: ignore markdown quotations and commented lines.
        for index, line in enumerate(data.splitlines(), 1):
            stripped = line.lstrip()
            if stripped.startswith(("#", ">", "%", "//", "*", "-")):
                continue
            if any(pattern.search(line) for pattern in FORBIDDEN):
                problems.append(f"{name}:{index}: prohibited consequential ranking language")
    for item in problems:
        print(item, file=sys.stderr)
    print(f"Imperium public governance baseline: {in_scope} applicable text files checked; {len(problems)} findings")
    return 1 if problems else 0
if __name__ == "__main__":
    raise SystemExit(main())
