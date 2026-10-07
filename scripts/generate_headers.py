#!/usr/bin/env python3
"""Generate C++17 headers from YAML persistence database.

Brace-handling golden rule:
  - Single C++ brace  -> f-string with doubled braces:  f"{{"
  - Double C++ brace  -> plain string with doubled braces: "{{"
Never mix f-string and plain-string braces on the two ends of an array.

version_specific handling:
  - When *_same_as_representative is true, emit the PAD value.
  - When false, emit the explicit value from the YAML.
"""
import hashlib
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INCLUDE = ROOT / "include" / "sim800_at_persistence_modes"

# yaml_file (with extension) -> header_file
YAML_TO_HEADER = {
    "at_basic.yaml": "at_basic.hpp",
    "at_3gpp.yaml": "at_3gpp.hpp",
    "sms.yaml": "sms.hpp",
    "gprs.yaml": "gprs.hpp",
    "tcpip.yaml": "tcpip.hpp",
    "http.yaml": "http.hpp",
    "ftp.yaml": "ftp.hpp",
    "audio.yaml": "audio.hpp",
    "stk.yaml": "stk.hpp",
    "init.yaml": "init.hpp",
}

ARRAY_NAMES = {
    "at_basic": "AT_BASIC_PERSISTENCE",
    "at_3gpp": "AT_3GPP_PERSISTENCE",
    "sms": "SMS_PERSISTENCE",
    "gprs": "GPRS_PERSISTENCE",
    "tcpip": "TCPIP_PERSISTENCE",
    "http": "HTTP_PERSISTENCE",
    "ftp": "FTP_PERSISTENCE",
    "audio": "AUDIO_PERSISTENCE",
    "stk": "STK_PERSISTENCE",
    "init": "INIT_PERSISTENCE",
}

NAMESPACES = {
    "at_basic": "sim800::persistence::at_basic",
    "at_3gpp": "sim800::persistence::at_3gpp",
    "sms": "sim800::persistence::sms",
    "gprs": "sim800::persistence::gprs",
    "tcpip": "sim800::persistence::tcpip",
    "http": "sim800::persistence::http",
    "ftp": "sim800::persistence::ftp",
    "audio": "sim800::persistence::audio",
    "stk": "sim800::persistence::stk",
    "init": "sim800::persistence::init",
}

CATEGORY_ENUM = {
    "at_basic": "Category::AtBasic",
    "at_3gpp_27007": "Category::At3gpp27007",
    "at_3gpp_27005": "Category::At3gpp27005",
    "sms": "Category::Sms",
    "gprs": "Category::Gprs",
    "tcpip": "Category::Tcpip",
    "http": "Category::Http",
    "ftp": "Category::Ftp",
    "audio": "Category::Audio",
    "stk": "Category::Stk",
    "init": "Category::Init",
}

MODE_ENUM = {
    "auto_save": "PersistenceMode::AutoSave",
    "explicit_save": "PersistenceMode::ExplicitSave",
    "volatile": "PersistenceMode::Volatile",
    "factory_locked": "PersistenceMode::FactoryLocked",
    "profile_specific": "PersistenceMode::ProfileSpecific",
    "conditional": "PersistenceMode::Conditional",
    "unknown": "PersistenceMode::Unknown",
    "momentary_action": "PersistenceMode::MomentaryAction",
}

SCOPE_ENUM = {
    "profile_0": "SaveScope::Profile0",
    "profile_1": "SaveScope::Profile1",
    "both_profiles": "SaveScope::BothProfiles",
    "factory_only": "SaveScope::FactoryOnly",
    "not_applicable": "SaveScope::NotApplicable",
}

PL_ENUM = {
    "retained": "PowerLossBehavior::Retained",
    "lost": "PowerLossBehavior::Lost",
    "reset_to_default": "PowerLossBehavior::ResetToDefault",
    "unknown": "PowerLossBehavior::Unknown",
    "not_applicable": "PowerLossBehavior::NotApplicable",
}

RESET_ENUM = {
    "retained": "ResetBehavior::Retained",
    "reset_to_default": "ResetBehavior::ResetToDefault",
    "reset_to_profile": "ResetBehavior::ResetToProfile",
    "unknown": "ResetBehavior::Unknown",
    "not_applicable": "ResetBehavior::NotApplicable",
}

FR_ENUM = {
    "reset_to_factory_default": "FactoryResetBehavior::ResetToFactoryDefault",
    "retained": "FactoryResetBehavior::Retained",
    "unknown": "FactoryResetBehavior::Unknown",
    "not_applicable": "FactoryResetBehavior::NotApplicable",
}

