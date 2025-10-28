# Change Proposal: Fix LONGER LK10/LK10 Plus host_type validation failure

- change-id: 2025-10-28-fix-longer-host-type
- owner: presets
- status: proposed
- summary: Remove invalid `host_type: klipper` from LONGER LK10 and LK10 Plus machine profiles to pass CI profile validation.

## Why
The CI job "Check profiles" failed with: "Invalid value provided for parameter host_type: klipper". The `host_type` setting is an enum defined in `src/libslic3r/PrintConfig.cpp` and does not include `klipper`. Other Klipper-based vendors omit `host_type` and rely solely on `gcode_flavor: klipper`. Aligning LONGER LK10 family with this convention resolves the CI failure without code changes.

## What Changes
- Data-only: Remove `host_type: klipper` from eight LONGER LK10/LK10 Plus machine JSONs; keep `gcode_flavor: klipper`.
- No schema or application code changes.

## Risks
- None. `host_type` is optional for Klipper setups and commonly omitted in existing profiles.

## Validation
- Local profile validator: PASS for vendor=LONGER and for all vendors.
- CI expectation: "Check profiles" job turns green after change is merged.
