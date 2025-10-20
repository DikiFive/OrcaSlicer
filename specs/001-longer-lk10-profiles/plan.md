# Implementation Plan: LONGER LK10 / LK10 Pro Profiles

**Branch**: `[001-longer-lk10-profiles]` | **Date**: 2025-10-20 | **Spec**: `specs/001-longer-lk10-profiles/spec.md`
**Input**: Feature specification from `/specs/001-longer-lk10-profiles/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

为 LONGER 品牌新增 LK10（220x220x220）与 LK10 Pro（330x330x330）两款机型 profiles：创建 vendor 索引，机型 model 与 0.4 变体，绑定系统默认耗材与 0.20mm Standard 工艺；采用 Klipper 宏 + 统一清线段的混合 Start/End 策略，并在宏缺失时自动降级为简化片段且提示一次性警告。所有变更需通过配置验证器与 Python 检查并完成缓存刷新冒烟测试。

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: C++17 app + JSON presets（配置为数据，无代码变更）  
**Primary Dependencies**: OrcaSlicer 预设加载与验证工具链；Klipper 宏（START_PRINT/END_PRINT）约定  
**Storage**: N/A（资源文件）  
**Testing**: OrcaSlicer_profile_validator；scripts/orca_extra_profile_check.py；人工冒烟  
**Target Platform**: 桌面（Windows/macOS/Linux），目标机型为 Klipper 主机  
**Project Type**: 单仓库桌面应用的资源配置  
**Performance Goals**: N/A（配置加载需零错误；切片可达）  
**Constraints**: 宪章门禁 I–VI；名称/路径/继承一致；无孤儿文件；反序列化兼容  
**Scale/Scope**: 新增 2 个机型 model、2 个 0.4 变体、2 个工艺、1 个 vendor 索引；床面/纹理后续补齐

## Constitution Check

*门禁：在进入 Phase 0 前必须通过；Phase 1 设计完成后需再次复核。*

基于《OrcaSlicer Constitution》的强制项：
- 命名与路径一致性：文件名与 JSON 内 name 完全一致；目录遵循 resources/profiles 层级。
- 继承优先与去重：machine/filament/process 正确使用 inherits，机型变体 nozzle_diameter 为单值数组。
- 可验证性：必须通过 OrcaSlicer_profile_validator 与 orca_extra_profile_check.py。
- 版本化：如涉及 vendor 元文件与 profile 变更，拟定 SemVer bump 与迁移说明。
- 可操作性：说明本地缓存刷新与冒烟验证策略。
- 预设系统：仅使用 TYPE_PRINT/TYPE_FILAMENT/TYPE_PRINTER，保持 Bundle 全量、UI 子集筛选；API 调用遵循 get_edited_preset/get_selected_preset 语义；若调整筛选逻辑需给出验证方案。

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: 采用单项目结构；仅在 resources/profiles 与 specs 下新增/修改文档与配置。相关真实目录：
- `resources/profiles/LONGER/*`（机型/工艺/耗材及 vendor 索引）
- `specs/001-longer-lk10-profiles/*`（规范、计划、研究、数据模型、合同、快速开始）

已生成工件：
- `research.md`（澄清结论与取舍）
- `data-model.md`（实体/字段/关系/校验）
- `contracts/*.json|md`（profile schema 与 G-code 契约）
- `quickstart.md`（验证步骤与注意事项）

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

