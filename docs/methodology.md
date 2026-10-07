# Methodology

## Extracting persistence_mode

| PDF phrase | persistence_mode |
|---|---|
| "saved automatically" | auto_save |
| "saved by AT&W" / "save with AT&W" | explicit_save |
| "volatile" / "not saved" | volatile |
| "factory locked" / "read-only" | factory_locked |
| "saved in profile 0/1" | profile_specific |
| "saved only if X" | conditional |
| no mention | unknown |
| action command (AT&W, ATZ, AT&F, AT&V) | momentary_action |

## Power-loss behaviour

- auto_save / explicit_save / profile_specific / factory_locked → retained
- volatile → lost
- momentary_action → not_applicable
- unknown → unknown

## reset_behavior / factory_reset_behavior

- "reset by ATZ" → reset_to_default
- "reset to profile by ATZ" → reset_to_profile
- "reset by AT&F" → reset_to_factory_default
- not mentioned → unknown

## page_hint decision table

| Situation | page_hint |
|---|---|
| Page number explicitly printed in PDF | use it |
| Page derivable from section header | use it |
| Not determinable | PAGE_UNSET (null in YAML) |

## MAX_PERSISTENCE_PER_HEADER

Set to 256 based on the estimated maximum number of parameters in the
largest header (Chapter 3/4 of the AT Manual). This leaves ample headroom.

## at_3gpp_27007 / at_3gpp_27005 split

Both chapters share `data/at_3gpp.yaml` and `include/.../at_3gpp.hpp`.
Each entry's `category` distinguishes the source chapter, and
`source_section` must include the exact chapter number (3 or 4).

## Ambiguity resolution

### G1 — unknown persistence behaviour
`persistence_mode: unknown`, notes: "behavior not documented in PDF".
No guessing.

### G2 — conditional persistence
`persistence_mode: conditional`, condition described in notes.

### G3 — different behaviour in profile 0 vs 1
Two separate PersistenceEntry rows with different profile_number.

### G4 — factory-locked parameter
`persistence_mode: factory_locked`, `is_factory_locked: true`.

### G5 — parameter requires reboot
`requires_reboot: true` only when explicitly stated in PDF.

### G6 — NVRAM address specified
`nvram_address` filled only when explicitly stated in PDF.

### G7 — action commands (AT&W, ATZ, AT&F, AT&V)
- Only the base form is registered as a PersistenceEntry.
- Numeric derivatives are described in notes.
- parameter_name: `profile` for AT&W/ATZ, `factory_defaults` for AT&F,
  `configuration_view` for AT&V.
- persistence_mode: momentary_action.
- profile_number: null, save_command: "", save_scope: "not_applicable".
- power_loss/reset/factory_reset: "not_applicable".
- is_volatile: false, is_factory_locked: false.