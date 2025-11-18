# OrcaSlicer 配置文件创建指导文档

## 引言

本文档将详细指导如何为 OrcaSlicer 开发配置文件，包括配置文件类型、命名规则、文件结构、创建方法、测试及验证流程，帮助用户快速搭建适配打印机、耗材的个性化配置。

## 一、配置文件概述

OrcaSlicer 采用 JSON 格式存储配置文件，核心分为 **4 类核心配置文件** + **1 个供应商元文件**，各类文件各司其职，协同实现打印参数的精准控制。

### 1.1 核心配置文件类型

|类型|标识字段|作用|示例文件名|
|---|---|---|---|
|打印机模型|`machine_model`|描述打印机通用信息（如支持喷嘴、打印床型号）|`Orca 3D Fuse1.json`|
|打印机变体|`machine`|定义特定喷嘴配置及机械细节（如打印区域、喷嘴类型）|`Orca 3D Fuse1 0.2 nozzle.json`|
|耗材|`filament`|配置耗材参数（如流速、冷却速度、加载时间）|`Generic PLA @Orca 3D Fuse1@.json`|
|工艺|`process`|定义打印质量及行为（如层高、打印模式）|`0.10mm Standard @Orca 3D Fuse1 0.2.json`|

### 1.2 供应商元文件

- 作用：统一管理特定供应商的所有配置文件（模型、变体、耗材、工艺）
- 命名格式：`vendor_name.json`
- 示例：`Orca 3D.json`

### 1.3 命名规则

|文件类型|命名格式|说明|
|---|---|---|
|供应商元文件|`vendor_name.json`|供应商名称需简短，避免文件名过长|
|打印机模型文件|`vendor_name+printer_name+.json`|体现品牌 + 打印机型号|
|打印机变体文件|`vendor_name+printer_variant_name+.json`|变体名称需包含打印机型号 + 喷嘴直径|
|耗材文件|`filament_vendor_name+filament_name+"@"+vendor_name+printer_name/printer_variant_name+.json`|关联对应打印机 / 变体|
|工艺文件|`layer_height+preset_name+"@"+vendor_name+printer_name/printer_variant_name+.json`|预设名可选：standard/fine/fast/draft 等|

> 原则：配置文件名需与 JSON 文件内 `name` 字段一致（不含 `.json` 后缀）

## 二、文件结构

配置文件需按以下目录结构放置在 OrcaSlicer 安装目录下：

plaintext

```plaintext
resources\profiles\
    ├── vendor_name.json  # 供应商元文件
    └── vendor_name\      # 供应商专属文件夹
        ├── machine\      # 打印机模型+变体文件
        │   ├── vendor_name printer_name.json
        │   └── vendor_name printer_name nozzle_diameter.json
        ├── process\      # 工艺文件
        │   └── layer_height preset_name @vendor_name printer_variant.json
        ├── filament\     # 耗材文件
        │   └── filament_vendor filament_name @vendor_name printer_name.json
        └── model\        # 打印机相关3D模型（可选）
            └── 3D模型文件（如.stl/.svg）
```

### 模板文件位置

OrcaSlicer 提供默认模板，可直接基于模板修改：

`OrcaSlicer\resources\profiles_template\Template`

## 三、各类配置文件创建详解

### 3.1 打印机模型配置文件（machine_model）

