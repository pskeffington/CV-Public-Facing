#!/usr/bin/env python3
"""Offline-safe checks for raw URL live verification policy."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from stem_citation_verifier import CitationVerifier  # noqa: E402


@dataclass(frozen=True)
class UrlPolicyCheckResult:
    passed: bool
    errors: list[str]

    def to_dict(self) -> dict[str, object]:
        return {"passed": self.passed, "errors": self.errors}


class UrlPolicyCheck:
    def run(self) -> UrlPolicyCheckResult:
        errors: list[str] = []
        allow_verifier = CitationVerifier(live=True, allowed_url_hosts=["example.org"])
        block_verifier = CitationVerifier(live=True, blocked_url_hosts=["blocked.example"])
        combined_verifier = CitationVerifier(live=True, allowed_url_hosts=["example.org"], blocked_url_hosts=["bad.example.org"])

        self._expect(allow_verifier._raw_url_allowed("https://example.org/paper"), True, errors, "allow exact host")
        self._expect(allow_verifier._raw_url_allowed("https://sub.example.org/paper"), True, errors, "allow subdomain")
        self._expect(allow_verifier._raw_url_allowed("https://not-example.org/paper"), False, errors, "deny off-allowlist host")
        self._expect(block_verifier._raw_url_allowed("https://blocked.example/paper"), False, errors, "block exact host")
        self._expect(block_verifier._raw_url_allowed("https://sub.blocked.example/paper"), False, errors, "block subdomain")
        self._expect(block_verifier._raw_url_allowed("https://allowed.example/paper"), True, errors, "permit when not blocked")
        self._expect(combined_verifier._raw_url_allowed("https://bad.example.org/paper"), False, errors, "block overrides allow")
        self._expect(combined_verifier._raw_url_allowed("https://good.example.org/paper"), True, errors, "allow other allowed subdomain")

        return UrlPolicyCheckResult(not errors, errors)

    @staticmethod
    def _expect(result: tuple[bool, str | None], expected: bool, errors: list[str], label: str) -> None:
        actual = result[0]
        if actual is not expected:
            errors.append(f"{label}: expected {expected}, found {actual} ({result[1]})")


def main() -> int:
    result = UrlPolicyCheck().run()
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
