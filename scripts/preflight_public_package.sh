#!/usr/bin/env bash
set -euo pipefail

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

require_absent_in_rendered_public_sources() {
  local pattern="$1"
  local match_file
  match_file="$(mktemp)"
  if grep -In -- "${pattern}" \
    cv/current_projects_public.tex \
    cv/publication_pipeline_public.tex \
    cv/one_page_profile_public.tex \
    research/RESEARCH_STATUS.md \
    research/generated_project_board.tex >"${match_file}"; then
    echo "Rendered public source contains disallowed pattern: ${pattern}" >&2
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
require_file "cv/public_cv_template_base.tex"
require_file "cv/current_projects_public.tex"
require_file "cv/publication_pipeline_public.tex"
require_file "research/research_status.tex"
require_file "research/RESEARCH_STATUS.md"
require_file "research/generated_project_board.tex"
require_file "scripts/check_public_sanitization.sh"
require_file "scripts/check_index_safe_upload.sh"
require_file "scripts/check_public_release_guard.py"

require_contains "cv/academic_cv_public.tex" "\\input{public_cv_template_base}"
require_contains "cv/public_upload_cv.tex" "\\input{public_cv_template_base}"
require_contains "cv/one_page_profile_public.tex" "\\input{public_cv_template_base}"
require_contains "cv/public_cv_template_base.tex" "microtype"
require_contains "cv/public_cv_template_base.tex" "cvbullets"

require_contains "cv/academic_cv_public.tex" "\\input{current_projects_public}"
require_contains "cv/academic_cv_public.tex" "\\input{publication_pipeline_public}"
require_contains "cv/public_upload_cv.tex" "\\input{current_projects_public}"
require_contains "cv/public_upload_cv.tex" "\\input{publication_pipeline_public}"
require_contains "research/research_status.tex" "\\input{../cv/publication_pipeline_public}"
require_contains "cv/academic_cv_public.tex" "Technical Skills and Methods"
require_contains "cv/public_upload_cv.tex" "Technical Skills and Methods"
require_contains "cv/one_page_profile_public.tex" "Selected Methods and Technical Skills"

# Current public package state must use evidence-bounded language.
require_contains "cv/one_page_profile_public.tex" "CART-TRACE"
require_contains "cv/one_page_profile_public.tex" "Pre-submission review"
require_contains "research/RESEARCH_STATUS.md" "Final public scholarly freeze"
require_contains "research/RESEARCH_STATUS.md" "Pre-submission review"
require_contains "research/RESEARCH_STATUS.md" "administrative access-gating extension"
require_contains "cv/publication_pipeline_public.tex" "Pre-submission review"
require_contains "research/generated_project_board.tex" "Pre-submission review"

# Public project pointers should match the current public-only allowlist.
for project in \
  "Longitudinal CAR T-cell care-trajectory reconstruction" \
  "Life-course data, family economics, and fertility" \
  "Machine-learning publication best practices" \
  "Humanitarian WASH and health-system disruption" \
  "Haiti Nippes public-health systems research" \
  "ECG signal-quality and morphology-preservation benchmarking" \
  "PET noise and radiomics robustness" \
  "Cancer end-of-life death-place typologies" \
  "WASH systems, watershed stress, and spatial equity" \
  "Catholic reliquary archival and public-history research"; do
  require_contains "data/pipeline_repos.json" "${project}"
done

# Known stale states and private-repository labels must not re-enter rendered sources.
for pattern in \
  "Under peer review" \
  "Manuscript under journal review" \
  "TransHeb" \
  "Machine-learning lab" \
  "Public-health emergency preparedness and practicum reporting" \
  "Public-health practicum report"; do
  require_absent_in_rendered_public_sources "${pattern}"
done

require_absent_in_sources "Research Interests and Current Projects"
require_absent_in_sources "Peer Review and Publication Pipeline"
require_absent_in_sources "Publication-ready or print-ready"
require_absent_in_sources "Validation-gated before submission"
require_absent_in_rendered_public_sources "STEM presence:"
require_absent_in_rendered_public_sources "core stem"
require_absent_in_rendered_public_sources "stem adjacent"
require_absent_in_rendered_public_sources "mixed or transitional"
require_absent_in_rendered_public_sources "low stem presence"

python3 scripts/check_public_release_guard.py
bash scripts/check_public_sanitization.sh
bash scripts/check_index_safe_upload.sh cv/public_upload_cv.tex

if [[ "${status}" -ne 0 ]]; then
  echo "Public package preflight failed." >&2
  exit "${status}"
fi

echo "Public package preflight passed."
