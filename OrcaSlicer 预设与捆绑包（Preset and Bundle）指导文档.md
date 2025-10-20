## 概述

本文档基于 OrcaSlicer 官方 Wiki 内容，详细解释代码中 3 个核心类（`Preset`、`PresetBundle`、`PresetCollection`）的功能、类型及使用规则，帮助理解软件预设系统的底层逻辑。

> ⚠️ 警告：代码库中存在大量过时（outdated）和遗留（legacy）代码，部分预设类型已不再使用。

## 一、Preset 类

### 核心作用

定义各类预设的数据类型，通过枚举 `Type` 区分预设所属的场景（如打印工艺、耗材、打印机）。

### 关键枚举类型（Type）

以下是 3 个仍在使用的核心类型（其他类型多为 SLA 打印机相关，因软件已停止支持 SLA，属于遗留代码）：

|枚举值|含义说明|对应 UI / 示例|
|---|---|---|
|`TYPE_PRINT`|打印工艺预设（ legacy 代码导致命名为 “Print”，实际指 “Process”）|层厚、线宽、填充、支撑等工艺参数配置；示例：`Global Objects 0.20mm Standard Ender3 - lan`|
|`TYPE_FILAMENT`|耗材预设（针对不同材质耗材的参数配置）|示例：`ABS - PlastAr`|
|`TYPE_PRINTER`|打印机预设（针对特定打印机的基础配置）|示例：`Bambu Lab X1 0.4 nozzle`；包含床型等参数|

### 关联 UI 参数（TYPE_PRINT 示例）

`TYPE_PRINT` 对应的工艺参数界面包含以下核心配置项（仅列举关键类别）：

- 层厚（Layer height）：初始层厚、常规层厚
- 线宽（Line width）：默认、初始层、外壁、内壁、顶面等
- 接缝（Seam）：位置（对齐 / 交错内壁接缝）、间隙、斜接接缝（测试版）
- 精度（Precision）：切片间隙闭合半径、分辨率、圆弧拟合、XY 补偿等
- 其他：擦拭速度、大象脚补偿、精准壁 / 高度配置等

## 二、PresetBundle 类

### 核心作用

预设捆绑包，用于整合一组相关的 `PresetCollection`（打印工艺集合、耗材集合、打印机集合），是软件启动时加载的核心数据单元。

### 包含的集合

一个 `PresetBundle` 固定包含以下 3 类集合：

1. `PresetCollection prints`：打印工艺预设集合（存储所有 `TYPE_PRINT` 类型预设）
2. `PresetCollection filaments`：耗材预设集合（存储所有 `TYPE_FILAMENT` 类型预设）
3. `PrinterPresetCollection printers`：打印机预设集合（存储所有 `TYPE_PRINTER` 类型预设）

### 重要规则

- 捆绑包中的**打印机、耗材、工艺预设无需强制兼容**，所有已保存的预设会统一存储在一个 `PresetBundle` 中。
- 软件启动时自动加载 `PresetBundle`，针对某台打印机显示的耗材 / 工艺列表，仅为 `filaments`/`prints` 集合的**子集**（筛选兼容项）。

## 三、PresetCollection 类

### 核心作用

预设集合容器，用于存储同一类型的多个预设（可存储任意 `Preset` 类型）。

### 派生类

- `PrinterPresetCollection`：继承自 `PresetCollection`，专门用于存储打印机预设（`TYPE_PRINTER`）。

### 关键函数

|函数名|功能描述|
|---|---|
|`get_edited_preset()`|返回当前选中的预设，**包含用户已做的修改**|
|`get_selected_preset()`|返回当前选中的预设，**不包含用户修改（即原始预设）**|

## 四、总结

1. **层级关系**：`Preset`（单个预设）→ `PresetCollection`（同类型预设集合）→ `PresetBundle`（多类型集合捆绑包）。
2. **核心用途**：通过捆绑包统一管理打印机、耗材、工艺预设，启动时加载并按需筛选兼容项。
3. **注意事项**：避免依赖遗留代码（如 SLA 相关预设类型），使用时需关注预设间的兼容性（软件会自动筛选子集）。