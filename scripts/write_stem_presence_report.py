#!/usr/bin/env python3
"""Generate a Markdown STEM presence dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OBJECTS_PATH = ROOT / "data" / "stem_cv_objects.json"
REPORT_PATH = ROOT / "research" / "stem_presence_report.md"


def clean(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


def load_projects() -> list[dict[str, Any]]:
    payload = json.loads(OBJECTS_PATH.read_text(encoding="utf-8"))
    projects = payload.get("projects", [])
    return [p for p in projects if isinstance(p, dict)]


def get_row(project: dict[str, Any]) -> dict[str, object]:
    stem = project.get("stem_presence")
    repo = project.get("repository")
    if not isinstance(stem, dict):
        stem = {}
    if not isinstance(repo, dict):
        repo = {}
    return {
        "title": project.get("title", "Untitled project"),
        "repository": repo.get("repo_full_name", ""),
        "section": project.get("cv_section", ""),
        "maturity": project.get("maturity", ""),
        "score": int(stem.get("score", 0)),
        "drift_score": int(stem.get("drift_score", 100)),
        "band": stem.get("band", "low_stem_presence"),
        "rationale": stem.get("rationale", "No rationale recorded."),
    }


def render(projects: list[dict[str, Any]]) -> str:
    rows = [get_row(project) for project in projects]
    rows.sort(key=lambda row: (-int(row["score"]), clean(row["title"]).lower()))
    count = len(rows)
    avg_score = round(sum(int(row["score"]) for row in rows) / count, 1) if count else 0
    avg_drift = round(sum(int(row["drift_score"]) for row in rows) / count, 1) if count else 100

    band_counts: dict[str, int] = {}
    for row in rows:
        band = clean(row["band"])
        band_counts[band] = band_counts.get(band, 0) + 1

    lines = [
        "# STEM Presence Report",
        "",
        "Generated from `data/stem_cv_objects.json`.",
        "",
        "## Portfolio summary",
        "",
        f"Project count: {count}",
        f"Average STEM presence score: {avg_score}",
        f"Average drift score: {avg_drift}",
        "",
        "## Band counts",
        "",
    ]
    if band_counts:
        for band in sorted(band_counts):
            lines.append(f"- `{band}`: {band_counts[band]}")
    else:
        lines.append("- No projects scored.")

    lines.extend([
        "",
        "## Project scores",
        "",
        "| Project | Repository | Section | Maturity | STEM score | Drift score | Band | Rationale |",
        "|---|---|---|---|---:|---:|---|---|",
    ])
    for row in rows:
        cells = [
            clean(row["title"]),
            "`" + clean(row["repository"]) + "`",
            clean(row["section"]),
            clean(row["maturity"]),
            str(row["score"]),
            str(row["drift_score"]),
            clean(row["band"]),
            clean(row["rationale"]),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    REPORT_PATH.write_text(render(load_projects()), encoding="utf-8")
    print("Wrote " + str(REPORT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
