# Contributing Data

## Steps

1. Locate the persistence statement in the official SIMCom PDF.
2. Add an entry to the matching `data/*.yaml`.
3. Use only the allowed values from `persistence_mode_registry.yaml`.
4. Run `python scripts/validate.py`.
5. Run `python scripts/generate_headers.py`.
6. Run `python scripts/generate_reports.py`.
7. Commit data + generated headers + reports.

## Rules

- Never guess persistence behaviour; use `unknown`.
- Keep `source_section` precise (chapter + section).
- For `at_3gpp.yaml`, always state chapter 3 or 4.
- Do not add numeric derivatives as separate entries.