- 作用：存储打印机通用属性，不涉及具体喷嘴细节
- 存储路径：`resources\profiles\vendor_name\machine\`
- 核心字段说明：
    - `nozzle_diameter`：支持的喷嘴直径（分号分隔）
    - `bed_model`：打印床 3D 模型文件（.stl）
    - `bed_texture`：打印床纹理文件（.svg）
    - `model_id`：打印机型号唯一标识
    - `default_materials`：默认支持的耗材（分号分隔）

#### 示例 JSON

json

```json
{
  "type": "machine_model",
  "name": "Example M5",
  "nozzle_diameter": "0.2;0.25;0.4;0.6",
  "bed_model": "M5-Example-bed.stl",
  "bed_texture": "M5-Example-texture.svg",
  "model_id": "V1234",
  "family": "Example",
  "machine_tech": "FFF",
  "default_materials": "Example Generic PLA;Example Generic PETG"
}
```

> 可选：在 `machine` 文件夹中添加 `[打印机模型名]_cover.png`，将在 UI 中显示为打印机封面图

### 3.2 打印机变体配置文件（machine）

- 作用：定义特定喷嘴的详细参数，继承自通用基础文件
- 存储路径：`resources\profiles\vendor_name\machine\`
- 核心要求：
    - 必须通过 `inherits` 字段继承基础文件（如 `fdm_machine_common`）
    - `nozzle_diameter` 字段需明确单个喷嘴尺寸（数组格式）
    - 需指定兼容的耗材和默认工艺配置

#### 示例 JSON

json

```json
{
  "type": "machine",
  "name": "Example M5 0.2 nozzle",
  "inherits": "fdm_machine_common",
  "from": "system",
  "setting_id": "GM001",
  "instantiation": "true",
  "nozzle_diameter": ["0.2"],
  "printer_model": "Example M5",
  "printer_variant": "0.2",
  "default_filament_profile": ["Example Generic PLA"],
  "default_print_profile": "0.10mm Standard 0.2mm nozzle @Example",
  "printable_area": ["0x0", "235x0", "235x235", "0x235"],
  "nozzle_type": "brass"
}
```

### 3.3 耗材配置文件（filament）

耗材配置分为 **全局库**（所有打印机通用）和 **供应商库**（特定打印机专用），优先使用全局库（可获得官方优化更新）。

#### 3.3.1 全局库耗材（OrcaFilamentLibrary）

- 作用：通用耗材配置，所有打印机可直接使用
- 存储路径：`resources\profiles\OrcaFilamentLibrary\filament\`
- 核心要求：
    - `compatible_printers` 字段需为空（适配所有打印机）
    - 可通过 `inherits` 继承已有基础耗材类型（如 `fdm_filament_pla`）

#### 示例 JSON（新增全局耗材 Generic PLA-GF）

1. 创建文件 `resources\profiles\OrcaFilamentLibrary\filament\Generic PLA-GF @System.json`：

json

```json
{
    "type": "filament",
    "filament_id": "GFL99",
    "setting_id": "GFSA05",
    "name": "Generic PLA-GF @System",
    "from": "system",
    "instantiation": "true",
    "inherits": "fdm_filament_pla",
    "filament_type": ["PLA-GF"],
    "filament_flow_ratio": ["0.96"],
    "compatible_printers": []
}
```

2. 在 `resources\profiles\OrcaFilamentLibrary.json` 中注册：

json

```json
{
    "name": "OrcaFilamentLibrary",
    "version": "02.02.00.04",
    "force_update": "0",
    "description": "Orca Filament Library",
    "filament_list": [
        // 其他耗材...
        {
            "name": "Generic PLA-GF @System",
            "sub_path": "filament/Generic PLA-GF @System.json"
        }
    ]
}
```

#### 3.3.2 供应商库耗材

- 作用：针对特定打印机优化的耗材配置
- 存储路径：`resources\profiles\vendor_name\filament\`
- 核心要求：
    - `compatible_printers` 字段需指定适配的打印机变体（非空）
    - 可继承全局库耗材（如 `Generic ABS @System`）并修改个性化参数

#### 示例 JSON（MyToolChanger 专用 ABS 耗材）

json

```json
{
    "type": "filament",
    "setting_id": "GFB99_MTC_0",
    "name": "Generic ABS @MyToolChanger",
    "from": "system",
    "instantiation": "true",
    "inherits": "Generic ABS @System",
    "filament_cooling_final_speed": ["3.5"],
    "filament_cooling_initial_speed": ["10"],
    "filament_load_time": ["10.5"],
    "filament_loading_speed": ["10"],
    "filament_unload_time": ["8.5"],
    "compatible_printers": [
        "MyToolChanger 0.4 nozzle",
        "MyToolChanger 0.2 nozzle",
        "MyToolChanger 0.6 nozzle",
        "MyToolChanger 0.8 nozzle"
    ]
}
```

> 注意：若耗材兼容 AMS 系统，`filament_id` 长度不可超过 8 字符

### 3.4 工艺配置文件（process）

- 作用：定义打印质量参数（层高、速度、填充等），无全局工艺配置
- 存储路径：`resources\profiles\vendor_name\process\`
- 核心要求：
    - 必须通过 `inherits` 字段继承基础文件（如 `fdm_process_common`）
    - `compatible_printers` 字段指定适配的打印机变体

#### 示例 JSON

json

```json
{
  "type": "process",
  "name": "0.10mm Standard @ExampleVendor Printer 0.2",
  "inherits": "fdm_process_common",
  "from": "system",
  "instantiation": "true",
  "compatible_printers": [
    "ExampleVendor Printer 0.2 nozzle"
  ]
}
```

### 3.5 供应商元文件（vendor_name.json）

- 作用：索引该供应商的所有配置文件，便于 OrcaSlicer 加载
- 存储路径：`resources\profiles\`
- 核心字段：`machine_model_list`/`machine_list`/`process_list`/`filament_list` 分别索引对应类型文件

#### 示例 JSON

json

```json
{
  "name": "ExampleVendor",
  "version": "01.00.00.00",
  "force_update": "1",
  "description": "Example configuration",
  "machine_model_list": [
    {
      "name": "Example M5",
      "sub_path": "machine/Example M5.json"
    }
  ],
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    }
  ],
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    }
  ],
  "filament_list": [
    {
      "name": "fdm_filament_common",
      "sub_path": "filament/fdm_filament_common.json"
    }
  ]
}
```

## 四、测试配置文件更改

修改配置文件后，OrcaSlicer 可能因缓存未加载新配置，需按以下步骤刷新：

1. 打开配置文件夹：点击 OrcaSlicer 菜单 → Help → Show Configuration Folder
2. 清除缓存：删除文件夹中的 `system` 目录（缓存的配置文件存储于此）
3. 重启 OrcaSlicer：重新启动软件后，将自动加载 `resources/profiles/` 下的最新配置

## 五、验证配置文件

需通过 **两种工具** 验证配置文件的兼容性，确保无语法错误或逻辑问题。

### 5.1 OrcaSlicer 配置验证器

- 功能：检查配置文件语法正确性、路径有效性
- 运行方式：
    - Windows：`OrcaSlicer_profile_validator.exe`
    - Ubuntu：`OrcaSlicer_profile_validator`
- 核心参数：
    - `-h/--help`：查看帮助
    - `-p/--path`：指定配置文件根目录（如 `resources/profiles`）
    - `-v/--vendor`：指定供应商名称（可选，不指定则验证所有供应商）
    - `-l/--log_level`：日志级别（默认 2 = 警告，数值越高日志越详细）

#### 示例命令（Windows）

bash

```bash
.\OrcaSlicer_profile_validator.exe --path d:\codes\OrcaSlicer\resources\profiles -l 2 -v Custom
.\build\src\Release\OrcaSlicer_profile_validator.exe --path F:\OS\OrcaSlicer-main\resources\profiles -l 2 -v LONGER
```

#### 验证结果：

- 成功：输出 `Validation completed successfully`
- 失败：提示具体错误（如语法错误、路径错误）

### 5.2 Python 验证脚本

- 功能：额外检查字段一致性（如 `compatible_printers` 有效性、耗材名称一致性）
- 脚本文件：`orca_extra_profile_check.py`
- 核心参数：
    - `--help`：查看帮助
    - `--vendor`：指定供应商（可选）
    - `--check-filaments`：检查耗材的 `compatible_printers` 字段（默认启用）
    - `--check-materials`：检查打印机模型的默认耗材名称
    - `--check-obsolete-keys`：检查配置文件中的废弃字段

#### 示例命令（全量检查）

bash

```bash
python ./orca_extra_profile_check.py --vendor="ExampleVendor" --check-filaments --check-materials
python .\scripts\orca_extra_profile_check.py --vendor="LONGER" --check-filaments --check-materials
```

#### 验证结果：

- 成功：输出错误数为 0，退出码为 0
- 失败：输出具体错误信息，退出码非 0

## 六、关键提示与注意事项

1. 优先使用全局耗材库（`OrcaFilamentLibrary`），仅当需为特定打印机优化时创建供应商专属耗材配置
2. 供应商名称需简短，避免配置文件路径过长导致加载失败
3. 所有配置文件的 `name` 字段必须与文件名（不含 `.json`）完全一致
4. 继承字段（`inherits`）是核心：变体 / 耗材 / 工艺配置需继承对应基础文件，减少重复配置
5. 若配置文件不生效，优先检查缓存（删除 `system` 文件夹）和文件路径是否符合要求