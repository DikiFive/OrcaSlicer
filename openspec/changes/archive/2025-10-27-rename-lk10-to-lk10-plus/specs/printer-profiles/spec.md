## ADDED Requirements

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
