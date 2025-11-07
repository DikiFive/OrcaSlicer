# Change Proposal: Fix LK10/LK10 Plus Movement Limits

## Why
- Current LONGER LK10 and LK10 Plus presets inherit movement limits from generic defaults that do not reflect the verified machine capabilities.
- The mismatch causes either aggressive accelerations that introduce artifacts or conservative limits that slow prints.

## What Changes
- Centralize the shared LONGER movement envelope (speeds, accelerations, retract/deretract 35 mm/s) in `resources/profiles/LONGER/machine/fdm_machine_common.json`.
- Keep LK10 Plus variants aligned with the common values while supplying their dedicated start G-code.
- Override LK10 variants with their specific Z speed and higher accelerations, plus LK10 start G-code, across all nozzle sizes.
- Update OpenSpec deltas for `lk10.movement` and `lk10plus.movement` to document the intended settings and start G-code tokens.

## Impact
- Specs: `openspec/specs/lk10.movement/spec.md`, `openspec/specs/lk10plus.movement/spec.md`.
- Profiles: `resources/profiles/LONGER/machine/LONGER LK10 (*.json)`, `resources/profiles/LONGER/machine/LONGER LK10 Plus (*.json)`, `resources/profiles/LONGER/machine/fdm_machine_common.json`.
- No application code changes; data-only preset updates.

## Scope
- Profiles only (JSON):
  - resources/profiles/LONGER/machine/
    - fdm_machine_common.json
    - LONGER LK10 (0.2|0.4|0.6|0.8 nozzle).json
    - LONGER LK10 Plus (0.2|0.4|0.6|0.8 nozzle).json
- Keys affected:
  - machine_max_speed_{x,y,z,e}
  - machine_max_acceleration_{x,y,z,e}
  - machine_max_acceleration_{extruding,retracting,travel}
  - retraction_speed, deretraction_speed
  - machine_start_gcode (per-model variant)

## Out of Scope
- Non-movement parameters (extrusion, temperatures, jerk/PA, etc.)

## Acceptance Criteria
- LK10 Plus presets inherit common values:
  - Speeds (mm/s): X=500, Y=500, Z=20, E=60
  - Accelerations (mm/s²): X=7000, Y=7000, Z=300, E=5000
  - Extruding/Retraction/Travel (mm/s²): 7000/7000/7000
- LK10 presets override movement values per model:
  - Speeds (mm/s): X=500, Y=500, Z=12, E=60
  - Accelerations (mm/s²): X=10000, Y=10000, Z=500, E=5000
  - Extruding/Retraction/Travel (mm/s²): 10000/10000/10000
- JSON syntax valid; application starts and loads these presets without schema warnings.
- No unintended changes to unrelated machines.

## Risks & Mitigations
- Risk: Changing common profile by mistake. Mitigation: Only override in the eight machine files.
- Risk: Value format inconsistency. Mitigation: Use array-of-string style consistent with existing profiles.

## Rollout
- Ship as part of preset update. No migration script required.