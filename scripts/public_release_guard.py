#!/usr/bin/env python3
"""Public release guard for blocked project-family reporting.

The guard intentionally stores only normalized phrase hashes so the public
repository does not expose the blocked project-family names it protects.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

# SHA-256 hashes of lowercase normalized blocked phrases. Do not replace these
# with plain text names in this public repository.
BLOCKED_PHRASE_HASHES = frozenset({
    "cd25c925ef0d19bdccd26130a2f7585f10805ca062ae258c0400dd519945c9a2",
    "696a4a5fb0016faa39fea14084d1b68cd7e7e10634a6e7b1ca59bf8e6164a32e",
    "5aabe6e0fc76d252fa6cf1ddbbe79298da4914af6b576d46d140c616abdcd878",
    "692e6ad8e48a82feeb692d48b8362eb083cd0489747d8342d734b6b6d3d9f86a",
    "6f72aa2a1664f71b8f9357e837da6aebddbbff6861861f85a18514f4e3de0b87",
    "a3f90152dc0156d7f12266d353727cf7c381b414efa598418c746c88a83abdf9",
    "7c39d99f0e0922eed0f1ff16a2f835f15717ccf454c39581a4f0db7804f146f4",
    "9fb8b540eccd52661263b20539e80b5b011c99164a6435dffc1442204ab7a38b",
})

DEFAULT_SCAN_SUFFIXES = {
    ".json",
    ".md",
    ".tex",
    ".txt",
    ".yml",
    ".yaml",
}

DEFAULT_EXCLUDED_PARTS = {
    ".git",
    "documents",
    "__pycache__",
}


def _hash_phrase(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _tokenize(text: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", text.lower()) if token]


@dataclass(frozen=True)
class BlockedPhraseFinding:
    path: Path
    phrase_hash_prefix: str


class PublicReleaseGuard:
    """Detects blocked public-reporting phrases without storing them in cleartext."""

    def __init__(self, blocked_hashes: Iterable[str] = BLOCKED_PHRASE_HASHES) -> None:
        self.blocked_hashes = frozenset(blocked_hashes)

    def text_is_blocked(self, text: str) -> bool:
        return bool(self.find_hashes(text))

    def find_hashes(self, text: str) -> set[str]:
        tokens = _tokenize(text)
        hits: set[str] = set()
        for start in range(len(tokens)):
            for width in range(1, 5):
                phrase = " ".join(tokens[start:start + width])
                if not phrase:
                    continue
                digest = _hash_phrase(phrase)
                if digest in self.blocked_hashes:
                    hits.add(digest)
        return hits

    def path_is_excluded(self, path: Path) -> bool:
        parts = set(path.parts)
        return bool(parts & DEFAULT_EXCLUDED_PARTS)

    def iter_scannable_files(self, root: Path = ROOT) -> Iterable[Path]:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if self.path_is_excluded(path.relative_to(root)):
                continue
            if path.suffix.lower() in DEFAULT_SCAN_SUFFIXES:
                yield path

    def scan_file(self, path: Path) -> list[BlockedPhraseFinding]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return []
        return [
            BlockedPhraseFinding(path=path, phrase_hash_prefix=digest[:12])
            for digest in sorted(self.find_hashes(text))
        ]

    def scan_tree(self, root: Path = ROOT) -> list[BlockedPhraseFinding]:
        findings: list[BlockedPhraseFinding] = []
        for path in self.iter_scannable_files(root):
            findings.extend(self.scan_file(path))
        return findings
