#!/usr/bin/env python3
"""Validate SIM800 AT persistence database."""
import json
import sys
from pathlib import Path

import yaml

try:
    import jsonschema
    HAVE_JSONSCHEMA = True
except ImportError:
    HAVE_JSONSCHEMA = False

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMA = ROOT / "schema"

VALID_CATEGORIES = {
    "at_basic", "at_3gpp_27007", "at_3gpp_27005", "sms", "gprs",
    "tcpip", "http", "ftp", "audio", "stk", "init",
}
VALID_MODES = {
    "auto_save", "explicit_save", "volatile", "factory_locked",
    "profile_specific", "conditional", "unknown", "momentary_action",
}
VALID_SCOPES = {
    "profile_0", "profile_1", "both_profiles", "factory_only", "not_applicable",
}
VALID_PL = {"retained", "lost", "reset_to_default", "unknown", "not_applicable"}
VALID_RESET = {"retained", "reset_to_default", "reset_to_profile", "unknown", "not_applicable"}
VALID_FR = {"reset_to_factory_default", "retained", "unknown", "not_applicable"}
VALID_EXTRACT = {"extracted_from_table", "extracted_from_text", "not_specified"}
VALID_PRESENCE = {"present", "explicitly_removed", "not_mentioned"}

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def rewrite_refs(schema, common_defs):
    """Recursively rewrite '$ref': 'common.schema.json#/definitions/X' -> '#/definitions/X'
    and inject common definitions."""
    def walk(node):
        if isinstance(node, dict):
            new = {}
            for k, v in node.items():
                if k == "$ref" and isinstance(v, str) and v.startswith("common.schema.json#"):
                    new[k] = v.replace("common.schema.json#", "#")
                else:
                    new[k] = walk(v)
            return new
        if isinstance(node, list):
            return [walk(x) for x in node]
        return node

    rewritten = walk(schema)
    rewritten.setdefault("definitions", {})
    for k, v in common_defs.items():
        if k not in rewritten["definitions"]:
            rewritten["definitions"][k] = v
    return rewritten


