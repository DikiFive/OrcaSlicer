# Feature Specification: 添加 LONGER 品牌 LK10 与 LK10 Pro 机型 Profiles

**Feature Branch**: `[001-longer-lk10-profiles]`  
**Created**: 2025-10-20  
**Status**: Draft  
**Input**: User description: "添加 LONGER 品牌 LK10 与 LK10 Pro 两款 i3 结构机型的 profiles（对标 Elegoo Neptune 4 Plus），先按 220x220 与 330x330 平面，打印高度待确认，按规范创建 vendor 与机型/变体并索引；缺失信息回填后续调整。"

## Clarifications

### Session 2025-10-20

- Q: 主机连接类型的默认选择是什么？ → A: Klipper（host_type=klipper）
- Q: 打印高度 printable_height 的目标值？ → A: LK10=220mm，LK10 Pro=330mm
- Q: 默认耗材与工艺绑定策略？ → A: 默认耗材 Generic PLA @System；默认工艺 0.20mm Standard @对应机型（0.4 nozzle）
- Q: Start/End G-code 策略（Klipper 场景）？ → A: 混合：调用 Klipper 宏（START_PRINT/END_PRINT）并在切片端附加统一清线/引线段。
- Q: 若未配置 START_PRINT/END_PRINT 宏的降级策略？ → A: 自动降级到简化 Start/End 片段，并显示一次性警告。

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - 选择 LONGER 打印机并加载预设 (Priority: P1)

用户在设备向导中选择 LONGER → 选择 LK10 或 LK10 Pro → 看到匹配的耗材与工艺列表可用并成功切片。

**Why this priority**: 这是最小可用路径，证明 profiles 可正确加载与使用。

**Independent Test**: 仅安装新增 profiles，清缓存并重启后，能选择 LONGER 机型并成功切片测试模型（如 20mm 方块）。

**Acceptance Scenarios**:

1. Given 已安装 profiles，When 在 UI 中选择 LONGER LK10 0.4 喷嘴，Then 列出兼容耗材/工艺，且可完成切片。
2. Given 已安装 profiles，When 在 UI 中选择 LONGER LK10 Pro 0.4 喷嘴，Then 列出兼容耗材/工艺，且可完成切片。

---

### User Story 2 - 兼容性与命名校验 (Priority: P2)

用户通过配置验证器与额外检查脚本验证 profiles 的语法、索引、兼容性字段。

**Why this priority**: 确保质量与可维护性，避免“孤儿文件”与字段错误。

**Independent Test**: 运行 OrcaSlicer_profile_validator 与 orca_extra_profile_check.py，输出 0 错误。

**Acceptance Scenarios**:

1. Given 新增 vendor 与机型文件，When 运行验证器，Then 输出 Validation completed successfully。
2. Given 新增 vendor 与机型文件，When 运行 Python 检查脚本，Then 错误为 0。

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?
- 用户未配置 Klipper 宏（START_PRINT/END_PRINT）：应触发一次性告警并自动回退到简化的 Start/End 片段（包含基本预热、归零与收尾）。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: MUST 创建 LONGER vendor 元文件，索引 machine_model/machine 列表。
- **FR-002**: MUST 为 LK10 与 LK10 Pro 各创建 machine_model（通用属性）。
- **FR-003**: MUST 为两机型至少提供 0.4 喷嘴的 machine 变体，nozzle_diameter 为单值数组 ["0.4"].
- **FR-004**: MUST 设置 printable_area 分别为 220x220 与 330x330；printable_height 分别为 220mm（LK10）与 330mm（LK10 Pro）。
- **FR-005**: MUST 继承合适的通用基类（i3/klipper 通用，host_type 固定为 klipper），并与现有对标机型风格一致。
- **FR-006**: MUST 更新 vendor 索引并通过验证器与 Python 检查。
- **FR-007**: MUST 设置默认映射：默认耗材为 Generic PLA @System；默认工艺为 “0.20mm Standard @<机型名称> (0.4 nozzle)”，并确保与 compatible_printers 一致。
- **FR-008**: MUST 采用 Start/End G-code 混合策略：
  - Start：调用 START_PRINT 传递必要参数（如首层与目标温度、床温、料径），随后在切片端执行统一清线/引线段；
  - End：调用 END_PRINT 完成收尾；
  - 该清线段应与 Orca 默认坐标/边界兼容且不越界。
- **FR-009**: MUST 宏缺失降级：
  - 当检测到或推断用户环境未配置 START_PRINT/END_PRINT 宏时，自动回退为简化 Start/End 片段（包含基本预热、归零、回抽与风扇收尾），并显示一次性警告；
  - 降级后生成的 G-code 不应包含 START_PRINT/END_PRINT 调用；
  - 文档需指引用户如何启用宏并恢复到混合策略。

### Key Entities *(include if data involved)*

- **Vendor (LONGER)**: 包含 machine_model_list、machine_list 的索引。
- **MachineModel (LK10/LK10 Pro)**: 通用属性、床面/纹理占位、默认材料。
- **Machine Variant (0.4)**: 可打印区域、喷嘴、继承链、基本 G-code 与主机类型。

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 在 UI 中可选择 LONGER 两款机型，耗材与工艺列表可用并成功切片。
- **SC-002**: 验证器与 Python 检查均通过（0 错误）。
- **SC-003**: 命名与路径完全一致，无孤儿文件；vendor 索引完整。
- **SC-004**: 选择打印机后，UI 中默认耗材与默认工艺分别预选为 Generic PLA @System 与 0.20mm Standard @对应机型（0.4 nozzle）。
- **SC-005**: 生成的 G-code 在开头包含 START_PRINT 调用且随后出现清线/引线段；收尾包含 END_PRINT 调用。
- **SC-006**: 在禁用或缺失宏的场景下，G-code 不包含 START_PRINT/END_PRINT，且包含简化 Start/End 片段；UI 显示一次性警告。

## 配置合规性（如适用）

- 命名与路径：文件名与 JSON 中 name 一致；目录与类型正确。
- 继承结构：正确使用 inherits；避免重复参数。
- 验证通过：OrcaSlicer_profile_validator 与 orca_extra_profile_check.py 均通过。
- 版本策略：涉及 vendor/profile 的版本与 force_update 调整已明确。

## 预设系统（如适用）

- 预设类型仅限：TYPE_PRINT（Process）、TYPE_FILAMENT、TYPE_PRINTER。
- 预设捆绑包包含完整集合；兼容性在 UI 中通过子集筛选体现。
- API 使用：get_edited_preset 与 get_selected_preset 语义不可混用。

## Assumptions

- 假设运动结构与 Neptune 4 Plus 相近（i3 结构），主机类型默认 klipper（host_type=klipper），gcode_flavor 默认 klipper（后续可根据实机调整）。
- 假设默认耗材使用 OrcaFilamentLibrary 的通用 PLA；默认工艺使用通用 0.20mm Standard（供应商或系统映射）。
- 打印高度：LK10 220mm，LK10 Pro 330mm。

