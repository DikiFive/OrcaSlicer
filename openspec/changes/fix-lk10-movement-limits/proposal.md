# Change Proposal: Fix LK10/LK10 Plus Movement Limits

## Summary
Correct movement capability parameters for LONGER LK10 and LONGER LK10 Plus machine profiles. Current presets inherit values from a generic common profile which do not match the verified machine limits. This proposal aligns the per-machine presets with the intended values (as shown in the provided reference UI screenshot) and documents the change.

## Motivation
- Prevent overly aggressive/insufficient accelerations that cause print artifacts or slowdowns.
- Ensure consistency across all nozzle variants for LK10 and LK10 Plus.
- Keep the change tightly scoped to movement capability keys; no behavioral code changes.

## Scope
- Profiles only (JSON):
  - resources/profiles/LONGER/machine/
    - LONGER LK10 (0.2|0.4|0.6|0.8 nozzle).json
    - LONGER LK10 Plus (0.2|0.4|0.6|0.8 nozzle).json
- Keys affected:
  - machine_max_speed_{x,y,z,e}
  - machine_max_acceleration_{x,y,z,e}
  - machine_max_acceleration_{extruding,retracting,travel}
  - retraction_speed, deretraction_speed

## Out of Scope
- Changes to fdm_machine_common.json
- Non-movement parameters (extrusion, temperatures, jerk/PA, etc.)

## Acceptance Criteria
- All LK10/LK10 Plus presets inherit or explicitly set the following values:
  - Speeds (mm/s): X=500, Y=500, Z=20, E=60
  - Accelerations (mm/s²): X=7000, Y=7000, Z=300, E=5000
  - Extruding/Retraction/Travel accelerations (mm/s²): 7000/7000/7000
- JSON syntax valid; application starts and loads these presets without schema warnings.
- No unintended changes to unrelated machines.

## Risks & Mitigations
- Risk: Changing common profile by mistake. Mitigation: Only override in the eight machine files.
- Risk: Value format inconsistency. Mitigation: Use array-of-string style consistent with existing profiles.

## Rollout
- Ship as part of preset update. No migration script required.