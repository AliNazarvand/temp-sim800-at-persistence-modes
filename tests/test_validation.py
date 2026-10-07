"""Python tests for the validation layer."""
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def test_versions_present():
    v = load(DATA / "versions.yaml")
    assert "versions" in v
    assert "latest" in v
    assert v["latest"] in [x["id"] for x in v["versions"]]


def test_category_mapping_complete():
    cm = load(DATA / "category_mapping.yaml")
    for key in ["basic_at", "at_3gpp_27007", "at_3gpp_27005", "sms",
                "gprs", "tcpip", "http", "ftp", "audio", "stk", "init"]:
        assert key in cm["categories"], f"missing category {key}"


def test_persistence_registry_has_all_modes():
    reg = load(DATA / "persistence_mode_registry.yaml")
    for mode in ["auto_save", "explicit_save", "volatile", "factory_locked",
                 "profile_specific", "conditional", "unknown", "momentary_action"]:
        assert mode in reg["modes"], f"missing mode {mode}"


def test_command_inventory_reasons():
    inv = load(DATA / "command_inventory.yaml")
    for c in inv["commands"]:
        if c["persistence_tracked"] is False:
            assert c.get("reason_not_tracked"), f"{c['command']} missing reason"
        if c["persistence_tracked"] is True:
            assert "reason_not_tracked" not in c, f"{c['command']} has unexpected reason"


def test_momentary_action_only_for_base_actions():
    allowed = {"AT&W", "ATZ", "AT&F", "AT&V"}
    for yf in ["at_basic.yaml"]:
        doc = load(DATA / yf)
        for e in doc.get("entries", []):
            if e["persistence_mode"] == "momentary_action":
                assert e["command"] in allowed, f"{e['command']} not allowed as momentary_action"


def test_no_version_reviews():
    for yf in DATA.glob("*.yaml"):
        doc = load(yf)
        txt = yf.read_text(encoding="utf-8")
        assert "version_reviews" not in txt, f"{yf.name} contains version_reviews"