#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-cv/public_upload_cv.tex}"

if [[ ! -f "${FILE}" ]]; then
  echo "Missing index-safe upload source: ${FILE}" >&2
  exit 1
fi

BLOCKLIST=(
  "Paul"
  "Skeffington"
  "paul@"
  "skeffington.us"
  "pskeffington"
  "GitHub"
  "Plymouth"
  "Micajah"
  "Sagamore"
  "Bourne"
  "Pelham"
  "Family Caregiver"
  "caregiver"
  "caregiving"
)

status=0

for pattern in "${BLOCKLIST[@]}"; do
  if grep -Iqi -- "${pattern}" "${FILE}"; then
    echo "Index-safe upload guard blocked '${pattern}' in ${FILE}" >&2
    status=1
  fi
done

if [[ "${status}" -ne 0 ]]; then
  echo "Index-safe upload guard failed." >&2
  exit "${status}"
fi

echo "Index-safe upload guard passed: ${FILE}"
