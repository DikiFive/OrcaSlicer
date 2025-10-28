# Change Proposal: Fix LONGER LK10/LK10 Plus host_type validation failure

- change-id: 2025-10-28-fix-longer-host-type
- owner: presets
- status: proposed
- summary: Remove invalid `host_type: klipper` from LONGER LK10 and LK10 Plus machine profiles to pass CI profile validation.

## Context
The CI job "Check profiles" fails with:

> Invalid value provided for parameter host_type: klipper

`host_type` is an enum defined in `src/libslic3r/PrintConfig.cpp` and does not include `klipper`. Existing Klipper-based machine profiles (e.g., Voron, TwoTrees) omit `host_type` entirely and only set `gcode_flavor: klipper`.

## Approach
- Keep changes minimal and data-only. Remove `host_type` from the eight LONGER LK10/LK10 Plus machine JSONs; leave `gcode_flavor: klipper` intact.
- No schema/code changes required.

## Risks
- None; `host_type` is optional and commonly absent for Klipper machines. No user-facing behavior changes beyond fixing validation.

## Validation
- Static check: ensured `host_type` enum does not include `klipper` and surveyed other Klipper profiles behavior.
- CI: Expect the "Check profiles" job to pass after removal.
