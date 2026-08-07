#!/usr/bin/env python3
"""Apply small public-safe positioning overrides after STEM CV generation.

The curator intentionally reduces project status to broad maturity buckets. This
post-processing step preserves externally meaningful completion language for
projects whose manifest explicitly records completed/accepted work, without
changing the underlying evidence boundaries or public-release controls.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pipeline_repos.json"
CURRENT_PROJECTS = ROOT / "cv" / "current_projects_public.tex"
RESEARCH_BOARD = ROOT / "research" / "generated_project_board.tex"
RESEARCH_STATUS = ROOT / "research" / "RESEARCH_STATUS.md"


def tex_escape(text: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(c, c) for c in text)


def completed_entries() -> list[dict[str, str]]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out: list[dict[str, str]] = []
    for item in data.get("repos", []):
        status = str(item.get("status", ""))
        lower = status.lower()
        if "completed" in lower or "accepted" in lower:
            out.append(item)
    return out


def patch_current_projects(item: dict[str, str]) -> None:
    text = CURRENT_PROJECTS.read_text(encoding="utf-8")
    title = tex_escape(item["title"])
    status = tex_escape(item["status"])
    summary = tex_escape(item["summary"])
    repo_name = tex_escape(item["repo"].split("/", 1)[-1])
    replacement = (
        f"\\cvrole{{{title}}}{{{status}}}\n"
        f"\\cvplace{{{repo_name}}}\n"
        "\\begin{itemize}\n"
        f"    \\item {summary}\n"
        "\\end{itemize}"
    )
    pattern = re.compile(
        rf"\\cvrole\{{{re.escape(title)}\}}\{{.*?\}}\n"
        rf"\\cvplace\{{.*?\}}\n"
        rf"\\begin\{{itemize\}}\n.*?\\end\{{itemize\}}",
        re.DOTALL,
    )
    text, count = pattern.subn(lambda _: replacement, text, count=1)
    if count:
        CURRENT_PROJECTS.write_text(text, encoding="utf-8")


def patch_research_board(item: dict[str, str]) -> None:
    text = RESEARCH_BOARD.read_text(encoding="utf-8")
    title = tex_escape(item["title"])
    status = tex_escape(item["status"])
    summary = tex_escape(item["summary"])
    needs = tex_escape(item["needs"])
    replacement = f"\\project{{{title}}}{{{status}}}{{{summary}}}{{{needs}}}"
    pattern = re.compile(rf"\\project\{{{re.escape(title)}\}}\{{.*?\}}\{{.*?\}}\{{.*?\}}")
    text, count = pattern.subn(lambda _: replacement, text, count=1)
    if count:
        RESEARCH_BOARD.write_text(text, encoding="utf-8")


def patch_research_status(item: dict[str, str]) -> None:
    text = RESEARCH_STATUS.read_text(encoding="utf-8")
    title = item["title"]
    status = item["status"]
    pattern = re.compile(rf"^#### {re.escape(title)} - .*?$", re.MULTILINE)
    text, count = pattern.subn(f"#### {title} - {status}", text, count=1)
    if count:
        RESEARCH_STATUS.write_text(text, encoding="utf-8")


def main() -> int:
    for item in completed_entries():
        patch_current_projects(item)
        patch_research_board(item)
        patch_research_status(item)
    print("Applied public CV completion-status positioning overrides.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
