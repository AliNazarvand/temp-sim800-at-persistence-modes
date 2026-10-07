#!/usr/bin/env python3
"""Extract persistence modes from SIM800 AT Command Manual PDFs (best-effort).

Downloads are handled by fetch_sources.py. This script:
  1. Checks that pdfs/ exists and contains at least one AT Manual.
  2. If PyMuPDF is available, scans for AT commands and writes candidates
     to data/_extracted/*.yaml for human review.
  3. Never modifies data/*.yaml directly.
  4. Exits 0 even if PDFs are missing (no-op).
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PDF_DIR = ROOT / "pdfs"
OUT_DIR = DATA / "_extracted"

CMD_LINE_RE = re.compile(r"^\s*(AT[+&][A-Z0-9]+)\s*$", re.MULTILINE)

KEYWORD_TO_MODE = [
    (re.compile(r"saved automatically|automatically saved", re.I), "auto_save"),
    (re.compile(r"save[d]? (with|by) AT&W", re.I), "explicit_save"),
    (re.compile(r"volatile|not saved|lost on (reset|power)", re.I), "volatile"),
    (re.compile(r"factory locked|read[- ]only", re.I), "factory_locked"),
    (re.compile(r"saved in profile ?[01]", re.I), "profile_specific"),
    (re.compile(r"saved only if", re.I), "conditional"),
]


def version_from_name(name):
    m = re.search(r"V(\d+\.\d+)", name)
    return f"V{m.group(1)}" if m else None


def extract_text(page):
    try:
        return page.get_text("text")
    except Exception:
        return ""


def find_command_pages(doc):
    result = {}
    for pno in range(doc.page_count):
        text = extract_text(doc[pno])
        for match in CMD_LINE_RE.finditer(text):
            cmd = match.group(1)
            if cmd not in result:
                result[cmd] = pno + 1
    return result


def classify_around(text, cmd):
    idx = text.find(cmd)
    if idx < 0:
        return None
    window = text[max(0, idx - 200): idx + 2000]
    for pat, mode in KEYWORD_TO_MODE:
        if pat.search(window):
            return mode
    return None


def main():
    if not PDF_DIR.exists():
        print("pdfs/ not present; skipping extraction (no-op).")
        return 0

    at_manuals = [p for p in PDF_DIR.glob("*.pdf") if "AT Command Manual" in p.name]
    if not at_manuals:
        print("No AT Command Manual PDFs found in pdfs/; skipping extraction (no-op).")
        return 0

    try:
        import fitz
    except ImportError:
        print("PyMuPDF not installed; skipping extraction (no-op).")
        print("Install with: pip install PyMuPDF")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    versions = yaml.safe_load((DATA / "versions.yaml").read_text(encoding="utf-8"))
    source_by_version = {v["id"]: v["source_document"] for v in versions["versions"]}

    extracted = {}
    for pdf in at_manuals:
        version = version_from_name(pdf.name)
        if version not in source_by_version:
            continue
        print(f"Extracting from {pdf.name} ({version}) ...")
        with fitz.open(pdf) as doc:
            cmd_pages = find_command_pages(doc)
            for cmd, pno in cmd_pages.items():
                text = extract_text(doc[pno - 1])
                mode = classify_around(text, cmd)
                if mode is None:
                    continue
                extracted.setdefault(cmd, []).append({
                    "command": cmd,
                    "persistence_mode": mode,
                    "source_document": source_by_version[version],
                    "page_hint": pno,
                    "version": version,
                })

    out_file = OUT_DIR / "candidates.yaml"
    out_file.write_text(
        yaml.dump({"candidates": extracted}, sort_keys=True, allow_unicode=True),
        encoding="utf-8",
    )
    total = sum(len(v) for v in extracted.values())
    print(f"{total} candidate rows across {len(extracted)} distinct commands -> {out_file}")
    print("Review candidates and merge into data/*.yaml as appropriate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())