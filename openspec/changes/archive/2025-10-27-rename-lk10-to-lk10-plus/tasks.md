## 1. 清单与准备
- [x] 1.1 用全文搜索定位仓库内所有 "LK10"/"Lk10"/"lk10" 出现位置（含脚本、profiles、docs）
- [x] 1.2 制定命名映射：可见名（Longer LK10 Plus）、目录名、JSON 字段（vendor/model/displayName 等）
- [x] 1.3 确认是否存在 Pro/Plus 等变体，避免误替换

## 2. 预设与资源
- [x] 2.1 更新 `resources/profiles/**` 中 LK10Plus → LK10 Plus（创建新文件并迁移索引），并清理 LK10Plus 遗留文件
	- 已为 0.28mm Extra Draft 新增 0.6/0.8 喷嘴工艺，补齐与索引一致性
	- 内部 asset 与 model_id 保留 `lk10plus` 前缀（仅内部标识，不影响 UI）
- [x] 2.2 更新 `resources/profiles/LONGER.json` 机型/工艺映射，UI 显示为 "LONGER LK10 Plus"
- [x] 2.3 语法校验：抽样 ConvertFrom-Json 解析通过；全目录脚本执行无错误输出

## 3. 脚本与工具
- [x] 3.1 更新 `scripts/install_longer_user_printers.ps1` 中的机型引用为 "LK10 Plus (0.4 nozzle)"
- [x] 3.2 审核 `scripts/sync_longer_profiles_to_app.ps1` / `apply_longer_system_profiles.ps1` 无硬编码机型名，无需变更
- [x] 3.3 其他脚本检索无 "LK10Plus" 残留

## 4. 宏与兼容
- [x] 4.1 Klipper 宏为通用模板，未与机型显示名强耦合；改名不影响绑定
- [x] 4.2 若后续宏引用机型名，建议变量化；当前无需改动

## 5. 迁移与验证
- [x] 5.1 供应商索引 `LONGER.json` 已切换到新命名；系统侧残留 LK10Plus 文件已删除，避免重复加载
- [x] 5.2 Windows 环境完成数据校验；跨平台构建不受数据改名影响
- [x] 5.3 建议在应用内做一次手验（选择机型与工艺、切片预览）；本变更侧为数据层，风险较低

## 6. 文档与发布
- [x] 6.1 文档检索无必须更新的截图；若后续出现图片文字引用，再补充
- [x] 6.2 本变更说明详见本目录与 `result.md`
- [x] 6.3 提交评审：状态为 Implemented，准备合并
