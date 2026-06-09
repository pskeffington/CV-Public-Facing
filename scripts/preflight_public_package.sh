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
    research/RESEARCH_STATUS.md \
    research/generated_project_board.tex >"${match_file}"; then
    echo "Rendered public source contains internal-only pattern: ${pattern}" >&2
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
require_file "research/generated_project_board.tex"
require_file "scripts/check_public_sanitization.sh"
require_file "scripts/check_index_safe_upload.sh"
require_file "scripts/check_public_release_guard.py"

require_contains "cv/academic_cv_public.tex" "\\input{current_projects_public}"
require_contains "cv/academic_cv_public.tex" "\\input{publication_pipeline_public}"
require_contains "cv/public_upload_cv.tex" "\\input{current_projects_public}"
require_contains "cv/public_upload_cv.tex" "\\input{publication_pipeline_public}"
require_contains "research/research_status.tex" "\\input{../cv/publication_pipeline_public}"

for profile_pattern in \
  "Publications and Manuscripts" \
  "Under peer review" \
  "In preparation" \
  "Dartmouth Scholar"; do
  require_contains "cv/one_page_profile_public.tex" "${profile_pattern}"
done

# These pointers must match the repository-object titles emitted by
# scripts/stem_cv_curator.py from data/pipeline_repos.json. Keeping the guard
# aligned with the generated object layer prevents stale legacy taxonomy strings
# from blocking otherwise valid public package builds.
for project in \
  "Life-course data, family economics, and fertility" \
  "Machine-learning publication best practices" \
  "Machine-learning lab" \
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
  require_contains "research/generated_project_board.tex" "${project}"
  require_contains "research/RESEARCH_STATUS.md" "${project}"
done

for bucket in \
  "Publications and Manuscripts" \
  "Under peer review" \
  "In preparation" \
  "Developing research projects"; do
  require_contains "cv/publication_pipeline_public.tex" "${bucket}"
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
