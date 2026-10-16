#!/usr/bin/env python3
"""Custodia Latina: enforce new authored Markdown; report legacy migration."""
from __future__ import annotations
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP = {"README.md"}
SKIP_PREFIX = (".github/", "dist/", "documents/")
MARK = "<!-- lingua: la -->"
# Existing authored Markdown is migration debt, not silently considered translated.
LEGACY = {
"CONTRIBUTING.md", "Dartmouth_CV.md", "PUBLIC_MANIFEST.md",
"docs/AUTH_ECO_INTEGRATION.md", "docs/CV_PORTFOLIO_SYNC_STATUS.md",
"docs/ECOSYSTEM_ALIGNMENT.md", "docs/FIRST_TEST_JOB_CV_ACTION.md",
"docs/LIVING_CV_ACTIONS.md", "docs/PUBLIC_RELEASE_ROADMAP.md",
"docs/STEM_CITATION_VERIFICATION.md", "docs/STEM_CV_CURATOR.md",
"docs/STEM_CV_OBJECT_SCHEMA.md", "docs/STEM_EVALUATOR_LIT_REVIEW_MATRIX.md",
"docs/STEM_PAPER_EVALUATOR.md", "docs/STEM_PRESENCE_SCORE.md",
"docs/job_sync/unh_adjunct_homeland_security_public_safe.md",
"hire/FOR_HIRE_LATIN.md", "research/RESEARCH_STATUS.md",
"research/living_source_ledger.md", "docs/IMPERIUM_PROTOCOL.md",
}
def is_pointer(data: str) -> bool:
    lines = [x.strip() for x in data.splitlines() if x.strip() and not x.lstrip().startswith("#")]
    return bool(lines) and all(x.startswith(("http://", "https://", "../")) for x in lines)

def main() -> int:
    names = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True).stdout.decode().split("\0")
    errors, legacy = [], []
    for name in names:
        if not name or name in SKIP or name.startswith(SKIP_PREFIX) or not name.endswith(".md"):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        data = path.read_text(encoding="utf-8")
        if is_pointer(data):
            continue
        if MARK not in data[:256]:
            (legacy if name in LEGACY else errors).append(name)
    for name in errors:
        print(f"Latin safeguard violation: {name}: missing verified Latin declaration", file=sys.stderr)
    print(f"Latin safeguards: {len(errors)} new-file violations; {len(legacy)} legacy documents pending translation")
    if legacy:
        print("Legacy migration inventory: " + ", ".join(legacy))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
