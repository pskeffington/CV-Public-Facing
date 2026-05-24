#!/usr/bin/env bash
set -euo pipefail

# Public-facing repository guardrail. These terms should not appear in public source,
# docs, or generated text artifacts because they expose private location/site context.
BLOCKLIST=(
  "Plymouth"
  "Micajah"
  "Sagamore"
  "Bourne"
  "Pelham"
  "Hunters Brook"
)

status=0

while IFS= read -r -d '' file; do
  case "${file}" in
    *.tex|*.md|*.txt|*.yml|Makefile)
      for pattern in "${BLOCKLIST[@]}"; do
        if grep -Iqi -- "${pattern}" "${file}"; then
          echo "Public sanitization blocked '${pattern}' in ${file}" >&2
          status=1
        fi
      done
      ;;
  esac
done < <(find . -type f \
  ! -path './.git/*' \
  ! -path './documents/*' \
  -print0)

if [[ "${status}" -ne 0 ]]; then
  echo "Public sanitization failed." >&2
  exit "${status}"
fi

echo "Public sanitization passed."
