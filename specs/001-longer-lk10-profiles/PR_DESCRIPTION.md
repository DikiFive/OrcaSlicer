# PR Description (Validation Summary)

This PR adds LONGER LK10 and LK10 Pro system profiles with Klipper START_PRINT/END_PRINT macros, unified priming line, and brand assets.

## Validation summary
- Extra checker: scripts/orca_extra_profile_check.py → 0 errors, 0 warnings
- Vendor index version: 01.00.00.31 (force refresh applied via sync scripts)
- Covers: truecolor PNG, square outputs
  - LONGER LK10_cover.png: 168×168, ~22.0 KB
  - LONGER LK10Plus_cover.png: 168×168, ~20.5 KB
- Bed assets: 3D bed models enabled and Z-sunk to keep grid visible; silkscreen aligns per latest textures

## Manual notes
- Official OrcaSlicer_profile_validator can be run after building tools (see quickstart). Pending in CI.
- Screenshots: add printer selection and preparation page thumbnails after app restart and cache rebuild.

## Post-merge steps
- Bump version if any follow-up asset tweak
- Re-run validators and attach logs/screenshots