EXTRACT_ENUM = {
    "extracted_from_table": "ExtractionStatus::ExtractedFromTable",
    "extracted_from_text": "ExtractionStatus::ExtractedFromText",
    "not_specified": "ExtractionStatus::NotSpecified",
}

PRESENCE_ENUM = {
    "present": "PresenceStatus::Present",
    "explicitly_removed": "PresenceStatus::ExplicitlyRemoved",
    "not_mentioned": "PresenceStatus::NotMentioned",
    "not_applicable": "PresenceStatus::NotApplicable",
}


def cstr(s):
    if s is None or s == "":
        return "std::string_view{}"
    esc = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{esc}"'


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def entry_hash(entries):
    payload = yaml.dump(entries, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def render_version_entry(v):
    s = []
    s.append("        VersionEntry{")
    s.append(f'            {cstr(v.get("version"))},')

    flag = v.get("persistence_mode_same_as_representative", False)
    val = "PersistenceMode::NotApplicable" if flag else MODE_ENUM[v["persistence_mode"]]
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("save_command_same_as_representative", False)
    val = "std::string_view{}" if flag else cstr(v.get("save_command"))
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("save_scope_same_as_representative", False)
    val = "SaveScope::NotApplicable" if flag else SCOPE_ENUM[v["save_scope"]]
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("profile_number_same_as_representative", False)
    if flag:
        val = "PROFILE_UNSET"
    else:
        pn = v.get("profile_number")
        val = "PROFILE_UNSET" if pn is None else str(pn)
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("power_loss_behavior_same_as_representative", False)
    val = "PowerLossBehavior::NotApplicable" if flag else PL_ENUM[v["power_loss_behavior"]]
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("reset_behavior_same_as_representative", False)
    val = "ResetBehavior::NotApplicable" if flag else RESET_ENUM[v["reset_behavior"]]
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("factory_reset_behavior_same_as_representative", False)
    val = "FactoryResetBehavior::NotApplicable" if flag else FR_ENUM[v["factory_reset_behavior"]]
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("requires_reboot_same_as_representative", False)
    val = "false" if flag else ("true" if v.get("requires_reboot") else "false")
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("is_volatile_same_as_representative", False)
    val = "false" if flag else ("true" if v.get("is_volatile") else "false")
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("is_factory_locked_same_as_representative", False)
    val = "false" if flag else ("true" if v.get("is_factory_locked") else "false")
    s.append(f'            {"true" if flag else "false"}, {val},')

    s.append(f'            {PRESENCE_ENUM[v["presence_status"]]},')
    s.append(f'            {EXTRACT_ENUM[v["extraction_status"]]},')

    flag = v.get("source_document_same_as_representative", False)
    val = "std::string_view{}" if flag else cstr(v.get("source_document"))
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("source_section_same_as_representative", False)
    val = "std::string_view{}" if flag else cstr(v.get("source_section"))
    s.append(f'            {"true" if flag else "false"}, {val},')

    flag = v.get("page_hint_same_as_representative", False)
    if flag:
        val = "PAGE_UNSET"
    else:
        ph = v.get("page_hint")
        val = "PAGE_UNSET" if ph is None else str(ph)
    s.append(f'            {"true" if flag else "false"}, {val},')

    s.append("        }")
    return "\n".join(s)


def render_entry(e):
    s = []
    s.append("    PersistenceEntry{")
    s.append(f'        {cstr(e.get("command"))},')
    s.append(f'        {cstr(e.get("parameter_name"))},')
    pn = e.get("profile_number")
    s.append(f'        {"PROFILE_UNSET" if pn is None else str(pn)},')
    s.append(f'        {CATEGORY_ENUM[e["category"]]},')
    s.append(f'        {MODE_ENUM[e["persistence_mode"]]},')
    s.append(f'        {cstr(e.get("save_command"))},')
    s.append(f'        {SCOPE_ENUM[e["save_scope"]]},')
    s.append(f'        {cstr(e.get("nvram_address"))},')
    s.append(f'        {PL_ENUM[e["power_loss_behavior"]]},')
    s.append(f'        {RESET_ENUM[e["reset_behavior"]]},')
    s.append(f'        {FR_ENUM[e["factory_reset_behavior"]]},')
    s.append(f'        {"true" if e.get("requires_reboot") else "false"},')
    s.append(f'        {"true" if e.get("is_volatile") else "false"},')
    s.append(f'        {"true" if e.get("is_factory_locked") else "false"},')
    s.append(f'        {cstr(e.get("source_document"))},')
    s.append(f'        {cstr(e.get("source_section"))},')
    s.append(f'        {EXTRACT_ENUM[e["extraction_status_latest"]]},')
    s.append(f'        {PRESENCE_ENUM[e["presence_status_latest"]]},')
    s.append(f'        {cstr(e.get("representative_version"))},')
    avail = e.get("available_in_versions", [])
    s.append("        std::array<std::string_view, MAX_AVAILABLE_VERSIONS>{{")
    for i in range(8):
        if i < len(avail):
            s.append(f'            {cstr(avail[i])},')
        else:
            s.append("            std::string_view{},")
    s.append("        }},")
    s.append(f'        {len(avail)},')
    vs = e.get("version_specific", [])
    s.append("        std::array<VersionEntry, MAX_VERSION_SPECIFIC>{{")
    for i in range(8):
        if i < len(vs):
            s.append(render_version_entry(vs[i]) + ",")
        else:
            s.append("        VERSION_ENTRY_PAD,")
    s.append("        }},")
    s.append(f'        {len(vs)},')
    ph = e.get("page_hint")
    s.append(f'        {"PAGE_UNSET" if ph is None else str(ph)},')
    s.append(f'        {cstr(e.get("notes"))}')
    s.append("    }")
    return "\n".join(s)


def generate_header(yaml_file, header_file, array_name, ns):
    """yaml_file: full filename with .yaml extension."""
    data = load_yaml(DATA / yaml_file)
    entries = data.get("entries", [])
    h = entry_hash(entries)
    ns_parts = ns.split("::")
    short_ns = ns_parts[-1]

    lines = []
    lines.append("// ============================================================")
    lines.append("// AUTO-GENERATED FILE - DO NOT EDIT MANUALLY")
    lines.append(f"// Generated from: data/{yaml_file}")
    lines.append(f"// Content hash (SHA-256 of entries section only): {h}")
    lines.append("// Generator: scripts/generate_headers.py")
    lines.append("// Generator version: 1.0.0")
    lines.append("// YAML schema version: 1.0.0")
    lines.append("// Database version: 1.0.0")
    lines.append("// To regenerate: cmake --build . --target generate")
    lines.append("// ============================================================")
    lines.append("")
    lines.append("#pragma once")
    lines.append('#include "persistence_types.hpp"')
    lines.append('#include "database_version.hpp"')
    lines.append("#include <array>")
    lines.append("#include <cstddef>")
    lines.append("#include <string_view>")
    lines.append("")
    lines.append(f"namespace {ns} {{")
    lines.append("")
    lines.append(f"inline constexpr std::array<PersistenceEntry, {len(entries)}> {array_name} = {{{{")
    for e in entries:
        lines.append(render_entry(e) + ",")
    lines.append("}};")
    lines.append("")
    lines.append(f"inline constexpr std::size_t {array_name}_COUNT = {array_name}.size();")
    lines.append(f"static_assert({array_name}_COUNT <= MAX_PERSISTENCE_PER_HEADER,")
    lines.append(f'              "{array_name} count exceeds MAX_PERSISTENCE_PER_HEADER");')
    lines.append("")
    lines.append(f"inline const PersistenceEntry* find_{short_ns}_persistence(std::string_view command,")
    lines.append("                                                         std::string_view param_name,")
    lines.append("                                                         std::uint8_t profile_number = PROFILE_UNSET) noexcept {")
    lines.append(f"    for (std::size_t i = 0; i < {array_name}_COUNT; ++i) {{")
    lines.append(f"        if ({array_name}[i].command == command")
    lines.append(f"            && {array_name}[i].parameter_name == param_name")
    lines.append(f"            && {array_name}[i].profile_number == profile_number) {{")
    lines.append(f"            return &{array_name}[i];")
    lines.append("        }")
    lines.append("    }")
    lines.append("    return nullptr;")
    lines.append("}")
    lines.append("")
    lines.append(f"}} // namespace {ns}")
    lines.append("")
    INCLUDE.mkdir(parents=True, exist_ok=True)
    (INCLUDE / header_file).write_text("\n".join(lines), encoding="utf-8")
    return len(entries)


def main():
    total = 0
    for yaml_file, header_file in YAML_TO_HEADER.items():
        yaml_path = DATA / yaml_file
        if not yaml_path.exists():
            print(f"SKIP {yaml_file}: not present")
            continue
        stem = yaml_file[:-5]  # strip .yaml
        ns_key = "at_3gpp" if "3gpp" in stem else stem
        ns = NAMESPACES[ns_key]
        arr = ARRAY_NAMES[ns_key]
        n = generate_header(yaml_file, header_file, arr, ns)
        total += n
        print(f"Generated {header_file} ({n} entries)")
    print(f"Total entries: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())