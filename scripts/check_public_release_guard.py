#!/usr/bin/env python3
"""Fail the public build if blocked project-family reporting appears."""

from __future__ import annotations

import sys

from public_release_guard import ROOT, PublicReleaseGuard


def main() -> int:
    guard = PublicReleaseGuard()
    findings = guard.scan_tree(ROOT)
    if findings:
        print("Public release guard failed.", file=sys.stderr)
        for finding in findings:
            rel = finding.path.relative_to(ROOT)
            print(f"- blocked reporting token hash {finding.phrase_hash_prefix} in {rel}", file=sys.stderr)
        return 2
    print("Public release guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
