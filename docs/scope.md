# Scope

## In scope

- Static database of Parameter Persistence Modes for SIM800 AT commands.
- Basic AT, 3GPP TS 27.007/27.005, SMS, GPRS, TCP-IP, HTTP, FTP, Audio, STK, INIT.
- Action commands `AT&W`, `ATZ`, `AT&F`, `AT&V` (base form only) as
  `momentary_action` entries.
- C++17 header generation for embedded firmware (ESP32 and others).

## Out of scope

- GNSS (`AT+CGNSINF`), BT, FM commands.
- Runtime AT command library, NVRAM manager, or profile manager.
- Action commands other than the four listed above (e.g. `ATA`, `ATH`,
  `AT+CMSS`, `AT+CMGD`, `AT+CMGW`, `AT+CHUP`). These are listed in
  `command_inventory.yaml` with `persistence_tracked: false`.
- Numeric derivatives (`AT&W0`, `AT&W1`, `ATZ0`, `ATZ1`, `AT&F0`, `AT&F1`,
  `AT&V0`, `AT&V1`) as separate entries; they are described in `notes` of
  the base entry.

## Database-only

No executable protocol code, no NVRAM storage, no hardware control.