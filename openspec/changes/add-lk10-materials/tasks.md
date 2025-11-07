## 1. Implementation
- [x] 1.1 Mirror Elegoo's shared tuning by updating `resources/profiles/LONGER/filament/fdm_filament_common.json` and adding `fdm_filament_pla.json` / `fdm_filament_pet.json` with identical overrides.
- [x] 1.2 Duplicate `Generic PLA @Elegoo` as `Generic PLA @LONGER LK10`, updating the name, IDs, and compatible printer list to the four LONGER LK10 nozzle presets.
- [x] 1.3 Duplicate `Generic PETG @Elegoo` as `Generic PETG @LONGER LK10` with the same field adjustments as 1.2.
- [x] 1.4 Create matching PLA/PETG presets for LONGER LK10 Plus (`Generic PLA @LONGER LK10 Plus`, `Generic PETG @LONGER LK10 Plus`) with compatibility covering all four Plus nozzle presets.
- [x] 1.5 Register the shared bases and four generic files in `resources/profiles/LONGER.json`, keeping JSON formatting and ordering consistent.

## 2. Validation
- [x] 2.1 Verify `setting_id` uniqueness within `resources/profiles/LONGER/` (custom Python check) to confirm IDs and fields remain valid.
- [x] 2.2 Execute `openspec validate add-lk10-materials --strict` to verify the proposal and spec deltas pass.
