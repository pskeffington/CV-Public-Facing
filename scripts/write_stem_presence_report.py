#!/usr/bin/env python3
"""Generate a Markdown STEM presence dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OBJECTS_PATH = ROOT / "data" / "stem_cv_objects.json"
REPORT_PATH = ROOT / "research" / "stem_presence_report.md"

MATURITY_VALUATION_WEIGHTS = {
    "submitted": 20,
    "publication_ready": 18,
    "active_manuscript": 16,
    "validation_gated": 14,
    "active_scaffold": 10,
    "early_stage": 6,
    "intake": 2,
}

SECTION_VALUATION_WEIGHTS = {
    "machine_learning": 10,
    "biomedical_data": 9,
    "methods": 8,
    "public_health": 8,
    "publications": 7,
    "archive_history": 5,
    "intake": 2,
}

BAND_VALUATION_WEIGHTS = {
    "core_stem": 10,
    "stem_adjacent": 7,
    "mixed_or_transitional": 3,
    "low_stem_presence": 0,
}


def clean(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


def load_projects() -> list[dict[str, Any]]:
    payload = json.loads(OBJECTS_PATH.read_text(encoding="utf-8"))
    projects = payload.get("projects", [])
    return [p for p in projects if isinstance(p, dict)]


def valuation_band(signal: int) -> str:
    if signal >= 80:
        return "market_ready"
    if signal >= 65:
        return "near_market"
    if signal >= 45:
        return "developing_asset"
    return "training_stage"


def valuation_signal(score: int, band: str, maturity: str, section: str, curated: bool) -> int:
    maturity_bonus = MATURITY_VALUATION_WEIGHTS.get(maturity, 2)
    section_bonus = SECTION_VALUATION_WEIGHTS.get(section, 2)
    band_bonus = BAND_VALUATION_WEIGHTS.get(band, 0)
    curated_bonus = 5 if curated else 0
    raw = round((score * 0.55) + maturity_bonus + section_bonus + band_bonus + curated_bonus)
    return max(0, min(100, raw))


def valuation_basis(row: dict[str, object]) -> str:
    return (
        f"skill/STEM score={row['score']}; "
        f"band={row['band']}; "
        f"maturity={row['maturity']}; "
        f"section={row['section']}; "
        f"curated={row['curated']}"
    )


def get_row(project: dict[str, Any]) -> dict[str, object]:
    stem = project.get("stem_presence")
    repo = project.get("repository")
    if not isinstance(stem, dict):
        stem = {}
    if not isinstance(repo, dict):
        repo = {}

    score = int(stem.get("score", 0))
    band = str(stem.get("band", "low_stem_presence"))
    maturity = str(project.get("maturity", ""))
    section = str(project.get("cv_section", ""))
    curated = bool(project.get("curated", False))
    signal = valuation_signal(score, band, maturity, section, curated)

    row: dict[str, object] = {
        "title": project.get("title", "Untitled project"),
        "repository": repo.get("repo_full_name", ""),
        "section": section,
        "maturity": maturity,
        "score": score,
        "drift_score": int(stem.get("drift_score", 100)),
        "band": band,
        "valuation_signal": signal,
        "valuation_band": valuation_band(signal),
        "curated": "yes" if curated else "no",
        "rationale": stem.get("rationale", "No rationale recorded."),
    }
    row["valuation_basis"] = valuation_basis(row)
    return row


def render(projects: list[dict[str, Any]]) -> str:
    rows = [get_row(project) for project in projects]
    rows.sort(key=lambda row: (-int(row["valuation_signal"]), -int(row["score"]), clean(row["title"]).lower()))
    count = len(rows)
    avg_score = round(sum(int(row["score"]) for row in rows) / count, 1) if count else 0
    avg_drift = round(sum(int(row["drift_score"]) for row in rows) / count, 1) if count else 100
    avg_valuation = round(sum(int(row["valuation_signal"]) for row in rows) / count, 1) if count else 0

    band_counts: dict[str, int] = {}
    valuation_band_counts: dict[str, int] = {}
    for row in rows:
        band = clean(row["band"])
        valuation = clean(row["valuation_band"])
        band_counts[band] = band_counts.get(band, 0) + 1
        valuation_band_counts[valuation] = valuation_band_counts.get(valuation, 0) + 1

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
        f"Average valuation signal: {avg_valuation}",
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
        "## Valuation bands",
        "",
    ])
    if valuation_band_counts:
        for band in sorted(valuation_band_counts):
            lines.append(f"- `{band}`: {valuation_band_counts[band]}")
    else:
        lines.append("- No valuation bands computed.")

    lines.extend([
        "",
        "## Project scores",
        "",
        "| Project | Repository | Section | Maturity | STEM score | Drift score | Valuation signal | Valuation band | Band | Valuation basis | Rationale |",
        "|---|---|---|---|---:|---:|---:|---|---|---|---|",
    ])
    for row in rows:
        cells = [
            clean(row["title"]),
            "`" + clean(row["repository"]) + "`",
            clean(row["section"]),
            clean(row["maturity"]),
            str(row["score"]),
            str(row["drift_score"]),
            str(row["valuation_signal"]),
            clean(row["valuation_band"]),
            clean(row["band"]),
            clean(row["valuation_basis"]),
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
