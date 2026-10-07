#!/usr/bin/env python3
"""Stub extractor for chapter mapping. Uses hand-curated data/chapter_mapping.yaml."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    mapping = ROOT / "data" / "chapter_mapping.yaml"
    if not mapping.exists():
        print(f"ERROR: {mapping} missing", file=sys.stderr)
        return 1
    print("chapter_mapping.yaml present; no extraction needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())