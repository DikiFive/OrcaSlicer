# Project Context

## Purpose
OrcaSlicer 是一款开源的下一代 3D 打印切片软件，目标是提供精准、快速、稳定且易用的切片体验：
- 提供高质量路径规划、智能支撑、精细化参数控制与校准工具；
- 覆盖常见 3D 打印机与耗材的预设（profiles），降低上手门槛；
- 保持跨平台（Windows/macOS/Linux）的一致体验与可重复构建。

参考：仓库 `README.md` 中的“Main features”“How to build”等说明。

## Tech Stack
- 语言与工具链：C++17、CMake（out-of-source 构建）、Catch2（单元测试）
- 桌面框架与底层库：wxWidgets、OpenGL/GLEW、OpenVDB、CGAL、Boost、TBB、OpenEXR、OpenCV 等（见 `deps/` 与 `deps_src/`）
- UI/资源：`resources/` 内置图标、字体、着色器、web 资源与预设数据
- 预设体系：JSON 形式的打印机/耗材/工艺 profiles（配置即数据，无代码变更），脚本位于 `scripts/`
- 版本控制与构建：Git + CMake，平台脚本 `build_release_vs2022.bat`、`build_release_macos.sh`、`build_linux.sh`

## Project Conventions

### Code Style
- C++17，遵循仓库根目录 `.clang-format`：4 空格缩进、140 列上限、类/函数大括号换行；
- 命名：类用 `CamelCase`，函数/局部变量用 `snake_case`，常量用 `SCREAMING_CASE`；
- 头文件自包含，包含顺序与 IWYU 指南一致；
- 在提交前运行 clang-format（CMake 可用 `clang-format` target）。

### Architecture Patterns
- 目录结构（重点）：
	- `src/`：核心 C++ 源码，按功能模块和平台适配拆分；
	- `resources/`：用户资源（图标、字体、预设、着色器等）；
	- `localization/`：多语言资源；
	- `tests/`：测试（基于 Catch2），按领域分组；
	- `cmake/`：CMake 辅助模块；`deps/`、`deps_src/`：第三方依赖（镜像/快照，不直接修改）；
	- `scripts/`、`tools/`：自动化与实用脚本。
- 预设加载与验证：将 profiles 视为数据（JSON），通过脚本生成/校验/打包；
- Klipper 宏约定：与 profiles 协同，常用 `START_PRINT`/`END_PRINT` 模板。

### Testing Strategy
- 单元测试：Catch2，使用 `ctest` 执行；
- 用例组织：`tests/` 下按组件/领域建立文件与夹（如 `tests/libslic3r/`），长时用例打标签便于筛选；
- 固定数据/夹具：放置于 `tests/data/`（如示例 G-code、几何体等）；
- 对难以自动化的功能（如打印机行为验证），在 PR 中补充手动步骤或截图说明。

### Git Workflow
- 分支：
	- `main`/`master`（上游）或项目默认主分支；功能开发采用主题分支（例如：`002-lk10plus-rename`）；
	- 变更较大或跨模块时，先提交 OpenSpec 变更提案（`openspec/changes/`）。
- 提交信息：简洁句式主题，必要时附 issue 引用（例如：`Fix grid lines origin for multiple plates (#10724)`）；
- PR 规范：填写模版、提供复现步骤/截图、指出受影响的预设/翻译、链接相关 issue/依赖变化；
- 在合并前 squash 修正类提交，保持历史清晰。

## Domain Context
- 本项目面向 FFF/FDM 等 3D 打印切片场景：几何处理、分层路径、支撑、速度/加速度/压力提前量等工艺参数；
- 预设体系涵盖“打印机/耗材/工艺”，为不同厂商/机型/材料提供开箱即用的组合；
- 与社区生态协同：Klipper、PrusaLink、OctoPrint 等远程功能；
- OrcaSlicer 源自开源上游（Bambu Studio <- PrusaSlicer <- Slic3r），遵循 AGPL-3.0 许可。

## Important Constraints
- 许可证：AGPL-3.0；使用/分发需遵守同源开源要求；
- 第三方依赖版本需与 `deps/`、`deps_src/` 与 CMake 配置兼容；
- 跨平台构建需在三大平台脚本上通过（Windows/macOS/Linux）；
- 不直接修改 `deps/`、`deps_src/` 源码（视为镜像/快照，修改需同步上游 tag 与说明）。

## External Dependencies
- 桌面与渲染：wxWidgets、OpenGL/GLEW；
- 几何/数值：CGAL、OpenVDB、Qhull、Eigen、TBB、Boost、NLopt、MPFR/GMP；
- 图像/IO：PNG、JPEG、OpenEXR、EXPAT、CURL、OpenSSL、FREETYPE；
- 其他：hidapi、imgui、imguizmo、libigl、clipper 等；
- 运行时组件：WebView2（Windows），VC++ Redistributable（Windows）；
- 测试框架：Catch2（项目内置）。
