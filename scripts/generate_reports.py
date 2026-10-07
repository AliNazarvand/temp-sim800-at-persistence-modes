#!/usr/bin/env python3
"""Generate coverage, version-diff, persistence-matrix reports (ASCII only)."""
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

YAML_FILES = [
    "at_basic.yaml", "at_3gpp.yaml", "sms.yaml", "gprs.yaml",
    "tcpip.yaml", "http.yaml", "ftp.yaml", "audio.yaml",
    "stk.yaml", "init.yaml",
]


def load(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def all_entries():
    out = []
    for yf in YAML_FILES:
        p = DATA / yf
        if not p.exists():
            continue
        doc = load(p)
        for e in doc.get("entries", []):
            e["_file"] = yf
            out.append(e)
    return out


def report_coverage(entries):
    lines = ["# Coverage Report", "", "## Persistence mode distribution", ""]
    lines.append("| Mode | Count |")
    lines.append("|---|---|")
    for m, c in sorted(Counter(e["persistence_mode"] for e in entries).items()):
        lines.append(f"| {m} | {c} |")
    lines.append("")
    lines.append("## Save command distribution")
    lines.append("")
    lines.append("| Save command | Count |")
    lines.append("|---|---|")
    for m, c in sorted(Counter(e.get("save_command", "") or "(none)" for e in entries).items()):
        lines.append(f"| {m} | {c} |")
    lines.append("")
    lines.append("## Power-loss behaviour distribution")
    lines.append("")
    lines.append("| Behaviour | Count |")
    lines.append("|---|---|")
    for m, c in sorted(Counter(e["power_loss_behavior"] for e in entries).items()):
        lines.append(f"| {m} | {c} |")
    lines.append("")
    (DOCS / "coverage_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote coverage_report.md")


def report_sources(entries):
    lines = ["# Sources Mapping", ""]
    lines.append("| command | parameter | source_document | source_section | page |")
    lines.append("|---|---|---|---|---|")
    for e in sorted(entries, key=lambda x: (x["command"], x["parameter_name"])):
        ph = e.get("page_hint")
        lines.append(
            f"| {e['command']} | {e['parameter_name']} | "
            f"{e.get('source_document','')} | {e.get('source_section','')} | "
            f"{ph if ph is not None else ''} |"
        )
    lines.append("")
    (DOCS / "sources_mapping.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote sources_mapping.md")


def report_version_diff(entries):
    versions = load(DATA / "versions.yaml")["versions"]
    vids = [v["id"] for v in sorted(versions, key=lambda x: x["order"])]
    lines = ["# Version Diff", ""]
    header = "| command | parameter | profile | representative | " + " | ".join(vids) + " | mode |"
    sep = "|---|---|---|---|" + "|".join(["---"] * len(vids)) + "|---|"
    lines.append(header)
    lines.append(sep)
    for e in sorted(entries, key=lambda x: (x["command"], x["parameter_name"])):
        avail = set(e.get("available_in_versions", []))
        vs_map = {v["version"]: v for v in e.get("version_specific", [])}
        cells = []
        for v in vids:
            if v in vs_map and vs_map[v].get("presence_status") == "explicitly_removed":
                cells.append("-")
            elif v in avail:
                cells.append("Y")
            else:
                cells.append("?")
        pn = e.get("profile_number")
        lines.append(
            f"| {e['command']} | {e['parameter_name']} | "
            f"{pn if pn is not None else '-'} | {e.get('representative_version','')} | "
            + " | ".join(cells) + f" | {e['persistence_mode']} |"
        )
    lines.append("")
    (DOCS / "version_diff.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote version_diff.md")


def report_matrix(entries):
    lines = ["# Persistence Matrix", ""]
    lines.append("| command | parameter | profile | mode | AT&W | ATZ | AT&F | Power Loss |")
    lines.append("|---|---|---|---|---|---|---|---|")
    key = lambda x: (x["command"], x["parameter_name"],
                     x.get("profile_number") if x.get("profile_number") is not None else 255)
    for e in sorted(entries, key=key):
        mode = e["persistence_mode"]
        sc = e.get("save_command", "")
        rb = e.get("reset_behavior", "")
        fr = e.get("factory_reset_behavior", "")
        pl = e.get("power_loss_behavior", "")
        if mode == "explicit_save" and sc in ("AT&W", "AT&W0", "AT&W1"):
            atw = "Y"
        elif mode in ("volatile", "factory_locked"):
            atw = "N"
        else:
            atw = "-"
        if rb == "reset_to_profile":
            atz = "P"
        elif rb == "reset_to_default":
            atz = "N"
        else:
            atz = "-"
        if fr == "reset_to_factory_default":
            atf = "N"
        elif fr == "retained" and mode in ("auto_save", "explicit_save", "profile_specific", "factory_locked"):
            atf = "Y"
        else:
            atf = "-"
        pl_cell = {"retained": "Retained", "lost": "Lost",
                   "reset_to_default": "ResetToDefault",
                   "unknown": "Unknown", "not_applicable": "-"}.get(pl, pl)
        pn = e.get("profile_number")
        pn_cell = "-" if pn is None else str(pn)
        lines.append(
            f"| {e['command']} | {e['parameter_name']} | {pn_cell} | "
            f"{mode} | {atw} | {atz} | {atf} | {pl_cell} |"
        )
    lines.append("")
    (DOCS / "persistence_matrix.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote persistence_matrix.md")


def main():
    DOCS.mkdir(exist_ok=True)
    entries = all_entries()
    report_coverage(entries)
    report_sources(entries)
    report_version_diff(entries)
    report_matrix(entries)
    print(f"Reports generated from {len(entries)} entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())