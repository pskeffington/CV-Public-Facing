#!/usr/bin/env python3
"""Run the STEM CV curator with the current public maturity policy."""

from __future__ import annotations

import stem_cv_curator as curator
from maturity_policy import maturity_from_status


def main() -> int:
    curator.maturity_from_status = maturity_from_status
    return curator.main()


if __name__ == "__main__":
    raise SystemExit(main())
