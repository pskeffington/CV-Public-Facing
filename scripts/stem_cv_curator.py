#!/usr/bin/env python3
"""Cloneable STEM CV Curator.

A user can clone this repository, set STEM_CV_OWNER to their GitHub username,
and run `make public-package` to generate a living CV object layer from their
own active public repositories.

The script is conservative by design. It scans active public repositories,
merges optional curated overrides from data/pipeline_repos.json, reads public
README/status surfaces, creates STEM CV objects, scores STEM presence/drift,
and renders the existing LaTeX input files used by the public CV package.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from stem_presence import StemPresenceScore, StemPresenceScorer

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "pipeline_repos.json"
OBJECTS_PATH = ROOT / "data" / "stem_cv_objects.json"
CV_PROJECTS_PATH = ROOT / "cv" / "current_projects_public.tex"
RESEARCH_BOARD_TEX_PATH = ROOT / "research" / "generated_project_board.tex"
RESEARCH_STATUS_MD_PATH = ROOT / "research" / "RESEARCH_STATUS.md"
SOURCE_LEDGER_PATH = ROOT / "research" / "living_source_ledger.md"
REPO_SCAN_PATH = ROOT / "research" / "living_repo_scan.md"
BLOCKED_RELEASE_LEDGER_PATH = ROOT / "research" / "blocked_release_ledger.md"

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
OWNER_OVERRIDE = os.environ.get("STEM_CV_OWNER")
INCLUDE_PRIVATE = os.environ.get("STEM_CV_INCLUDE_PRIVATE", "false").lower() == "true"
TRIGGER = os.environ.get("STEM_CV_TRIGGER", "local")

SECTION_ORDER = [
    "publications",
    "machine_learning",
    "public_health",
    "biomedical_data",
    "methods",
    "archive_history",
    "intake",
]

SECTION_LABELS = {
    "publications": "Submitted and Publication-Oriented Work",
    "machine_learning": "Machine Learning and Reproducible Research Tools",
    "public_health": "Public Health, Infrastructure, and Environmental Evidence",
    "biomedical_data": "Biomedical Data and Signal/Imaging Methods",
    "methods": "Computational Methods and Safety Evaluation",
    "archive_history": "Archive and Public-History Indexing",
    "intake": "Discovered Repository Intake",
}

BLOCKED_PUBLIC_RELEASE_VALUES = {"blocked", "deny", "private", "restricted", "internal_only", "high_sec"}


@dataclass
class RepositoryObject:
    repo_full_name: str
    repo_name: str
    owner: str
    url: str
    visibility: str
    default_branch: str = "main"
    archived: bool = False
    active_status: str = "intake"
    last_observed_at: str | None = None
    topics: list[str] = field(default_factory=list)
    detected_domains: list[str] = field(default_factory=list)


@dataclass
class RepoSurfaceObject:
    repo_full_name: str
    source_path: str
    source_type: str
    available: bool
    heading: str | None = None
    status_line: str | None = None
    summary_text: str | None = None
    retrieval_time: str | None = None
    note: str | None = None


@dataclass
class ProjectObject:
    project_id: str
    title: str
    repository: RepositoryObject
    maturity: str
    cv_section: str
    public_summary: str
    near_term_needs: str
    source_surfaces: list[RepoSurfaceObject] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    stem_presence: StemPresenceScore | None = None
    include_in_cv: bool = True
    include_in_resume: bool = False
    display_priority: int = 100
    curated: bool = False
    public_release: str = "public"
    release_reason: str | None = None


@dataclass
class BlockedProjectRecord:
    project_id: str
    repo_full_name: str
    public_release: str
    release_reason: str
    curated: bool


@dataclass
class ClaimObject:
    claim_id: str
    project_id: str
    claim_text: str
    claim_strength: str
    evidence_paths: list[str] = field(default_factory=list)
    public_safe: bool = True
    cv_allowed: bool = True
    resume_allowed: bool = True
    needs_review: bool = False


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {"scan": {}, "repos": []}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def request_json(url: str) -> tuple[bool, Any]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "stem-cv-curator"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return True, json.loads(res.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        return False, f"http {exc.code}"
    except Exception as exc:
        return False, f"error: {exc}"


def request_raw(url: str) -> tuple[bool, str]:
    headers = {"Accept": "application/vnd.github.raw", "User-Agent": "stem-cv-curator"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return True, res.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False, "missing"
        return False, f"http {exc.code}"
    except Exception as exc:
        return False, f"error: {exc}"


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-") or "object"


def repo_key(value: str) -> str:
    return value.strip().lower()


def repo_name_key(value: str) -> str:
    return repo_key(value.split("/")[-1])


def title_from_repo(name: str) -> str:
    parts = [p for p in re.split(r"[-_.\s]+", name.strip("-_ .")) if p]
    acronyms = {"cv": "CV", "ml": "ML", "ecg": "ECG", "pet": "PET", "wash": "WASH", "gis": "GIS", "nlsy": "NLSY"}
    return " ".join(acronyms.get(p.lower(), p.capitalize()) for p in parts) or name


def detect_domains(repo_name: str, text: str) -> list[str]:
    haystack = f"{repo_name} {text}".lower()
    rules = [
        ("machine_learning", ["ml", "machine learning", "model-card", "benchmark", "best practices", "classifier", "regression", "neural"]),
        ("public_health", ["health", "wash", "water", "mcdowell", "haiti", "practicum", "emergency", "preparedness"]),
        ("biomedical_data", ["ecg", "pet", "radiomics", "cancer", "signal", "imaging", "clinical"]),
        ("methods", ["cipher", "topology", "identity", "abuse", "safety", "risk", "evaluation"]),
        ("archive_history", ["archive", "bonaventure", "hebrew", "reliquary", "trans"]),
        ("publications", ["family", "economic", "nlsy", "manuscript", "publication"]),
    ]
    domains = [domain for domain, tokens in rules if any(token in haystack for token in tokens)]
    return domains or ["intake"]


def primary_section(domains: list[str]) -> str:
    for section in SECTION_ORDER:
        if section in domains:
            return section
    return "intake"


def maturity_from_status(status: str, curated: bool) -> str:
    lower = status.lower()
    if "submitted" in lower or "peer review" in lower:
        return "submitted"
    if "publication" in lower and "ready" in lower:
        return "publication_ready"
    if "manuscript" in lower and "active" in lower:
        return "active_manuscript"
    if "validation" in lower:
        return "validation_gated"
    if "early" in lower:
        return "early_stage"
    if "active" in lower or curated:
        return "active_scaffold"
    return "intake"


def source_type(path: str) -> str:
    low = path.lower()
    if low == "readme.md":
        return "README"
    if "project_status" in low:
        return "PROJECT_STATUS"
    if "roadmap" in low:
        return "ROADMAP"
    if "reproduc" in low:
        return "REPRODUCIBILITY"
    if "citation" in low:
        return "CITATION"
    return "DOCS"


def first_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.strip().startswith("#"):
            return line.strip().lstrip("#").strip()
    return None


def status_line(text: str) -> str | None:
    for pat in [r"(?im)^\*\*Repository status:\*\*\s*(.+)$", r"(?im)^\*\*Status:\*\*\s*(.+)$", r"(?im)^Status:\s*(.+)$"]:
        m = re.search(pat, text)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()
    return None


def summary_text(text: str) -> str | None:
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("**") or s.startswith("|") or s.startswith("-"):
            continue
        if len(s) > 40:
            return re.sub(r"\s+", " ", s).strip()
    return None


def surface_evidence_text(surfaces: list[RepoSurfaceObject]) -> str:
    parts: list[str] = []
    for surface in surfaces:
        parts.extend([
            surface.source_path,
            surface.source_type,
            surface.heading or "",
            surface.status_line or "",
            surface.summary_text or "",
        ])
    return " ".join(part for part in parts if part)


def public_release_value(override: dict[str, Any] | None) -> str:
    if not override:
        return "public"
    return str(override.get("public_release", "public")).strip().lower()


def release_reason_value(override: dict[str, Any] | None) -> str | None:
    if not override:
        return None
    reason = str(override.get("release_reason", "")).strip()
    return reason or None


def blocked_repo_names(manifest: dict[str, Any]) -> set[str]:
    scan = manifest.get("scan", {})
    explicit = {repo_key(str(item)) for item in scan.get("blocked_repos", [])}
    explicit |= {repo_name_key(str(item)) for item in scan.get("blocked_repos", [])}
    for item in manifest.get("repos", []):
        if str(item.get("public_release", "public")).strip().lower() in BLOCKED_PUBLIC_RELEASE_VALUES:
            explicit.add(repo_key(str(item.get("repo", ""))))
            explicit.add(repo_name_key(str(item.get("repo", ""))))
    return {item for item in explicit if item}


def is_repo_blocked(repo: dict[str, Any], manifest: dict[str, Any], override: dict[str, Any] | None) -> bool:
    if public_release_value(override) in BLOCKED_PUBLIC_RELEASE_VALUES:
        return True
    blocked = blocked_repo_names(manifest)
    full = repo_key(str(repo.get("full_name", "")))
    name = repo_name_key(str(repo.get("name", "")))
    return full in blocked or name in blocked


def scan_repositories(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    scan = manifest.get("scan", {})
    owner = OWNER_OVERRIDE or scan.get("owner") or "pskeffington"
    include_private = INCLUDE_PRIVATE or bool(scan.get("include_private_repos", False))
    excluded = {str(x).lower() for x in scan.get("exclude_repos", ["CV", "CV-Public-Facing"])}
    excluded |= blocked_repo_names(manifest)
    repos: list[dict[str, Any]] = []
    page = 1
    if include_private and TOKEN:
        endpoint = "https://api.github.com/user/repos?visibility=all&affiliation=owner&sort=updated&direction=desc"
    else:
        endpoint = f"https://api.github.com/users/{owner}/repos?type=owner&sort=updated&direction=desc"
    while True:
        ok, payload = request_json(f"{endpoint}&per_page=100&page={page}")
        if not ok or not isinstance(payload, list) or not payload:
            break
        for repo in payload:
            name = str(repo.get("name", ""))
            full = str(repo.get("full_name", name))
            if not name or name.lower() in excluded or full.lower() in excluded:
                continue
            if repo.get("archived"):
                continue
            if repo.get("private") and not include_private:
                continue
            repos.append(repo)
        if len(payload) < 100:
            break
        page += 1
    return repos


def curated_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("repo", "")).lower(): item for item in manifest.get("repos", [])}


def fetch_surfaces(repo_full_name: str, paths: list[str]) -> list[RepoSurfaceObject]:
    out: list[RepoSurfaceObject] = []
    for path in paths:
        url = f"https://api.github.com/repos/{repo_full_name}/contents/{urllib.parse.quote(path)}?ref=main"
        ok, text = request_raw(url)
        out.append(RepoSurfaceObject(
            repo_full_name=repo_full_name,
            source_path=path,
            source_type=source_type(path),
            available=ok,
            heading=first_heading(text) if ok else None,
            status_line=status_line(text) if ok else None,
            summary_text=summary_text(text) if ok else None,
            retrieval_time=now_utc(),
            note=None if ok else text,
        ))
    return out


def repository_object(repo: dict[str, Any], domains: list[str]) -> RepositoryObject:
    name = str(repo.get("name", ""))
    full = str(repo.get("full_name", name))
    owner = str(repo.get("owner", {}).get("login", full.split("/")[0]))
    return RepositoryObject(
        repo_full_name=full,
        repo_name=name,
        owner=owner,
        url=str(repo.get("html_url", f"https://github.com/{full}")),
        visibility="private" if repo.get("private") else "public",
        default_branch=str(repo.get("default_branch", "main")),
        archived=bool(repo.get("archived", False)),
        active_status="active",
        last_observed_at=now_utc(),
        topics=list(repo.get("topics", [])) if isinstance(repo.get("topics"), list) else [],
        detected_domains=domains,
    )


def build_stem_presence(
    scorer: StemPresenceScorer,
    repo: dict[str, Any],
    title: str,
    status: str,
    section: str,
    summary: str,
    needs: str,
    surfaces: list[RepoSurfaceObject],
) -> StemPresenceScore:
    topics = " ".join(repo.get("topics", [])) if isinstance(repo.get("topics"), list) else ""
    return scorer.score_text(
        str(repo.get("name", "")),
        title,
        topics,
        status,
        section,
        summary,
        needs,
        surface_evidence_text(surfaces),
    )


def build_blocked_records(manifest: dict[str, Any]) -> list[BlockedProjectRecord]:
    records: list[BlockedProjectRecord] = []
    for item in manifest.get("repos", []):
        release = str(item.get("public_release", "public")).strip().lower()
        if release not in BLOCKED_PUBLIC_RELEASE_VALUES:
            continue
        records.append(BlockedProjectRecord(
            project_id=str(item.get("key") or slugify(str(item.get("repo", "blocked-object")))),
            repo_full_name=str(item.get("repo", "")),
            public_release=release,
            release_reason=str(item.get("release_reason", "blocked_from_public_outputs")),
            curated=True,
        ))
    return records


def build_projects(manifest: dict[str, Any]) -> list[ProjectObject]:
    overrides = curated_map(manifest)
    scorer = StemPresenceScorer()
    default_status = manifest.get("scan", {}).get("default_status", "Discovered active repository / intake needed")
    projects: list[ProjectObject] = []
    for repo in scan_repositories(manifest):
        full = str(repo.get("full_name", ""))
        name = str(repo.get("name", ""))
        override = overrides.get(full.lower())
        if is_repo_blocked(repo, manifest, override):
            continue
        paths = override.get("source_files", ["README.md", "PROJECT_STATUS.md", "ROADMAP.md"]) if override else ["README.md", "PROJECT_STATUS.md", "ROADMAP.md"]
        surfaces = fetch_surfaces(full, paths)
        surface_blob = surface_evidence_text(surfaces)
        domains = detect_domains(name, surface_blob)
        repo_obj = repository_object(repo, domains)
        curated = override is not None
        title = override.get("title") if override else title_from_repo(name)
        status = override.get("status") if override else default_status
        section = override.get("cv_section") if override else primary_section(domains)
        aliases = {"current": "public_health", "archive": "archive_history"}
        section = aliases.get(section, section)
        summary = override.get("summary") if override else (next((s.summary_text for s in surfaces if s.summary_text), None) or f"Public repository discovered by the STEM CV Curator for {title}; status and claim boundaries remain intake-stage until curated.")
        needs = override.get("needs") if override else "Add or refresh README/status documentation, source manifest, claim boundary, and public deliverable target."
        stem_presence = build_stem_presence(scorer, repo, title, status, section, summary, needs, surfaces)
        projects.append(ProjectObject(
            project_id=override.get("key") if override else slugify(name),
            title=title,
            repository=repo_obj,
            maturity=maturity_from_status(status, curated),
            cv_section=section,
            public_summary=summary,
            near_term_needs=needs,
            source_surfaces=surfaces,
            keywords=domains,
            stem_presence=stem_presence,
            include_in_cv=True,
            include_in_resume=section in {"machine_learning", "biomedical_data", "methods", "public_health"},
            display_priority=int(override.get("priority", 50 if curated else 150)) if override else 150,
            curated=curated,
            public_release=public_release_value(override),
            release_reason=release_reason_value(override),
        ))
    rank = {section: i for i, section in enumerate(SECTION_ORDER)}
    projects.sort(key=lambda p: (rank.get(p.cv_section, 99), p.display_priority, p.title.lower()))
    return projects


def build_claims(projects: list[ProjectObject]) -> list[ClaimObject]:
    claims: list[ClaimObject] = []
    for p in projects:
        evidence = [s.source_path for s in p.source_surfaces if s.available]
        claims.append(ClaimObject(
            claim_id=f"claim-{p.project_id}",
            project_id=p.project_id,
            claim_text=p.public_summary,
            claim_strength="source_supported" if evidence else "repo_supported",
            evidence_paths=evidence,
            public_safe=True,
            cv_allowed=True,
            resume_allowed=p.include_in_resume,
            needs_review=not p.curated,
        ))
    return claims


def tex_escape(text: str) -> str:
    repl = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(repl.get(c, c) for c in text)


def score_label(project: ProjectObject) -> str:
    if not project.stem_presence:
        return "not scored"
    return f"{project.stem_presence.score}/100 {project.stem_presence.band.replace('_', ' ')}"


def sectioned(projects: list[ProjectObject]) -> dict[str, list[ProjectObject]]:
    grouped = {section: [] for section in SECTION_ORDER}
    for p in projects:
        grouped.setdefault(p.cv_section, []).append(p)
    return grouped


def write_current_projects(projects: list[ProjectObject]) -> None:
    lines = ["% Auto-generated by scripts/stem_cv_curator.py.", "% Edit data/pipeline_repos.json or upstream README/status surfaces rather than hand-editing this file.", "\\section*{Current Project Register}"]
    for section, entries in sectioned(projects).items():
        if not entries:
            continue
        lines += [f"\\subsection*{{{tex_escape(SECTION_LABELS[section])}}}", "\\begin{itemize}"]
        for p in entries:
            prefix = "Discovered intake: " if not p.curated else ""
            score = f" STEM presence: {score_label(p)}."
            lines.append(f"    \\item \\textbf{{{tex_escape(p.title)}:}} {tex_escape(prefix + p.public_summary + score)}")
        lines += ["\\end{itemize}", ""]
    lines += ["\\section*{Selected Project Outputs}", "\\begin{itemize}", "    \\item \\textbf{Machine-learning workflow:} ML lab and best-practices repositories are first-class STEM CV objects with source-aware claim gates.", "    \\item \\textbf{Recursive repository scan:} active public repositories are scanned and carried forward as curated or intake-stage objects after public-release filtering.", "\\end{itemize}", ""]
    CV_PROJECTS_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_research_board(projects: list[ProjectObject]) -> None:
    lines = ["% Auto-generated by scripts/stem_cv_curator.py.", "\\section*{Research Storyboard}", "This portfolio is organized around careful, reproducible use of public-health, infrastructure, environmental, administrative, longitudinal, biomedical, machine-learning, and public-history data after public-release filtering.", "", "\\section*{Current Project Board}"]
    for section, entries in sectioned(projects).items():
        if not entries:
            continue
        lines.append(f"\\subsection*{{{tex_escape(SECTION_LABELS[section])}}}")
        for p in entries:
            needs = f"{p.near_term_needs} STEM presence: {score_label(p)}."
            lines.append(f"\\project{{{tex_escape(p.title)}}}{{{tex_escape(p.maturity.replace('_', ' '))}}}{{{tex_escape(p.public_summary)}}}{{{tex_escape(needs)}}}")
            lines.append("")
    RESEARCH_BOARD_TEX_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_research_status(projects: list[ProjectObject]) -> None:
    lines = ["# Research Status", "", "Public-facing overview generated by the STEM CV Curator object engine after public-release filtering.", "", "## Current project board", ""]
    for section, entries in sectioned(projects).items():
        if not entries:
            continue
        lines += [f"### {SECTION_LABELS[section]}", ""]
        for p in entries:
            marker = " _(recursive-scan intake)_" if not p.curated else ""
            lines += [
                f"#### {p.title} - {p.maturity.replace('_', ' ')}{marker}",
                "",
                f"**Current output:** {p.public_summary}  ",
                f"**Near-term needs:** {p.near_term_needs}  ",
                f"**STEM presence:** {score_label(p)}",
                "",
            ]
    lines += ["## Immediate major needs", "", "- Keep recursive public repository scanning active inside the public CV workflow.", "- Promote discovered intake repositories into curated manifest entries only after public-release review.", "- Keep ML project claims tied to source manifests, model cards, benchmark targets, validation gates, and STEM presence scoring.", "- Keep blocked or restricted project families out of all public CV, source-ledger, and research-status outputs.", ""]
    RESEARCH_STATUS_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_ledgers(projects: list[ProjectObject], blocked_records: list[BlockedProjectRecord]) -> None:
    source_lines = ["# Living CV Source Ledger", "", f"Last generated: {now_utc()}", "", "| Project | Repository | Source file | Available | Heading/status observed | Note |", "|---|---|---|---|---|---|"]
    for p in projects:
        for s in p.source_surfaces:
            observed = s.status_line or s.heading or ""
            note = s.note or ""
            source_lines.append(f"| {p.title.replace('|', '/')} | `{p.repository.repo_full_name}` | `{s.source_path}` | {'yes' if s.available else 'no'} | {observed.replace('|', '/')} | {note.replace('|', '/')} |")
    SOURCE_LEDGER_PATH.write_text("\n".join(source_lines) + "\n", encoding="utf-8")

    scan_lines = ["# Living CV Repository Scan", "", f"Last generated: {now_utc()}", "", f"Total active public project objects: {len(projects)}", f"Blocked release-control records: {len(blocked_records)}", f"Curated objects: {sum(1 for p in projects if p.curated)}", f"Recursive-scan intake objects: {sum(1 for p in projects if not p.curated)}", "", "| Project | Repository | Section | Maturity | STEM presence | Curated |", "|---|---|---|---|---|---|"]
    for p in projects:
        scan_lines.append(f"| {p.title.replace('|', '/')} | `{p.repository.repo_full_name}` | {p.cv_section} | {p.maturity} | {score_label(p)} | {'yes' if p.curated else 'no'} |")
    REPO_SCAN_PATH.write_text("\n".join(scan_lines) + "\n", encoding="utf-8")

    blocked_lines = ["# Blocked Release Ledger", "", f"Last generated: {now_utc()}", "", "This ledger records counts and non-sensitive identifiers for manifest entries excluded from public CV outputs.", "", "| Record | Release state | Reason | Curated |", "|---|---|---|---|"]
    for record in blocked_records:
        blocked_lines.append(f"| `{record.project_id}` | {record.public_release} | {record.release_reason} | {'yes' if record.curated else 'no'} |")
    BLOCKED_RELEASE_LEDGER_PATH.write_text("\n".join(blocked_lines) + "\n", encoding="utf-8")


def write_objects(projects: list[ProjectObject], claims: list[ClaimObject], blocked_records: list[BlockedProjectRecord]) -> None:
    payload = {
        "schema": "stem-cv-curator/v0.3",
        "run": {
            "run_time": now_utc(),
            "trigger": TRIGGER,
            "scanned_repositories": len(projects),
            "active_project_objects": len(projects),
            "blocked_release_records": len(blocked_records),
        },
        "repositories": [asdict(p.repository) for p in projects],
        "projects": [asdict(p) for p in projects],
        "blocked_release_records": [asdict(record) for record in blocked_records],
        "claims": [asdict(c) for c in claims],
        "sections": [{"section_id": s, "title": SECTION_LABELS[s], "projects": [p.project_id for p in projects if p.cv_section == s]} for s in SECTION_ORDER if any(p.cv_section == s for p in projects)],
        "render_targets": [
            {"target_id": "academic_cv_public", "output_type": "academic_cv", "included_sections": SECTION_ORDER},
            {"target_id": "one_page_profile_public", "output_type": "one_page_profile", "included_sections": ["machine_learning", "public_health", "biomedical_data", "methods"], "max_pages": 1},
            {"target_id": "research_status_public", "output_type": "research_status", "included_sections": SECTION_ORDER},
        ],
    }
    OBJECTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    manifest = load_manifest()
    projects = build_projects(manifest)
    blocked_records = build_blocked_records(manifest)
    claims = build_claims(projects)
    write_current_projects(projects)
    write_research_board(projects)
    write_research_status(projects)
    write_ledgers(projects, blocked_records)
    write_objects(projects, claims, blocked_records)
    print(f"STEM CV Curator generated {len(projects)} project objects and {len(blocked_records)} blocked release records for owner {OWNER_OVERRIDE or manifest.get('scan', {}).get('owner', 'pskeffington')}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
