#!/usr/bin/env python3
"""Custodia Latina: Latin prose gate with explicit upstream-feeder exceptions.

Checks committed authored Markdown. Legacy content is inventoried, not silently
declared compliant. Executable code, JSON schemas, LaTeX syntax and generated
research text require separate source-level migration.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = "<!-- lingua: la -->"
ROOT_EXEMPT = {"README.md"}
FEEDER_PATHS = {"research/living_source_ledger.md"}
SKIP_PREFIXES = (".github/", "dist/", "documents/")
# Existing prose and generated research status pending manual/source translation.
LEGACY_AUTHORED = {
    "docs/LIVING_CV_ACTIONS.md",
    "docs/STEM_CITATION_VERIFICATION.md",
    "docs/STEM_CV_CURATOR.md",
    "docs/STEM_EVALUATOR_LIT_REVIEW_MATRIX.md",
    "docs/STEM_PAPER_EVALUATOR.md",
    "research/RESEARCH_STATUS.md",
}
ENGLISH_WORDS = re.compile(
    r"\b(?:the|and|this|that|these|those|with|without|from|which|"
    r"should|must|would|could|have|has|were|was|are|into|when|"
    r"where|their|your|before|after|whether|while|between)\b",
    re.IGNORECASE,
)
LATIN_WORDS = re.compile(
    r"\b(?:et|in|ad|de|cum|est|sunt|non|qui|quae|quod|"
    r"ante|post|tamen|sed|ne|ut|ubi|haec|hoc|sine|per|"
    r"inter|vel|aut|tantum|nisi|ex|e|quibus|autem)\b",
    re.IGNORECASE,
)
BARE_POINTER = re.compile(
    r"(?:[-*]\s*)?(?:https?://\S+|\.\./\S+|\[[^\]]+\]\((?:https?://|\.\./)[^)]+\))"
)
INLINE_CODE = re.compile(r"\x60[^\x60]*\x60")
LINK_DESTINATION = re.compile(r"\]\((?:https?://)[^)]+\)")


def is_pointer_only(content: str) -> bool:
    """Do not exempt mixed source pointers and local analysis."""
    lines = [
        s.strip()
        for s in content.splitlines()
        if s.strip()
        and not s.lstrip().startswith(("#", "<!--"))
    ]
    return bool(lines) and all(BARE_POINTER.fullmatch(s) for s in lines)


def suspicious_english_lines(content: str) -> list[int]:
    """Flag clear English prose; lexical heuristics never prove good Latin."""
    flagged: list[int] = []
    fenced = False
    for number, raw in enumerate(content.splitlines(), 1):
        line = raw.strip()
        if line.startswith((chr(96) * 3, "~~~")):
            fenced = not fenced
            continue
        if fenced or not line or line.startswith(("<!--", ">", "<", "%")):
            continue  # comments, quoted sources, HTML, or LaTeX
        candidate = INLINE_CODE.sub("", LINK_DESTINATION.sub("", line))
        words = re.findall(r"[A-Za-z]{2,}", candidate)
        if len(words) < 6:
            continue
        english = len(ENGLISH_WORDS.findall(candidate))
        latin = len(LATIN_WORDS.findall(candidate))
        if english >= 2 and english >= latin:
            flagged.append(number)
    return flagged


def audit(name: str, content: str) -> tuple[str, list[int]]:
    """Return status: exempt, feeder, pending, compliant, or violation."""
    if name in ROOT_EXEMPT:
        return "exempt", []
    if name in FEEDER_PATHS or is_pointer_only(content):
        return "feeder", []
    if MARK not in content[:256]:
        if name in LEGACY_AUTHORED:
            return "pending", []
        return "violation", []
    bad = suspicious_english_lines(content)
    return ("violation" if bad else "compliant"), bad


def main() -> int:
    paths = (
        subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
        )
        .stdout.decode()
        .split("\0")
    )
    counts = {key: 0 for key in ("exempt", "feeder", "pending", "compliant", "violation")}
    violations: list[str] = []
    pending: list[str] = []
    for name in paths:
        if not name or name.startswith(SKIP_PREFIXES) or not name.endswith(".md"):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        status, lines = audit(name, path.read_text(encoding="utf-8"))
        counts[status] += 1
        if status == "pending":
            pending.append(name)
        if status == "violation":
            detail = ", ".join(map(str, lines[:10])) if lines else "missing Latin declaration"
            violations.append(f"{name}: {detail}")
    for item in violations:
        print(f"Violatio linguae Latinae: {item}", file=sys.stderr)
    print(
        "Custodia Latina: "
        + ", ".join(f"{key}={value}" for key, value in counts.items())
    )
    if pending:
        print("Documenta adhuc convertenda: " + ", ".join(pending))
    print("Nota: recognitio humana linguae et translatio fontium generatorum necessaria manent.")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
