# Contributing

## Data contributions

1. Extract persistence behaviour from official SIMCom PDFs only.
2. Add entries to the appropriate `data/*.yaml` file.
3. Run `python scripts/validate.py` and fix all errors.
4. Run `python scripts/generate_headers.py` and commit generated headers.
5. Run `python scripts/generate_reports.py` and commit reports.

## Golden rules

- Never guess: use `unknown` when the PDF does not state persistence behaviour.
- Brace-handling: `{` single → f-string `{{`; `{` double → plain string `{{`.
- One topic per commit.
- Tests must be self-contained: no dependency on live data.