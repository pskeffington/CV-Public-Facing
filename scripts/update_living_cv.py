#!/usr/bin/env python3
"""Generate public CV project objects from the pipeline repo manifest.

The generator is intentionally deterministic and conservative. It treats the
manifest as the public CV source of truth for project titles, status buckets,
summary language, and near-term needs, while also pulling the current README /
status surfaces from each listed public repository so the CV records where each
project was last observed. Missing source files are logged but do not fail the
public CV build; that lets intake-stage repos mature without breaking the CV.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pipeline_repos.json"
CV_PROJECTS = ROOT / "cv" / "current_projects_public.tex"
RESEARCH_BOARD = ROOT / "research" / "generated_project_board.tex"
STATUS_MD = ROOT / "research" / "RESEARCH_STATUS.md"
SOURCE_LEDGER = ROOT / "research" / "living_source_ledger.md"

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


@dataclass(frozen=True)
class Project:
    key: str
    repo: str
    title: str
    status: str
    summary: str
    needs: str
    cv_section: str
    source_files: tuple[str, ...]


def load_projects() -> list[Project]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    projects = []
    for item in data["repos"]:
        projects.append(
            Project(
                key=item["key"],
                repo=item["repo"],
                title=item["title"],
                status=item["status"],
                summary=item["summary"],
                needs=item["needs"],
                cv_section=item.get("cv_section", "current"),
                source_files=tuple(item.get("source_files", ["README.md"])),
            )
        )
    return projects


def tex_escape(text: str) -> str:
    replacements = {
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
    return "".join(replacements.get(char, char) for char in text)


def plain_status(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fetch_github_file(repo: str, path: str) -> tuple[bool, str]:
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref=main"
    headers = {
        "Accept": "application/vnd.github.raw",
        "User-Agent": "living-cv-generator",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return True, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False, "missing"
        return False, f"http {exc.code}"
    except Exception as exc:  # noqa: BLE001 - CI ledger should capture unexpected fetch issues.
        return False, f"error: {exc}"


def first_heading(markdown: str) -> str | None:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return None


def status_snippet(markdown: str) -> str | None:
    patterns = [
        r"(?im)^\*\*Repository status:\*\*\s*(.+)$",
        r"(?im)^\*\*Status:\*\*\s*(.+)$",
        r"(?im)^Status:\s*(.+)$",
        r"(?im)^# Current Project Status\s*$",
        r"(?im)^## Current status\s*$",
    ]
    for pattern in patterns[:3]:
        match = re.search(pattern, markdown)
        if match:
            return plain_status(match.group(1))
    lines = markdown.splitlines()
    for i, line in enumerate(lines):
        if re.match(patterns[3], line) or re.match(patterns[4], line):
            for candidate in lines[i + 1 : i + 7]:
                stripped = candidate.strip(" -")
                if stripped:
                    return plain_status(stripped)
    return None


def build_source_observations(projects: Iterable[Project]) -> dict[str, list[dict[str, str]]]:
    observations: dict[str, list[dict[str, str]]] = {}
    for project in projects:
        observations[project.key] = []
        for path in project.source_files:
            ok, content = fetch_github_file(project.repo, path)
            obs = {
                "repo": project.repo,
                "path": path,
                "available": "yes" if ok else "no",
                "heading": "",
                "status": "",
                "note": "",
            }
            if ok:
                obs["heading"] = first_heading(content) or ""
                obs["status"] = status_snippet(content) or ""
            else:
                obs["note"] = content
            observations[project.key].append(obs)
    return observations


def write_current_projects(projects: list[Project]) -> None:
    lines = [
        "% Auto-generated by scripts/update_living_cv.py from data/pipeline_repos.json.",
        "% Edit the manifest or upstream project README/status files rather than hand-editing this file.",
        "\\section*{Current Project Register}",
        "\\begin{itemize}",
    ]
    for project in projects:
        lines.append(
            f"    \\item \\textbf{{{tex_escape(project.title)}:}} {tex_escape(project.summary)}"
        )
    lines.extend(
        [
            "\\end{itemize}",
            "",
            "\\section*{Selected Project Outputs}",
            "\\begin{itemize}",
            "    \\item \\textbf{Submitted manuscript:} NLSY79 family-economics and fertility manuscript submitted for publication and currently under journal peer review.",
            "    \\item \\textbf{Decision-support prototype:} Stream-aware rural infrastructure and public-health planning outputs remain validation-gated before measured-risk language is used.",
            "    \\item \\textbf{Living CV intake:} Pipeline repositories are tracked as living objects whose public README/status surfaces feed the project board.",
            "\\end{itemize}",
            "",
        ]
    )
    CV_PROJECTS.write_text("\n".join(lines), encoding="utf-8")


def write_research_board(projects: list[Project]) -> None:
    lines = [
        "% Auto-generated by scripts/update_living_cv.py from data/pipeline_repos.json.",
        "% Edit the manifest or upstream project README/status files rather than hand-editing this file.",
        "\\section*{Research Storyboard}",
        "This portfolio is organized around careful, reproducible use of public-health, infrastructure, environmental, administrative, longitudinal, biomedical, safety-evaluation, and public-history data. The current emphasis is on building transparent workflows, documenting evidence boundaries, and moving selected projects from exploratory scaffolds toward validated manuscripts, methods notes, report artifacts, or decision-support tools.",
        "",
        "\\section*{Current Project Board}",
    ]
    for project in projects:
        lines.append(
            f"\\project{{{tex_escape(project.title)}}}{{{tex_escape(project.status)}}}{{{tex_escape(project.summary)}}}{{{tex_escape(project.needs)}}}"
        )
        lines.append("")
    RESEARCH_BOARD.write_text("\n".join(lines), encoding="utf-8")


def write_status_md(projects: list[Project]) -> None:
    lines = [
        "# Research Status",
        "",
        "Public-facing overview of current research, project maturity, validation boundaries, and near-term development needs.",
        "",
        "This file is generated from `data/pipeline_repos.json` and the living CV generator. Edit the manifest or upstream project README/status files rather than hand-editing this board.",
        "",
        "## Portfolio thesis",
        "",
        "This portfolio is organized around reproducible use of public-health, infrastructure, environmental, administrative, geospatial, biomedical, and longitudinal data. The work emphasizes transparent methods, careful evidence boundaries, and practical outputs that can support manuscripts, methods notes, public-history archives, and decision-support tools.",
        "",
        "## Current project board",
        "",
    ]
    for project in projects:
        lines.extend(
            [
                f"### {project.title} — {project.status}",
                "",
                f"**Current output:** {project.summary}  ",
                f"**Near-term needs:** {project.needs}",
                "",
            ]
        )
    lines.extend(
        [
            "## Completed / print-ready objects",
            "",
            "- Public CV package with academic CV, one-page profile, index-safe CV, and research-status outputs.",
            "- Gaza WASH presentation object suitable for conversion into a reproducible methods note.",
            "- McDowell GIS and stakeholder materials, pending official-source validation.",
            "",
            "## Pending validation",
            "",
            "- Water-quality and wastewater indicators remain secondary-extracted until confirmed through official or certified sources.",
            "- NLSY79 manuscript claims require continued citation, model-table, and sample-audit parity through peer review.",
            "- Early-stage repositories remain development objects until datasets, methods, and claim boundaries are frozen.",
            "",
            "## Submission-oriented work",
            "",
            "- NLSY79 family economics and fertility manuscript: submitted / journal peer review.",
            "- Gaza WASH assessment: presentation-complete object that can be converted into a methods note after source-manifest cleanup.",
            "",
            "## Immediate major needs",
            "",
            "- Keep public repository intake output wired into the export path so new public repositories are picked up before PDF builds.",
            "- Complete project-intake records for newly discovered public repositories before adding strong CV claims.",
            "- For McDowell, obtain official water-system and wastewater confirmation before using measured-risk language.",
            "- For NLSY79, preserve a direct audit trail from model output to LaTeX tables and future reviewer-response material.",
            "- For medical/noise projects, select public datasets before expanding claims.",
            "",
        ]
    )
    STATUS_MD.write_text("\n".join(lines), encoding="utf-8")


def write_source_ledger(projects: list[Project], observations: dict[str, list[dict[str, str]]]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Living CV Source Ledger",
        "",
        f"Last generated: {now}",
        "",
        "This ledger records which public README/status files were checked when regenerating the living CV project board. Missing files are allowed for intake-stage repositories but should be added over time.",
        "",
        "| Project | Repository | Source file | Available | Heading/status observed | Note |",
        "|---|---|---|---|---|---|",
    ]
    for project in projects:
        for obs in observations[project.key]:
            heading_status = obs.get("status") or obs.get("heading") or ""
            note = obs.get("note") or ""
            lines.append(
                "| {title} | `{repo}` | `{path}` | {available} | {heading_status} | {note} |".format(
                    title=project.title.replace("|", "/"),
                    repo=obs["repo"],
                    path=obs["path"],
                    available=obs["available"],
                    heading_status=heading_status.replace("|", "/"),
                    note=note.replace("|", "/"),
                )
            )
    lines.append("")
    SOURCE_LEDGER.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    projects = load_projects()
    observations = build_source_observations(projects)
    write_current_projects(projects)
    write_research_board(projects)
    write_status_md(projects)
    write_source_ledger(projects, observations)
    print(f"Generated living CV objects for {len(projects)} pipeline repositories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
