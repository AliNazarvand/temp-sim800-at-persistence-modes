#!/usr/bin/env python3
"""Fetch SIM800 reference PDFs, verify checksums, update docs/sources.md.

Behavior:
  - Preserves existing docs/sources.json entries across runs.
  - If a previously-recorded SHA-256 differs from the freshly-computed one,
    exits with code 1 (checksum mismatch).
  - Only rewrites docs/sources.md based on the merged manifest.
"""
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_JSON = ROOT / "docs" / "sources.json"
SOURCES_MD = ROOT / "docs" / "sources.md"

SOURCES = [
    {"name": "SIM800 Series_AT Command Manual_V1.01.pdf", "type": "at_manual", "version": "V1.01"},
    {"name": "SIM800 Series_AT Command Manual_V1.10.pdf", "type": "at_manual", "version": "V1.10"},
    {"name": "SIM800 Series_AT Command Manual_V1.12.pdf", "type": "at_manual", "version": "V1.12"},
    {"name": "SIM800A_Hardware Design_V1.02.pdf", "type": "hardware", "version": "V1.02"},
    {"name": "SIM800C-DS_Hardware_Design_V1.01.pdf", "type": "hardware", "version": "V1.01"},
    {"name": "SIM800C_Hardware_Design_V1.02.pdf", "type": "hardware", "version": "V1.02"},
    {"name": "SIM800F_Hardware Design_V1.05.pdf", "type": "hardware", "version": "V1.05"},
    {"name": "SIM800H&SIM800L_Hardware Design_V2.02.PDF", "type": "hardware", "version": "V2.02"},
    {"name": "SIM800H_Hardware Design_V2.03.pdf", "type": "hardware", "version": "V2.03"},
    {"name": "SIM800L_Hardware Design_V1.00.pdf", "type": "hardware", "version": "V1.00"},
    {"name": "SIM800_Hardware Design_V1.09.pdf", "type": "hardware", "version": "V1.09"},
    {"name": "SIM808_Hardware Design_V1.03.pdf", "type": "hardware", "version": "V1.03"},
    {"name": "SIM868_Hardware_Design_V1.00.pdf", "type": "hardware", "version": "V1.00"},
]

BASE_URL = "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def page_count(path: Path):
    try:
        import fitz
        with fitz.open(path) as doc:
            return doc.page_count
    except Exception:
        return None


def load_prev():
    if not SOURCES_JSON.exists():
        return {}
    try:
        data = json.loads(SOURCES_JSON.read_text(encoding="utf-8"))
        return {m["name"]: m for m in data}
    except Exception:
        return {}


def write_sources_md(manifest):
    lines = ["# Sources", ""]
    lines.append("## AT Command Manuals (primary source for persistence_mode)")
    lines.append("")
    lines.append("| Document | Version | Pages | URL | SHA-256 |")
    lines.append("|---|---|---|---|---|")
    for m in manifest:
        if m["type"] != "at_manual":
            continue
        url = m.get("url") or (BASE_URL + urllib.parse.quote(m["name"]))
        lines.append(f"| {m['name']} | {m.get('version','')} | "
                     f"{m.get('pages') or '-'} | [link]({url}) | `{m.get('sha256') or '-'}` |")
    lines.append("")
    lines.append("## Hardware Design Manuals (cross-reference only)")
    lines.append("")
    lines.append("Not used as `metadata.extracted_from`.")
    lines.append("")
    lines.append("| Document | Version | Pages | URL | SHA-256 |")
    lines.append("|---|---|---|---|---|")
    for m in manifest:
        if m["type"] != "hardware":
            continue
        url = m.get("url") or (BASE_URL + urllib.parse.quote(m["name"]))
        lines.append(f"| {m['name']} | {m.get('version','')} | "
                     f"{m.get('pages') or '-'} | [link]({url}) | `{m.get('sha256') or '-'}` |")
    lines.append("")
    SOURCES_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    pdf_dir = ROOT / "pdfs"
    pdf_dir.mkdir(exist_ok=True)
    prev = load_prev()
    manifest = []
    checksum_mismatch = False

    for src in SOURCES:
        url = BASE_URL + urllib.parse.quote(src["name"])
        dest = pdf_dir / src["name"]
        if not dest.exists():
            print(f"Downloading {src['name']} ...")
            try:
                urllib.request.urlretrieve(url, dest)
            except Exception as e:
                print(f"  WARN: download failed for {src['name']}: {e}")
                # Preserve previous entry if available
                if src["name"] in prev:
                    manifest.append(prev[src["name"]])
                else:
                    manifest.append({
                        "name": src["name"], "type": src["type"],
                        "version": src.get("version"),
                        "pages": None, "sha256": None, "url": url,
                    })
                continue

        new_sha = sha256(dest) if dest.exists() else None
        if src["name"] in prev and prev[src["name"]].get("sha256") and new_sha:
            if prev[src["name"]]["sha256"] != new_sha:
                print(f"ERROR: checksum mismatch for {src['name']}")
                print(f"  expected {prev[src['name']]['sha256']}")
                print(f"  got      {new_sha}")
                checksum_mismatch = True

        manifest.append({
            "name": src["name"],
            "type": src["type"],
            "version": src.get("version"),
            "pages": page_count(dest) if dest.exists() else None,
            "sha256": new_sha,
            "url": url,
        })

    SOURCES_JSON.parent.mkdir(parents=True, exist_ok=True)
    SOURCES_JSON.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_sources_md(manifest)
    print(f"Wrote {SOURCES_JSON}")
    print(f"Wrote {SOURCES_MD}")

    if checksum_mismatch:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())