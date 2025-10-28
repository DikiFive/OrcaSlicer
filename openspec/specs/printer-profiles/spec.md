# printer-profiles Specification

## Purpose
Define consistent rules and validation for printer vendor presets (machines, processes, and indexes) shipped with the app.

This spec ensures that:
- User-facing names are consistent across JSON files, UI, and scripts (e.g., vendor/model/variant naming like "Vendor Model Plus").
- Vendor index files (e.g., resources/profiles/<VENDOR>.json) correctly map machine models, machine variants, and process profiles to existing files.
- Data migrations for naming changes are handled without breaking users (gracefully removing legacy files and aligning references).
- Common scripts and tools (install/sync/apply) do not hardcode stale names and remain compatible after preset changes.
- Internal identifiers and asset filenames may keep legacy tokens when needed for compatibility, as long as they are not user-visible.

Scope:
- resources/profiles/** and resources/profiles_template/** JSON data
- Naming conventions, compatible_printers, default_print_profile fields, and vendor index integrity
- Script-level compatibility where it intersects with preset naming

Out-of-scope:
- Slicer engine behavior, algorithms, and runtime logic beyond preset data loading
## Requirements
### Requirement: Longer LK10 Plus 预设命名一致性与迁移
项目 SHALL 统一使用 "Longer LK10 Plus" 作为机型显示名与目录/文件命名基准，并提供从旧名（LK10）到新名的迁移策略。

#### Scenario: 预设与目录命名统一
- **WHEN** 打包/同步系统预设（resources/profiles, resources/profiles_template）
- **THEN** 所有涉及该机型的目录与文件采用统一的 "LK10 Plus" 命名（不出现裸 "LK10" 混称）

#### Scenario: UI 可见名称正确
- **WHEN** 在应用内选择打印机预设
- **THEN** UI 显示为 "Longer LK10 Plus"，与 JSON 中的显示名字段一致

#### Scenario: 脚本与工具匹配更新
- **WHEN** 运行安装/同步脚本（install/sync/apply 系列）
- **THEN** 脚本能够正确识别并处理 "LK10 Plus"，且不会遗漏或误匹配旧名

#### Scenario: 宏模板兼容性
- **WHEN** 使用 Klipper 宏（START_PRINT/END_PRINT）
- **THEN** 改名不影响宏模板加载与执行；若宏中引用机型名，应通过变量或注释避免硬编码耦合

#### Scenario: 用户配置迁移
- **WHEN** 用户已有缓存/自定义预设仍使用旧名（LK10）
- **THEN** 通过一次性迁移（文档步骤或脚本）自动/半自动映射到 "LK10 Plus"，不丢失关键参数

### Requirement: Machine profiles MUST only use `host_type` values declared in `PrintHostType` enum
Profiles MUST NOT specify a `host_type` value outside the `PrintHostType` enum. Klipper-targeted machines MUST omit `host_type` and rely on `gcode_flavor: klipper`.

- Rationale: The profile validator enforces enum compliance to prevent invalid integrations and keeps Klipper machines consistent with existing vendors.

#### Scenario: LONGER LK10 and LK10 Plus omit unsupported host_type
- Given: The LONGER LK10 and LONGER LK10 Plus machine profiles target Klipper (`gcode_flavor: klipper`).
- And: `PrintHostType` enum does not include `klipper`.
- When: The profiles are validated by CI.
- Then: The profiles MUST NOT specify `host_type: klipper`.
- And: Validation passes when `host_type` is omitted.

