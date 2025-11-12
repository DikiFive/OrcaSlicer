## ADDED Requirements

### Requirement: Unified start sequence via common inheritance
LK10 machine presets SHALL define a unified start sequence via inheritance from `fdm_machine_common.json`. Concrete machine JSON MUST NOT include a `machine_start_gcode` field.
#### Scenario: Loading any LK10 or LK10 Plus machine preset
- GIVEN a user selects any LONGER LK10 or LK10 Plus machine profile (any nozzle diameter)
- WHEN the profile is parsed
- THEN the `machine_start_gcode` field is NOT present in the concrete machine JSON
- AND it is inherited from `fdm_machine_common.json`

### Requirement: START_PRINT macro invocation with parameters
The common start sequence SHALL invoke `START_PRINT` with parameters:
`BED_TEMP=[bed_temperature_initial_layer_single] NOZZLE_TEMP=[nozzle_temperature_initial_layer] TRAVEL_SPEED=[travel_speed]`.
#### Scenario: Generating G-code for first layer
- GIVEN slicing is performed with a LK10 series machine
- WHEN the resulting G-code file begins
- THEN the first non-comment line after any header metadata is:
  START_PRINT BED_TEMP=[bed_temperature_initial_layer_single] NOZZLE_TEMP=[nozzle_temperature_initial_layer] TRAVEL_SPEED=[travel_speed]
- AND no legacy arc-cleaning or line-purge motions are emitted from presets.

### Requirement: Macro parameter names
Macro parameter names MUST match documented Klipper macros: `BED_TEMP`, `NOZZLE_TEMP`, `TRAVEL_SPEED`.
#### Scenario: Printer executes start sequence
- GIVEN the Klipper firmware has a START_PRINT macro accepting BED_TEMP, NOZZLE_TEMP, TRAVEL_SPEED
- WHEN the print starts
- THEN macro expansion sets bed & nozzle temperatures and performs travel speed initialization without preset duplication.

<!-- No REMOVED requirements in baseline; legacy behavior is captured as a Note below. -->

## Notes
- Assumes Klipper macro implements any needed homing, mesh load, purge.
- If macro coverage is insufficient, future spec may reintroduce optional additive steps.
- Legacy behavior using G2/G3 arc motions for nozzle cleaning is deprecated and moved to firmware macros.
