# Proposal: Unify LK10 series machine_start_gcode to common START_PRINT macro

Change-id: 003-lk10-start-gcode-unify

## Why
- Reduce duplication and drift across LK10 variants
- Centralize Klipper macro usage (START_PRINT) for maintainability
- Align with project guideline “配置为数据，无代码变更” for preset-driven behavior

## What Changes
- Remove per-machine `machine_start_gcode` overrides for LK10/LK10 Plus (all nozzle sizes)
- Define a single start sequence in `resources/profiles/LONGER/machine/fdm_machine_common.json` using a Klipper macro:
	- START_PRINT BED_TEMP=[bed_temperature_initial_layer_single] NOZZLE_TEMP=[nozzle_temperature_initial_layer] TRAVEL_SPEED=[travel_speed]

## Scope
- Affects LONGER LK10 and LK10 Plus machine presets (all nozzle sizes)
- No changes to process/filament presets or C++ sources
- End G-code remains unchanged (PRINT_END)

## Risks & Considerations
- START_PRINT macro must exist on target printers and accept the three parameters; owners should ensure Klipper macros are installed as documented.
- TRAVEL_SPEED uses the raw `travel_speed` preset value; macro should handle unit conversion if needed.

## Validation
- Profiles load without JSON errors
- Slicing G-code for any LK10* machine starts with the START_PRINT line
- Manual smoke test on one LK10 and one LK10 Plus profile

## Alternatives
- Keep per-printer overrides (rejected for duplication)
- Move to per-model macro names (not needed)
