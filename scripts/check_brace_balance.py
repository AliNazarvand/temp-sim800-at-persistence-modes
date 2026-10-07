#!/usr/bin/env python3
"""Check brace balance in generated C++ headers (string/comment aware)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ROOT / "include" / "sim800_at_persistence_modes"


def count_braces(text):
    depth = 0
    i = 0
    n = len(text)
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    while i < n:
        c = text[i]
        nc = text[i + 1] if i + 1 < n else ""
        if in_line_comment:
            if c == "\n":
                in_line_comment = False
        elif in_block_comment:
            if c == "*" and nc == "/":
                in_block_comment = False
                i += 1
        elif in_string:
            if c == "\\":
                i += 1
            elif c == '"':
                in_string = False
        elif in_char:
            if c == "\\":
                i += 1
            elif c == "'":
                in_char = False
        else:
            if c == "/" and nc == "/":
                in_line_comment = True
                i += 1
            elif c == "/" and nc == "*":
                in_block_comment = True
                i += 1
            elif c == '"':
                in_string = True
            elif c == "'":
                in_char = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth < 0:
                    return -1
        i += 1
    return depth


def main():
    if not INCLUDE.exists():
        print("include/ dir missing; nothing to check")
        return 0
    errors = []
    checked = 0
    for hpp in sorted(INCLUDE.glob("*.hpp")):
        text = hpp.read_text(encoding="utf-8")
        depth = count_braces(text)
        checked += 1
        if depth != 0:
            errors.append(f"{hpp.name}: brace depth = {depth}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print(f"Brace balance OK ({checked} headers checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())