def check_entry(e, fname, idx, versions_by_id):
    ctx = f"{fname}[{idx}] ({e.get('command','?')}/{e.get('parameter_name','?')})"

    for req in ["command", "parameter_name", "category", "persistence_mode",
                "save_command", "save_scope", "power_loss_behavior",
                "reset_behavior", "factory_reset_behavior",
                "source_document", "source_section",
                "extraction_status_latest", "presence_status_latest",
                "representative_version", "available_in_versions"]:
        if req not in e:
            err(f"{ctx}: missing field '{req}'")

    if e.get("category") not in VALID_CATEGORIES:
        err(f"{ctx}: invalid category {e.get('category')}")
    if e.get("persistence_mode") not in VALID_MODES:
        err(f"{ctx}: invalid persistence_mode {e.get('persistence_mode')}")
    if e.get("save_scope") not in VALID_SCOPES:
        err(f"{ctx}: invalid save_scope {e.get('save_scope')}")
    if e.get("power_loss_behavior") not in VALID_PL:
        err(f"{ctx}: invalid power_loss_behavior")
    if e.get("reset_behavior") not in VALID_RESET:
        err(f"{ctx}: invalid reset_behavior")
    if e.get("factory_reset_behavior") not in VALID_FR:
        err(f"{ctx}: invalid factory_reset_behavior")
    if e.get("extraction_status_latest") not in VALID_EXTRACT:
        err(f"{ctx}: invalid extraction_status_latest")
    if e.get("presence_status_latest") not in VALID_PRESENCE:
        err(f"{ctx}: invalid presence_status_latest")

    if not e.get("command"):
        err(f"{ctx}: empty command")
    if not e.get("parameter_name"):
        err(f"{ctx}: empty parameter_name")
    if not e.get("representative_version"):
        err(f"{ctx}: representative_version must not be null")

    avail = e.get("available_in_versions", [])
    if not avail:
        err(f"{ctx}: available_in_versions empty")
    if len(set(avail)) != len(avail):
        err(f"{ctx}: duplicate versions in available_in_versions")
    if avail:
        orders = [versions_by_id.get(v, {}).get("order", -1) for v in avail]
        if any(o < 0 for o in orders):
            err(f"{ctx}: available_in_versions contains unknown version id")
        if orders != sorted(orders):
            err(f"{ctx}: available_in_versions not ascending by order")

    if avail:
        rep = e.get("representative_version")
        if rep not in avail:
            err(f"{ctx}: representative_version not in available_in_versions")
        else:
            newest = max(avail, key=lambda v: versions_by_id.get(v, {}).get("order", -1))
            if rep != newest:
                err(f"{ctx}: representative_version must be newest available")

    vs = e.get("version_specific", [])
    vs_ids = [v.get("version") for v in vs]
    for vid in vs_ids:
        if vid not in avail:
            err(f"{ctx}: version_specific member {vid} not in available_in_versions")
    if len(set(vs_ids)) != len(vs_ids):
        err(f"{ctx}: duplicate versions in version_specific")
    if vs_ids:
        vs_orders = [versions_by_id.get(v, {}).get("order", -1) for v in vs_ids]
        if vs_orders != sorted(vs_orders):
            err(f"{ctx}: version_specific not ascending by order")
    if e.get("representative_version") in vs_ids:
        err(f"{ctx}: version_specific must not include representative_version")

    mode = e.get("persistence_mode")
    sc = e.get("save_command", "")
    ss = e.get("save_scope")
    if mode == "auto_save":
        if sc: err(f"{ctx}: auto_save must have empty save_command")
        if ss != "not_applicable": err(f"{ctx}: auto_save must have save_scope=not_applicable")
    elif mode == "explicit_save":
        if sc not in ("AT&W", "AT&W0", "AT&W1"):
            err(f"{ctx}: explicit_save needs AT&W/AT&W0/AT&W1 save_command")
        if ss not in ("profile_0", "profile_1", "both_profiles"):
            err(f"{ctx}: explicit_save needs profile scope")
    elif mode == "volatile":
        if sc: err(f"{ctx}: volatile must have empty save_command")
        if ss != "not_applicable": err(f"{ctx}: volatile must have save_scope=not_applicable")
    elif mode == "factory_locked":
        if sc: err(f"{ctx}: factory_locked must have empty save_command")
        if ss != "factory_only": err(f"{ctx}: factory_locked must have save_scope=factory_only")
    elif mode == "profile_specific":
        if sc: err(f"{ctx}: profile_specific must have empty save_command")
        if ss not in ("profile_0", "profile_1"): err(f"{ctx}: profile_specific needs profile_0/1")
    elif mode == "unknown":
        if sc: err(f"{ctx}: unknown must have empty save_command")
        if ss != "not_applicable": err(f"{ctx}: unknown must have save_scope=not_applicable")
    elif mode == "momentary_action":
        if sc: err(f"{ctx}: momentary_action must have empty save_command")
        if ss != "not_applicable": err(f"{ctx}: momentary_action must have save_scope=not_applicable")
    elif mode == "conditional":
        if not e.get("notes"):
            err(f"{ctx}: conditional must have notes describing the condition")

    if mode == "volatile" and not e.get("is_volatile"):
        err(f"{ctx}: volatile requires is_volatile=true")
    if mode != "volatile" and e.get("is_volatile"):
        err(f"{ctx}: is_volatile must be false unless mode=volatile")

    if mode == "factory_locked" and not e.get("is_factory_locked"):
        err(f"{ctx}: factory_locked requires is_factory_locked=true")
    if mode != "factory_locked" and e.get("is_factory_locked"):
        err(f"{ctx}: is_factory_locked must be false unless mode=factory_locked")

    pl = e.get("power_loss_behavior")
    rb = e.get("reset_behavior")
    fr = e.get("factory_reset_behavior")
    if mode == "volatile":
        if pl != "lost": err(f"{ctx}: volatile requires power_loss_behavior=lost")
        if rb != "reset_to_default": err(f"{ctx}: volatile requires reset_behavior=reset_to_default")
    elif mode in ("auto_save", "explicit_save", "profile_specific", "factory_locked"):
        if pl != "retained": err(f"{ctx}: {mode} requires power_loss_behavior=retained")
    elif mode == "momentary_action":
        if pl != "not_applicable": err(f"{ctx}: momentary_action requires power_loss=not_applicable")
        if rb != "not_applicable": err(f"{ctx}: momentary_action requires reset=not_applicable")
        if fr != "not_applicable": err(f"{ctx}: momentary_action requires factory_reset=not_applicable")

    if rb == "reset_to_factory_default":
        err(f"{ctx}: reset_behavior=reset_to_factory_default is forbidden")

    pn = e.get("profile_number")
    if ss == "profile_0" and pn != 0:
        err(f"{ctx}: save_scope=profile_0 requires profile_number=0")
    if ss == "profile_1" and pn != 1:
        err(f"{ctx}: save_scope=profile_1 requires profile_number=1")
    if ss in ("both_profiles", "factory_only", "not_applicable") and pn is not None:
        err(f"{ctx}: save_scope={ss} requires profile_number=null")
    if sc == "AT&W0" and (ss != "profile_0" or pn != 0):
        err(f"{ctx}: save_command=AT&W0 requires scope=profile_0, profile_number=0")
    if sc == "AT&W1" and (ss != "profile_1" or pn != 1):
        err(f"{ctx}: save_command=AT&W1 requires scope=profile_1, profile_number=1")
    if sc == "AT&W" and (ss != "both_profiles" or pn is not None):
        err(f"{ctx}: save_command=AT&W requires scope=both_profiles, profile_number=null")

    # Rule 19 (upgraded to error): *_same_as_representative true => PAD value
    PAD = {
        "persistence_mode": "NotApplicable",
        "save_command": "",
        "save_scope": "not_applicable",
        "profile_number": None,
        "power_loss_behavior": "not_applicable",
        "reset_behavior": "not_applicable",
        "factory_reset_behavior": "not_applicable",
        "requires_reboot": False,
        "is_volatile": False,
        "is_factory_locked": False,
        "source_document": "",
        "source_section": "",
        "page_hint": None,
    }
    for v in vs:
        vctx = f"{ctx}/version_specific[{v.get('version','?')}]"
        for field, pad in PAD.items():
            flag = f"{field}_same_as_representative"
            if v.get(flag) is True and field in v:
                if v[field] != pad:
                    err(f"{vctx}: {field} must be PAD when {flag}=true (got {v[field]!r})")
            if v.get(flag) is False and field not in v:
                # required when same_as_representative=false
                if field not in ("persistence_mode","save_command","save_scope","profile_number",
                                 "power_loss_behavior","reset_behavior","factory_reset_behavior",
                                 "requires_reboot","is_volatile","is_factory_locked",
                                 "source_document","source_section","page_hint"):
                    continue
                err(f"{vctx}: {field} required when {flag}=false")

    # Rule 31: source_document matches versions.yaml
    src = e.get("source_document")
    rep = e.get("representative_version")
    if rep and rep in versions_by_id:
        expected = versions_by_id[rep].get("source_document")
        if expected and src != expected:
            err(f"{ctx}: source_document does not match versions.yaml for {rep}")

    # Rule 32: explicitly_removed implies older representative
    if e.get("presence_status_latest") == "explicitly_removed":
        if rep and versions_by_id.get(rep, {}).get("order") == max(
                v.get("order", 0) for v in versions_by_id.values()):
            err(f"{ctx}: explicitly_removed requires older representative")


