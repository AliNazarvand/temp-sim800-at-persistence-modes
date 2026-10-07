#!/usr/bin/env python3
"""Stub extractor for command inventory. Uses hand-curated data/command_inventory.yaml."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    inv = ROOT / "data" / "command_inventory.yaml"
    if not inv.exists():
        print(f"ERROR: {inv} missing", file=sys.stderr)
        return 1
    print("command_inventory.yaml present; no extraction needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())