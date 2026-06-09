#!/usr/bin/env python3
"""Keep generated public CV files aligned with the portfolio taxonomy."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CV_PROJECTS_PATH = ROOT / "cv" / "current_projects_public.tex"
RESEARCH_BOARD_TEX_PATH = ROOT / "research" / "generated_project_board.tex"
RESEARCH_STATUS_MD_PATH = ROOT / "research" / "RESEARCH_STATUS.md"

CV_ANCHORS = [
    ("Family economics, financial literacy, and fertility", "Longitudinal NLSY79 manuscript work using applied economics, health data science, and reproducible table development."),
    ("Rural and global health systems", "Applied public-health work on WASH, water and wastewater infrastructure, health-system disruption, terrain and access constraints, environmental-health indicators, and community vulnerability."),
    ("Maternal, child, reproductive, and life-course health", "Research direction connecting family economics, fertility, household context, and reproductive outcomes to maternal-child and life-course population health."),
    ("Cancer outcomes and end-of-life care", "Methods work focused on cancer end-of-life typologies, place-of-death patterns, care-quality variation, and reproducible biomedical study design."),
    ("Biomedical data science methods", "Early work on ECG signal quality, PET imaging robustness, and responsible machine-learning evaluation using public-data methods."),
    ("Public-history and archival indexing", "Public-history work using transcription, entity modeling, and uncertainty notes for Catholic material-culture records."),
]

RESEARCH_ANCHORS = [
    ("Family economics, financial literacy, and fertility", "Under peer review", "Longitudinal NLSY79 manuscript work connecting family economics, fertility, household context, and reproductive outcomes.", "Continue peer-review response planning and manuscript development."),
    ("Rural water, wastewater, and infrastructure health", "In preparation", "Applied rural-health work on water, wastewater, terrain, access, environmental-health indicators, and community vulnerability.", "Continue official-source review and manuscript drafting."),
    ("Humanitarian WASH and health-system disruption", "In preparation", "Global-health work connecting WASH, displacement, environmental-health, and health-system disruption.", "Develop a public-health methods note with conservative interpretation."),
    ("Maternal, child, reproductive, and life-course health", "Developing", "Research direction connecting fertility, family economics, household context, and intergenerational health.", "Extend longitudinal methods toward maternal-child and life-course health questions."),
    ("Cancer outcomes and end-of-life care", "Developing", "Methods work focused on place-of-death patterns, cancer care, and end-of-life quality variation.", "Identify public data sources and define outcome measures."),
    ("Biomedical data science methods", "Developing", "Early work on ECG signal quality, PET imaging robustness, and reproducible biomedical study design.", "Select public datasets and define benchmark questions."),
    ("Public-history and archival indexing", "Developing", "Public-history work using transcription, entity modeling, and uncertainty notes for Catholic material-culture records.", "Continue indexing and documentation."),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def ensure_block(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    insert_at = 0
    while insert_at < len(lines) and lines[insert_at].startswith("%"):
        insert_at += 1
    return "\n".join(lines[:insert_at] + [block.rstrip(), ""] + lines[insert_at:])


def sync_cv_projects() -> None:
    lines = ["\\section*{Research Experience}", "\\begin{itemize}"]
    for title, summary in CV_ANCHORS:
        lines.append(f"    \\item \\textbf{{{title}:}} {summary}")
    lines.append("\\end{itemize}")
    text = read_text(CV_PROJECTS_PATH)
    write_text(CV_PROJECTS_PATH, ensure_block(text, CV_ANCHORS[0][0], "\n".join(lines)))


def sync_research_board() -> None:
    lines = ["\\section*{Research Areas}", "This portfolio is organized around health policy, health services research, rural and global health, maternal-child and life-course health, cancer outcomes, and reproducible health data science.", "", "\\section*{Current Research}"]
    for title, status, summary, needs in RESEARCH_ANCHORS:
        lines.append(f"\\project{{{title}}}{{{status}}}{{{summary}}}{{{needs}}}")
        lines.append("")
    text = read_text(RESEARCH_BOARD_TEX_PATH)
    write_text(RESEARCH_BOARD_TEX_PATH, ensure_block(text, RESEARCH_ANCHORS[0][0], "\n".join(lines)))


def sync_research_status() -> None:
    lines = ["## Portfolio thesis", "", "This portfolio is organized around health policy, health services research, rural and global health, maternal-child and life-course health, cancer outcomes, and reproducible health data science.", "", "## Current research", ""]
    for title, status, summary, _needs in RESEARCH_ANCHORS:
        lines += [f"### {title} - {status}", "", summary, ""]
    text = read_text(RESEARCH_STATUS_MD_PATH)
    write_text(RESEARCH_STATUS_MD_PATH, ensure_block(text, RESEARCH_ANCHORS[0][0], "\n".join(lines)))


def main() -> int:
    sync_cv_projects()
    sync_research_board()
    sync_research_status()
    print("Public portfolio anchors synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
