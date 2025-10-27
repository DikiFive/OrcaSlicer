## Why
为与硬件和社区通用叫法保持一致，并减少“LK10 / LK10 Plus”混称导致的用户困惑，需要将现有 Longer 机型相关的预设与脚本中的名称统一为“LK10 Plus”。该改名还有助于后续扩展（如区分 Pro/Plus 变体、打包正确的 Klipper 宏模板）。

## What Changes
- 统一 profiles/vendor 名称与显示名为“Longer LK10 Plus”（含 `resources/profiles/` 与 `resources/profiles_template/` 中的目录/文件/JSON 字段）
- 更新安装/同步脚本（`scripts/install_longer_user_printers.ps1`、`scripts/sync_longer_profiles_to_app.ps1`、`scripts/apply_longer_system_profiles.ps1` 等）中的机型匹配与路径
- 如有 README/文档内指代“LK10”的位置，统一替换为“LK10 Plus”并校对截图/说明
- 校验 Klipper 宏模板（`START_PRINT`/`END_PRINT`）在改名后仍能正确关联并加载
- 对用户缓存/已有配置提供一次性迁移策略（旧名 → 新名 的映射），避免丢失已有自定义配置

## Impact
- Affected specs: printer-profiles（打印机预设与命名约定）
- Affected assets: `resources/profiles/**`, `resources/profiles_template/**`
- Affected scripts: `scripts/install_longer_user_printers.ps1`, `scripts/sync_longer_profiles_to_app.ps1`, `scripts/apply_longer_system_profiles.ps1`, 以及可能引用机型名的其他脚本
- Affected docs: README/指南中对机型名称的文本与截图（如有）

## Status
- Implemented (2025-10-27)
- Notes:
	- 索引与文件均已迁移至 "LK10 Plus"；遗留 `LK10Plus` 机型与工艺文件已清理
	- 内部 ID 与素材文件名保留 `lk10plus` 前缀（例如 model_id 与床面纹理/模型），属内部兼容，不影响 UI 命名一致性
	- 抽样与脚本校验均通过；建议在应用内进行一次手工选择机型与切片的冒烟验证