def sort_key(e):
    pn = e.get("profile_number")
    return (
        e.get("command", ""),
        e.get("parameter_name", ""),
        -1 if pn is None else pn,
    )


def main():
    if not HAVE_JSONSCHEMA:
        warn("jsonschema not installed; skipping JSON Schema validation")

    versions_path = DATA / "versions.yaml"
    if not versions_path.exists():
        err("versions.yaml missing")
        print("\n".join(errors))
        return 1
    versions = load(versions_path)
    versions_by_id = {v["id"]: v for v in versions["versions"]}

    yaml_files = [
        "at_basic.yaml", "at_3gpp.yaml", "sms.yaml", "gprs.yaml",
        "tcpip.yaml", "http.yaml", "ftp.yaml", "audio.yaml",
        "stk.yaml", "init.yaml",
    ]

    reg_path = DATA / "persistence_mode_registry.yaml"
    if reg_path.exists():
        reg = load(reg_path)
        for mode in VALID_MODES:
            if mode not in reg.get("modes", {}):
                err(f"persistence_mode_registry: missing mode '{mode}'")
        cond = reg.get("modes", {}).get("conditional", {})
        if cond:
            if cond.get("requires_save_command") or cond.get("is_persistent") or cond.get("is_factory_locked"):
                err("persistence_mode_registry: conditional must have false/false/false")

    cm_path = DATA / "category_mapping.yaml"
    category_map = {}
    if cm_path.exists():
        cm = load(cm_path)
        category_map = {k: v for k, v in cm.get("categories", {}).items()}

    allowed_momentary = {"AT&W", "ATZ", "AT&F", "AT&V"}
    forbidden_derivatives = {"AT&W0","AT&W1","ATZ0","ATZ1","AT&F0","AT&F1","AT&V0","AT&V1"}

    seen_keys = set()
    all_yaml_commands = set()
    for yf in yaml_files:
        p = DATA / yf
        if not p.exists():
            err(f"{yf} missing")
            continue
        doc = load(p)
        meta = doc.get("metadata", {})
        if not meta.get("extracted_from"):
            err(f"{yf}: metadata.extracted_from empty")
        if meta.get("database_version") != "1.0.0":
            err(f"{yf}: database_version must be 1.0.0")
        if meta.get("schema_version") != "1.0.0":
            err(f"{yf}: schema_version must be 1.0.0")

        entries = doc.get("entries", [])
        # Rule 21: entries sorted by (command, parameter_name, profile_number)
        if entries != sorted(entries, key=sort_key):
            err(f"{yf}: entries not sorted by (command, parameter_name, profile_number) (Rule 21)")

        for idx, e in enumerate(entries):
            check_entry(e, yf, idx, versions_by_id)
            key = (e.get("command"), e.get("parameter_name"), e.get("profile_number"))
            if key in seen_keys:
                err(f"{yf}[{idx}]: duplicate uniqueness key {key}")
            seen_keys.add(key)
            if e.get("persistence_mode") == "momentary_action":
                if e.get("command") not in allowed_momentary:
                    err(f"{yf}[{idx}]: momentary_action only for AT&W/ATZ/AT&F/AT&V")
            if e.get("command") in forbidden_derivatives:
                err(f"{yf}[{idx}]: numeric derivative {e.get('command')} not allowed")
            if e.get("persistence_mode") == "NotApplicable":
                err(f"{yf}[{idx}]: persistence_mode=NotApplicable forbidden")
            if e.get("presence_status_latest") == "not_applicable":
                err(f"{yf}[{idx}]: presence_status=not_applicable forbidden")
            all_yaml_commands.add(e.get("command"))
            if category_map:
                cat = e.get("category")
                for v in category_map.values():
                    if v.get("category") == cat:
                        break
                else:
                    err(f"{yf}[{idx}]: category {cat} not in category_mapping.yaml")

    # Rule 34: extracted_from union per file
    for yf in yaml_files:
        p = DATA / yf
        if not p.exists():
            continue
        doc = load(p)
        declared = set(doc.get("metadata", {}).get("extracted_from", []))
        required = set()
        for e in doc.get("entries", []):
            for vid in e.get("available_in_versions", []):
                vdoc = versions_by_id.get(vid, {}).get("source_document")
                if vdoc:
                    required.add(vdoc)
        missing = required - declared
        if missing:
            err(f"{yf}: metadata.extracted_from missing {sorted(missing)}")

    # Rule 37 + 38 (bidirectional)
    inv_path = DATA / "command_inventory.yaml"
    inventory_commands = {}
    if inv_path.exists():
        inv = load(inv_path)
        for i, c in enumerate(inv.get("commands", [])):
            inventory_commands[c.get("command")] = c
            if c.get("persistence_tracked") is False:
                if not c.get("reason_not_tracked"):
                    err(f"command_inventory[{i}]: false needs reason_not_tracked")
            if c.get("persistence_tracked") is True:
                if c.get("reason_not_tracked"):
                    err(f"command_inventory[{i}]: true must not have reason_not_tracked")
                if c.get("command") not in all_yaml_commands:
                    err(f"command_inventory[{i}]: {c.get('command')} tracked but no YAML entry")
        # Bidirectional: every YAML command must be in inventory as tracked=true
        for cmd in all_yaml_commands:
            if cmd not in inventory_commands:
                err(f"YAML command '{cmd}' missing from command_inventory.yaml")
            elif inventory_commands[cmd].get("persistence_tracked") is not True:
                err(f"YAML command '{cmd}' must have persistence_tracked: true in inventory")

    # Rule 39
    at3gpp = DATA / "at_3gpp.yaml"
    if at3gpp.exists():
        doc = load(at3gpp)
        for idx, e in enumerate(doc.get("entries", [])):
            sec = e.get("source_section", "")
            if "Chapter 3" not in sec and "Chapter 4" not in sec:
                err(f"at_3gpp.yaml[{idx}]: source_section must reference Chapter 3 or 4")

    # JSON Schema validation with rewritten $ref
    if HAVE_JSONSCHEMA:
        schema_files = {
            "at_basic.yaml": "at_basic.schema.json",
            "at_3gpp.yaml": "at_3gpp.schema.json",
            "sms.yaml": "sms.schema.json",
            "gprs.yaml": "gprs.schema.json",
            "tcpip.yaml": "tcpip.schema.json",
            "http.yaml": "http.schema.json",
            "ftp.yaml": "ftp.schema.json",
            "audio.yaml": "audio.schema.json",
            "stk.yaml": "stk.schema.json",
            "init.yaml": "init.schema.json",
        }
        common_path = SCHEMA / "common.schema.json"
        if common_path.exists():
            common = json.loads(common_path.read_text(encoding="utf-8"))
            common_defs = common.get("definitions", {})
            for yf, sf in schema_files.items():
                sp = SCHEMA / sf
                if not sp.exists():
                    continue
                schema = json.loads(sp.read_text(encoding="utf-8"))
                schema = rewrite_refs(schema, common_defs)
                data = load(DATA / yf)
                try:
                    jsonschema.validate(data, schema)
                except jsonschema.ValidationError as ve:
                    err(f"{yf}: JSON Schema violation: {ve.message} at {list(ve.path)}")
                except Exception as ex:
                    err(f"{yf}: JSON Schema error: {ex}")

    # Rule 33
    for yf in DATA.glob("*.yaml"):
        if "_extracted" in str(yf):
            continue
        txt = yf.read_text(encoding="utf-8")
        if "version_reviews" in txt:
            err(f"{yf.name}: contains 'version_reviews'")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN: {w}")
        return 1
    for w in warnings:
        print(f"WARN: {w}")
    print("Validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())