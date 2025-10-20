# Quickstart: LONGER LK10 / LK10 Pro Profiles

## Prereqs
- On branch: 001-longer-lk10-profiles
- Profiles present under resources/profiles/LONGER/* and LONGER.json indexed

## Validate
1) Run validators (Windows):
   - OrcaSlicer_profile_validator → expect 0 errors
   - scripts/orca_extra_profile_check.py → expect 0 errors
     - Command (PowerShell): D:/miniforge/Scripts/conda.exe run -p D:\miniforge --no-capture-output python scripts/orca_extra_profile_check.py --vendor LONGER --check-materials --check-filaments --check-obsolete-keys > .verify/longer_extra_check.log 2>&1
     - Log: .verify/longer_extra_check.log (Checked: 0 errors, 0 warnings)
2) Clear preset cache and restart OrcaSlicer
3) Add printer: LONGER → LK10 (0.4) or LK10 Pro (0.4)
4) Confirm defaults selected: Generic PLA @System, 0.20mm Standard @variant
5) Slice 20mm cube; check G-code:
   - Contains START_PRINT then priming line; ends with END_PRINT
6) If macros missing: switch to fallback process or accept auto fallback (per plan), observe one-time warning

## Notes
- Bed model/texture pending; add when assets ready
- For Klipper macro setup, see contracts/gcode.start_end.md

### Build and run official validator (Windows, optional)
- Build: run build_release_vs2022.bat slicer (this enables ORCA_TOOLS and builds OrcaSlicer_profile_validator)
- Run (from build folder): .\build\Release\OrcaSlicer_profile_validator.exe -p ..\resources\profiles -v LONGER -l 3
- Expected output: "Validation completed successfully" and non-zero vendor count; if errors, fix profiles then rerun.
