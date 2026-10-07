#!/usr/bin/env python3
"""Check that docs/examples are self-contained."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "docs" / "examples"

errors = []

if not EX.exists():
    print("WARN: docs/examples missing")
    sys.exit(0)

for p in EX.iterdir():
    if p.suffix == ".cpp":
        txt = p.read_text(encoding="utf-8")
        if "find_" in txt and "data/" in txt:
            errors.append(f"{p.name}: example appears to depend on live data")

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)
print("Doc examples OK")
sys.exit(0)