# SIM800 AT Persistence Modes

Static, offline database of **Parameter Persistence Modes** for SIMCom SIM800
AT commands (basic AT, 3GPP TS 27.007/27.005, SMS, GPRS, TCP-IP, HTTP, FTP,
Audio, STK, INIT). Each entry documents whether a parameter is auto-saved to
NVRAM, requires explicit `AT&W`, is volatile, or is factory-locked, plus its
behaviour under `ATZ`, `AT&F`, power loss, and module reset.

## Scope

This project is **only** a static database and C++17 header generator.
It does **not** send/receive AT commands, manage NVRAM, or control hardware.

Out of scope: GNSS, BT, FM commands. Action commands other than
`AT&W`, `ATZ`, `AT&F`, `AT&V` are listed in `command_inventory.yaml`
with `persistence_tracked: false`.

## Quick start

```bash
pip install pyyaml jsonschema PyMuPDF pytest
python scripts/generate_headers.py
python scripts/validate.py
cmake -B build -G "MinGW Makefiles" .
cmake --build build
ctest --test-dir build --output-on-failure
```

## Project layout

- `data/` — YAML persistence database
- `schema/` — JSON Schema definitions
- `include/sim800_at_persistence_modes/` — C++17 headers
- `scripts/` — extraction, generation, validation, reports
- `docs/` — scope, sources, methodology, reports
- `tests/` — Python and C++ tests

## License

MIT