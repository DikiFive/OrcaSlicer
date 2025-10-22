# Tasks: LONGER LK10 / LK10 Pro Profiles

Branch: 001-longer-lk10-profiles | Spec: specs/001-longer-lk10-profiles/spec.md | Plan: specs/001-longer-lk10-profiles/plan.md

Note: Tasks are organized by phase and user story. Follow checklist format. Mark [P] for safe parallel tasks.

## Phase 1 — Setup

- [X] T001 Ensure feature branch active in repository root (docs reference) at specs/001-longer-lk10-profiles/plan.md
- [X] T002 Verify vendor directory exists and is correct at resources/profiles/LONGER/
- [X] T003 Audit naming consistency (file name == JSON name) across LONGER profiles at resources/profiles/LONGER/

## Phase 2 — Foundational (blocking)

- [X] T004 Ensure vendor index completeness (machine_model_list/machine_list/process_list/filament_list) at resources/profiles/LONGER.json
- [X] T005 Validate inherits chains for models/variants/process (no duplication) at resources/profiles/LONGER/
- [X] T006 Confirm host_type and gcode_flavor both set to klipper in variants at resources/profiles/LONGER/machine/
- [X] T007 Align printable_area/printable_height with spec (220/330) at resources/profiles/LONGER/machine/

## Phase 3 — User Story 1: 选择 LONGER 打印机并加载预设 (P1)
Goal: 用户能选择 LK10/LK10 Pro（0.4），看到匹配耗材/工艺，并成功切片（含 Start/End 策略与清线）。
Independent Test: 参见 spec.md 的 US1；quickstart.md 步骤可复用。

- [X] T008 [US1] Ensure default_print_profile set to variant at resources/profiles/LONGER/machine/LONGER LK10 (0.4 nozzle).json
- [X] T009 [US1] Ensure default_print_profile set to variant at resources/profiles/LONGER/machine/LONGER LK10 Pro (0.4 nozzle).json
- [X] T010 [US1] Ensure default_filament_profile includes "Generic PLA @System" at resources/profiles/LONGER/machine/LONGER LK10 (0.4 nozzle).json
- [X] T011 [US1] Ensure default_filament_profile includes "Generic PLA @System" at resources/profiles/LONGER/machine/LONGER LK10 Pro (0.4 nozzle).json
- [X] T012 [P] [US1] Ensure variant nozzle_diameter single-value array ["0.4"] at resources/profiles/LONGER/machine/LONGER LK10 (0.4 nozzle).json
- [X] T013 [P] [US1] Ensure variant nozzle_diameter single-value array ["0.4"] at resources/profiles/LONGER/machine/LONGER LK10 Pro (0.4 nozzle).json
- [X] T014 [US1] Bind process compatible_printers to LK10 0.4 variant at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 (0.4 nozzle).json
- [X] T015 [US1] Bind process compatible_printers to LK10 Pro 0.4 variant at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 Pro (0.4 nozzle).json
- [X] T016 [US1] Implement Start G-code macro call (START_PRINT with parameters) at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 (0.4 nozzle).json
- [X] T017 [US1] Implement Start G-code macro call (START_PRINT with parameters) at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 Pro (0.4 nozzle).json
- [X] T018 [US1] Add unified priming/line segment within safe bounds at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 (0.4 nozzle).json
- [X] T019 [US1] Add unified priming/line segment within safe bounds at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 Pro (0.4 nozzle).json
- [X] T020 [US1] Implement End G-code macro call (END_PRINT) at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 (0.4 nozzle).json
- [X] T021 [US1] Implement End G-code macro call (END_PRINT) at resources/profiles/LONGER/process/0.20mm Standard @LONGER LK10 Pro (0.4 nozzle).json
- [X] T022 [P] [US1] Reindex new/updated processes into vendor index at resources/profiles/LONGER.json
- [ ] T023 [US1] Smoke test: select printer → defaults preselected → slice cube per quickstart at specs/001-longer-lk10-profiles/quickstart.md

## Phase 4 — User Story 2: 兼容性与命名校验 (P2)
Goal: 通过官方验证器与 Python 检查，0 错误。
Independent Test: 参见 spec.md 的 US2；quickstart.md 步骤可复用。

- [ ] T024 [US2] Run OrcaSlicer_profile_validator and capture output at tools/OrcaSlicer_profile_validator
- [X] T025 [US2] Run extra checker script and capture output at scripts/orca_extra_profile_check.py (0 errors, 0 warnings)
- [X] T025 [US2] Run extra checker script and capture output at scripts/orca_extra_profile_check.py (see .verify/longer_extra_check.log: 0 errors, 0 warnings)
- [ ] T026 [P] [US2] Fix reported issues (if any) and rerun validators at resources/profiles/LONGER/
- [X] T027 [US2] Bump vendor version/force_update appropriately at resources/profiles/LONGER.json (version=01.00.00.01, force_update=1)
- [X] T028 [US2] Update quickstart with validator outputs reference at specs/001-longer-lk10-profiles/quickstart.md

## Phase 5 — Polish & Cross-cutting

- [X] T029 Add macro setup guidance link from contract to quickstart at specs/001-longer-lk10-profiles/quickstart.md
- [X] T030 Add placeholders for bed_model/bed_texture (comment or TODO) at resources/profiles/LONGER/machine/LONGER LK10.json
- [X] T031 Add placeholders for bed_model/bed_texture (comment or TODO) at resources/profiles/LONGER/machine/LONGER LK10 Pro.json
- [X] T032 Consider adding cover images (optional) at resources/profiles/LONGER/
- [X] T033 Prepare PR description with validation summary and screenshots at specs/001-longer-lk10-profiles/plan.md

## Dependencies

- Story order: US1 → US2
- Blocking tasks: T004–T007 must complete before US1 tasks
- Post-validation bump/versioning after US1 success

## Parallel Execution Examples

- Parallel within US1: T012/T013 (nozzle arrays) can run in parallel; T016–T021 pairs per model can run in parallel once their respective files exist; T022 reindex afterwards.
- Parallel within US2: T024/T025 can run independently; T026 follows if issues found.

## Implementation Strategy (MVP first)

- MVP scope: Complete Phase 3 (US1) + minimal Foundational tasks (T004–T007) to enable slicing path; defer bed assets and PR polish to Phase 5.

## Format Validation

- All tasks follow the checklist format with TaskID, optional [P], Story labels only in story phases, and include file paths.
