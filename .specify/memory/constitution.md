<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles: 新增 VI（预设系统一致性）
- Added sections: 在“附加约束”新增预设系统与 API 使用约束
- Removed sections: 无
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md（加入预设系统门禁）
	- ✅ .specify/templates/spec-template.md（加入“预设系统（如适用）”小节）
	- ✅ .specify/templates/tasks-template.md（加入预设一致性与行为验证示例任务）
	- ⚠ .specify/templates/commands/*.md（目录不存在，暂不适用）
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): 初始采纳日期未知，需维护者确认历史采用时间。
-->

# OrcaSlicer Constitution
<!-- 本宪章定义 OrcaSlicer 仓库中“配置文件创建与维护”的非功能性准则与质量门禁 -->

## Core Principles

### I. 命名与路径一致性（强制）
- 配置文件名（不含 .json 后缀）必须与 JSON 内的 name 字段完全一致。
- 供应商名称需简短，目录结构必须遵循 resources/profiles 既定层级：vendor/machine|process|filament/。
- 机型与变体命名需体现品牌+型号+喷嘴直径；耗材与工艺需按 OrcaSlicer.md 规定的格式命名。
- 所有 JSON 的 type 字段必须正确：machine_model | machine | filament | process。
理由：名称与路径是一切加载与索引的基准，任何不一致都会导致加载失败或缓存混乱。

### II. 继承优先与去重（强制）
- machine / filament / process 必须通过 inherits 继承各自的基础文件（如 fdm_machine_common、Generic XXX @System、fdm_process_common）。
- 机型变体的 nozzle_diameter 必须为单值数组（如 ["0.4"]），并显式声明 printer_model、printer_variant。
- 优先复用全局耗材库 OrcaFilamentLibrary；仅在确有必要时创建供应商专用耗材，并正确设置 compatible_printers。
理由：通过继承减少重复与漂移，确保配置可维护、可演进。

### III. 可验证性与质量门禁（强制）
- 任何配置变更必须通过官方配置验证器 OrcaSlicer_profile_validator（Windows/Ubuntu）。
- 必须通过 Python 额外检查脚本 orca_extra_profile_check.py（含耗材兼容性、默认材料、废弃键检查）。
- 验证失败即为阻塞：PR 不得合入，需在 PR 描述附上关键验证输出摘要。
理由：在本地和 CI 阶段尽早发现语法、路径、一致性问题，避免回归。

### IV. 版本化与变更管理（强制）
- 宪章与配置均采用语义化版本：MAJOR.MINOR.PATCH。
- 供应商元文件 vendor_name.json 的 version/force_update 字段必须按变更语义更新。
- 破坏性变更（如移除/重命名 profile、变更兼容矩阵）必须提供迁移说明与影响范围。
理由：版本是使用者与升级策略的依据，也是回溯变更的锚点。

### V. 可操作性与文档化（建议/强制混合）
- 强制：合并前在本地完成缓存刷新流程（删除配置目录下 system 缓存并重启应用）进行人工冒烟验证。
- 建议：为新机型添加封面图 [打印机模型名]_cover.png 以提升可用性与辨识度。
- 建议：在供应商元文件完成索引后，于文档或 PR 描述附链接与使用说明。
理由：确保变更可被用户实际加载与感知，降低支持成本。

### VI. 预设系统一致性（强制）
- 预设捆绑包（PresetBundle）存放 prints/filaments/printers 的完整集合，兼容性在 UI 层通过筛选子集实现，禁止在 Bundle 层做强制剔除。
- 仅使用仍在支持的枚举类型：TYPE_PRINT（对应 Process）、TYPE_FILAMENT、TYPE_PRINTER；禁止引入 SLA 遗留类型。
- API 语义必须遵守：get_edited_preset() 返回含用户修改的当前预设；get_selected_preset() 返回原始未修改预设；读写行为须选用正确接口。
- 不得破坏既有预设文件的反序列化兼容性；如涉及格式或键名变更，必须提供迁移说明与回滚策略。
理由：保持运行时预设行为一致、可预期，避免 UI 与数据层面错配。

## 附加约束

1) 文件与路径约束
	- 路径长度需可在目标平台可靠访问（Windows 对长路径较敏感）。
	- 纹理/模型文件（.svg/.stl）引用必须存在于 resources/profiles 或其约定子目录。

2) AMS 兼容性
	- 若耗材需兼容 AMS，filament_id 长度不得超过 8 个字符。

3) 孤儿文件与索引
	- 禁止未在 vendor_name.json 索引的“孤儿配置文件”。
	- 任何新增/重命名必须同步更新 vendor_name.json 的对应列表。

4) 预设系统补充约束
	- TYPE_PRINT 名称上的历史命名（“Print” 实指 “Process”）不可贸然重命名枚举；需在文档/UI 侧清晰映射，保持序列化稳定。
	- 涉及预设筛选逻辑的修改，需在 PR 描述中提供：选择某打印机变体后，耗材与工艺列表显示“兼容子集”的截图/步骤。

## 开发流程与质量门禁

1) 变更流程（新增/修改任一配置）
	- 创建/更新配置文件于正确目录；保持文件名与 name 一致。
	- 使用 inherits 复用基类；避免重复参数。
	- 更新 vendor_name.json 的 machine_model_list/machine_list/process_list/filament_list 索引。
	- 本地运行验证器与 Python 检查；修复所有错误或显式豁免理由。
	- 清缓存并重启应用做冒烟验证（加载、选择、切片流程可达）。
	- 在 PR 中附上：版本号变更、验证输出摘要、兼容矩阵与影响说明。

2) 质量门禁（PR 必须满足）
	- 宪章原则 I–IV 全部通过；原则 V 至少完成“缓存刷新+冒烟”。
	- 无验证错误；警告需在 PR 说明中确认接受理由。
	- 如引入破坏性变更，提供迁移说明与 SemVer 决策。

## Governance
<!-- 宪章解释权与修订流程 -->

本宪章优先级高于与配置流程相关的其他实践性文档；与 OrcaSlicer.md 若有冲突，以 OrcaSlicer.md 为准并在后续修订本宪章以保持一致。

  - ✅ .specify/templates/plan-template.md（补充 Constitution Check 门禁要点）
  - ✅ .specify/templates/spec-template.md（新增“配置合规性要求（如适用）”占位）
  - ✅ .specify/templates/tasks-template.md（示例中加入“配置验证与缓存刷新”任务）
  - ⚠ .specify/templates/commands/*.md（目录不存在，暂不适用）
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): 初始采纳日期未知，需维护者确认历史采用时间。
-->

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): 初次采纳日期待确认 | **Last Amended**: 2025-10-20
<!-- 版本说明：首次落地宪章与门禁，建立与 OrcaSlicer 配置指导文档的一致性基线 -->
