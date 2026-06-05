#!/usr/bin/env python3
"""Build a public-safe CV package for a selected job object.

This script intentionally performs light public-safe packaging only. It does not
pull private application packets. It reads public-safe job rendering hints from
`data/job_cv_objects.json`, copies the neutral public package artifacts produced
by `make public-package`, and writes a small manifest/brief for the selected job.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "job_cv_objects.json"
DOCUMENTS_DIR = ROOT / "documents"
OUT_ROOT = ROOT / "dist" / "job_cv_packages"

EXPECTED_PUBLIC_DOCS = [
    "Paul_A_Skeffington_Academic_CV_Public.pdf",
    "Paul_A_Skeffington_One_Page_Profile_Public.pdf",
    "Index_Safe_Public_Upload_CV.pdf",
    "Paul_A_Skeffington_Research_Status_Public.pdf",
]


class BuildError(Exception):
    """Raised when the requested public-safe job CV package cannot be built."""


def slugify(value: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    while "__" in safe:
        safe = safe.replace("__", "_")
    return safe.strip("_") or "job_cv_package"


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise BuildError(f"missing registry: {REGISTRY_PATH.relative_to(ROOT)}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def select_job_object(registry: dict[str, Any], job_object_id: str) -> dict[str, Any]:
    objects = registry.get("job_objects", {})
    if job_object_id not in objects:
        available = ", ".join(sorted(objects))
        raise BuildError(f"unknown job object '{job_object_id}'. Available: {available}")
    selected = dict(objects[job_object_id])
    selected["job_object_id"] = job_object_id
    return selected


def ensure_public_docs() -> None:
    missing = [name for name in EXPECTED_PUBLIC_DOCS if not (DOCUMENTS_DIR / name).exists()]
    if missing:
        raise BuildError("missing public package documents: " + ", ".join(missing))


def write_job_brief(out_dir: Path, job_object: dict[str, Any]) -> Path:
    lines: list[str] = []
    lines.append(f"# Public-Safe CV Package - {job_object['label']}")
    lines.append("")
    lines.append("## Role posture")
    lines.append("")
    lines.append(job_object["profile_emphasis"])
    lines.append("")
    lines.append("## Public-safe focus")
    lines.append("")
    for item in job_object.get("public_safe_focus", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Tailoring notes")
    lines.append("")
    lines.append(job_object.get("tailoring_notes", "Use neutral public-safe package."))
    lines.append("")
    lines.append("## Exclusions")
    lines.append("")
    for item in job_object.get("exclusions", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Package boundary")
    lines.append("")
    lines.append(
        "This artifact is public-safe packaging guidance. It does not import private job packets, "
        "private source records, sensitive operational details, or unsupported role claims."
    )
    lines.append("")
    path = out_dir / "PUBLIC_SAFE_JOB_BRIEF.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build(job_object_id: str) -> dict[str, Any]:
    registry = load_registry()
    job_object = select_job_object(registry, job_object_id)
    ensure_public_docs()

    output_slug = slugify(job_object.get("output_slug", job_object_id))
    out_dir = OUT_ROOT / output_slug
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for name in EXPECTED_PUBLIC_DOCS:
        src = DOCUMENTS_DIR / name
        dst = out_dir / name
        shutil.copy2(src, dst)
        copied.append(str(dst.relative_to(ROOT)))

    brief_path = write_job_brief(out_dir, job_object)

    manifest = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "job_object_id": job_object_id,
        "label": job_object["label"],
        "role_family": job_object.get("role_family"),
        "output_dir": str(out_dir.relative_to(ROOT)),
        "public_documents": copied,
        "brief": str(brief_path.relative_to(ROOT)),
        "boundary": "public-safe package only; no private job packet import",
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str]) -> None:
    job_object_id = argv[1] if len(argv) > 1 else "neutral"
    print(json.dumps(build(job_object_id), indent=2))


if __name__ == "__main__":
    try:
        main(sys.argv)
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
