# Data Model

## Entities

- Vendor (LONGER)
  - Fields: name, version, force_update, machine_model_list[], machine_list[], process_list[], filament_list[]
  - Constraints: No orphan profiles; version bump on change.

- MachineModel (LK10 / LK10 Pro)
  - Fields: type=machine_model, name, inherits, printable_area (XxY), printable_height, bed_model?, bed_texture?, default_print_profile, default_filament_profile
  - Constraints: Names and paths match; host-agnostic here; inherits common brand base.

- Machine Variant (0.4)
  - Fields: type=machine, name, inherits (-> model), nozzle_diameter ["0.4"], gcode_flavor=klipper, host_type=klipper
  - Constraints: nozzle_diameter single-value array; printable_area/height match model; Start/End strategy applied via process.

- Process Preset (0.20mm Standard)
  - Fields: type=process, name, inherits (fdm_process_common), compatible_printers[], start_gcode, end_gcode
  - Constraints: Compatible list matches variants; defaults set in model; provide two variants if shipping fallback.

- Filament Preset (Generic PLA @System)
  - Fields: referenced from OrcaFilamentLibrary
  - Constraints: Prefer system library.

## Relationships
- Vendor indexes all profiles; Machine references Model; Process references Variants via compatible_printers; Model references default Process/Filament.

## Validation Rules
- Name/path equality; required fields present; inherits chain resolvable; lists indexed in vendor.json; validators pass.
