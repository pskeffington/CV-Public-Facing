#!/usr/bin/env bash
set -euo pipefail

# Public package consistency gate.
# This protects the public-facing CV package from stale hand-written sections,
# missing shared includes, incomplete project registers, and unsorted publication
# status buckets. It is intentionally read-only and must not create commits,
# dispatch workflows, or mutate tracked source files.

status=0

require_file() {
  local file="$1"
  if [[ ! -f "${file}" ]]; then
    echo "Missing required public package file: ${file}" >&2
    status=1
  fi
}

require_contains() {
  local file="$1"
  local pattern="$2"
  if [[ ! -f "${file}" ]]; then
    echo "Cannot inspect missing file: ${file}" >&2
    status=1
    return
  fi
  if ! grep -Fq -- "${pattern}" "${file}"; then
    echo "Missing required pattern in ${file}: ${pattern}" >&2
    status=1
  fi
}

require_absent_in_sources() {
  local pattern="$1"
  local match_file
  match_file="$(mktemp)"
  if grep -RIn \
    --include='*.tex' \
    --include='*.md' \
    --exclude-dir=.git \
    --exclude-dir=documents \
    -- "${pattern}" cv research >"${match_file}"; then
    echo "Stale/disallowed source pattern found: ${pattern}" >&2
    cat "${match_file}" >&2
    rm -f "${match_file}"
    status=1
    return
  fi
  rm -f "${match_file}"
}

require_file "cv/academic_cv_public.tex"
require_file "cv/one_page_profile_public.tex"
require_file "cv/public_upload_cv.tex"
require_file "cv/current_projects_public.tex"
require_file "cv/publication_pipeline_public.tex"
require_file "research/research_status.tex"
require_file "research/RESEARCH_STATUS.md"
require_file "scripts/check_public_sanitization.sh"
require_file "scripts/check_index_safe_upload.sh"
require_file "scripts/check_public_release_guard.py"

# Shared source must drive full CV outputs.
require_contains "cv/academic_cv_public.tex" "\\input{current_projects_public}"
require_contains "cv/academic_cv_public.tex" "\\input{publication_pipeline_public}"
require_contains "cv/public_upload_cv.tex" "\\input{current_projects_public}"
require_contains "cv/public_upload_cv.tex" "\\input{publication_pipeline_public}"
require_contains "research/research_status.tex" "\\input{../cv/publication_pipeline_public}"

# One-page profile is compressed, but must still expose publication status.
require_contains "cv/one_page_profile_public.tex" "Peer Review and Publication Pipeline"
require_contains "cv/one_page_profile_public.tex" "Currently submitted / under peer review"
require_contains "cv/one_page_profile_public.tex" "Active manuscript preparation"
require_contains "cv/one_page_profile_public.tex" "Validation-gated before submission"

# Full project register must be populated with public-allowlist entries only.
for project in \
  "Life-course data, family economics, and fertility" \
  "Rural water, wastewater, and infrastructure health risk" \
  "Humanitarian WASH and health-system disruption" \
  "Haiti Nippes public-health and infrastructure assessment" \
  "Medical-signal noise reduction" \
  "PET noise and radiomics robustness" \
  "Cancer end-of-life typologies" \
  "Public-health emergency preparedness and practicum reporting" \
  "Public-health practicum report" \
  "Catholic archive and public-history indexing"; do
  require_contains "cv/current_projects_public.tex" "${project}"
  require_contains "research/RESEARCH_STATUS.md" "${project}"
done

# Publication sorting must be present in the shared LaTeX source that feeds output PDFs.
for bucket in \
  "Currently submitted / under peer review" \
  "Publication-ready or print-ready" \
  "Active manuscript preparation" \
  "Validation-gated before submission"; do
  require_contains "cv/publication_pipeline_public.tex" "${bucket}"
done

# Old hand-written four-project block must not return in document sources.
require_absent_in_sources "Research Interests and Current Projects"

# Existing sanitizers and release guard remain part of preflight.
python3 scripts/check_public_release_guard.py
bash scripts/check_public_sanitization.sh
bash scripts/check_index_safe_upload.sh cv/public_upload_cv.tex

if [[ "${status}" -ne 0 ]]; then
  echo "Public package preflight failed." >&2
  exit "${status}"
fi

echo "Public package preflight passed."
