# Win7/Vista 兼容补丁（取自 PythonVista v3.13.16）

来源：https://github.com/adang1345/PythonVista （tag `v3.13.16`，`patches/` 目录）。
该仓库发布的是补丁包而非改完的完整源码：从 python.org 官方 sdist 出发，
按 `Notes.md` 中 Python 3.13 一节打补丁，再跑 `Tools/msi/buildrelease.bat`。

## 补丁清单（3.13.16 用这 4 个官方补丁 + 1 个自制）

| 补丁 | 作用 |
|---|---|
| `add-dll-7.patch` | 随包安装 `api-ms-win-core-path-l1-1-0.dll`（Vista/Win7 运行必需） |
| `restore-vista-handling-7.patch` | 恢复 Vista/SP2 兼容（3.13.15+ 用 -7 版） |
| `build-full-installer-7.patch` | 切到 `full.wixproj` 打完整离线包（含调试符号/二进制、UCRT、实验性自由线程版） |
| `fix-launcher-2.patch` | py 启动器 Win7 兼容 + 随包带 dll |
| `zh-bundle-win7.patch` | 自制：将上面两个补丁对 `Default.wxl` 的改动汉化后合入本仓库版本 |

`support-vs-2026-12.patch` 已直接合入 main（runner 为 VS2026，3.13 原生工程要求
v143 工具集会报 MSB8020；win7 job 的 `add-dll-7` 在其之上仍可正常应用）。
未采用：`fix-tcltk-*`（3.13 一节未要求）、`fix-ucrt-3`（仅 3.13.0-3.13.7 需要）。

## 应用顺序（workflow 中执行，勿调换）

```
add-dll-7 → fix-launcher-2 → build-full-installer-7 → restore-vista-7 → zh-bundle-win7
```

`build-full-installer-7` 与 `restore-vista-7` 对 `Tools/msi/bundle/Default.wxl`
的 hunks 用 `--exclude` 跳过，改由 `zh-bundle-win7.patch` 以汉化形式加入：
`FailureOldOS` 拆为 6 条 Win7/Vista/Server 中文提示（bootstrapper cpp 引用了这些新 ID，
缺失会导致构建失败）；3 条 `Include_*` 由“下载”改为“安装”、VS 2017→VS 2026（full 离线包语义）。

## 与中文汉化的合并说明

- 其余补丁文件与中文改动（`Parser/pegen.c`、`Python/bltinmodule.c`、`Objects/*`、
  `Modules/_io/*`、`Lib/_zh_builtins.py`）无重叠，直接应用。
- 本版按用户要求暂不汉化标准库（无 `_zh_stdlib.py`），无运行横幅（`Modules/main.c` 未动）。
