# -*- coding: utf-8 -*-
"""中文 pip 快捷命令（`python -m 库 ...`）。

把 pip 常用命令包一层中文名，方便记不住英文单词的用户使用。
实际执行仍调用 `python -m pip ...`，并在运行前打印等效的 pip 命令，
用户对照着看几次就能记住英文原命令。

用法：
    python -m 库 帮助
    python -m 库 安装 <包名> [pip 额外选项...]
    python -m 库 列表
"""

from __future__ import annotations

import subprocess
import sys

# 国内镜像（默认“安装”走这里，官方源访问慢时用）
国内镜像 = "https://pypi.tuna.tsinghua.edu.cn/simple"
MIRROR = 国内镜像

# 需要包名/参数的命令（缺参数时直接报错提示，不调用 pip）
需要参数 = frozenset([
    "安装", "官网安装", "卸载", "升级", "强制重装", "离线安装",
    "查看", "文件", "下载", "配置获取", "配置设置", "配置删除",
])

帮助文本 = """\
中文库管理（python -m 库 <命令> [参数]），常用命令：

  安装 <包> [...]        pip install <包> -i 国内镜像（默认清华源，速度快）
  官网安装 <包> [...]    pip install <包>（官方源）
  卸载 <包> [...]        pip uninstall <包> -y（自动确认，无需再输 -y）
  升级 <包> [...]        pip install --upgrade <包>
  强制重装 <包> [...]    pip install --force-reinstall <包>
  安装本项目 [路径]      pip install -e .（缺省为当前目录 .，可传别的路径）
  离线安装 <包/文件> [...]  pip install --no-index ...（不联网，需配合本地包）
  列表 [...]             pip list
  已过时 [...]           pip list --outdated
  查看 <包> [...]        pip show <包>
  文件 <包> [...]        pip show --files <包>（同时列出该包安装了哪些文件）
  导出 [...]             pip freeze（可重定向：python -m 库 导出 > requirements.txt）
  检查 [...]             pip check（检查依赖冲突）
  下载 <包> [...]        pip download <包>（只下载不安装）
  缓存信息 [...]         pip cache info
  缓存列表 [...]         pip cache list
  清缓存 [...]           pip cache purge
  配置列表 [...]         pip config list
  配置获取 <配置项> [...]  pip config get <配置项>
  配置设置 <配置项> <值> [...]  pip config set <配置项> <值>
  配置删除 <配置项> [...]  pip config unset <配置项>
  版本 [...]             pip --version
  自检 [...]             pip debug（输出 pip 运行环境信息，报 bug 时用）
  帮助                   显示本帮助（不是 pip --help）

说明：
  1. [...] 表示可透传 pip 额外选项，如：python -m 库 安装 requests --upgrade。
  2. “安装”默认走国内镜像；想用官方源请用“官网安装”。
  3. 每次执行前会打印等效的 pip 命令，对照几次即可记住英文原命令。
"""


def 显示帮助() -> None:
    print(帮助文本)


def 构建pip参数(命令: str, 其余: list[str]) -> list[str] | None:
    """由中文命令构造 pip 参数；“帮助”返回 None 表示内部处理。"""
    if 命令 == "安装":
        return ["install", *其余, "-i", MIRROR]
    if 命令 == "官网安装":
        return ["install", *其余]
    if 命令 == "卸载":
        参数 = ["uninstall", *其余]
        if "-y" not in 其余 and "--yes" not in 其余:
            参数.append("-y")
        return 参数
    if 命令 == "升级":
        return ["install", "--upgrade", *其余]
    if 命令 == "强制重装":
        return ["install", "--force-reinstall", *其余]
    if 命令 == "安装本项目":
        return ["install", "-e", *(其余 or ["."])]
    if 命令 == "离线安装":
        return ["install", "--no-index", *其余]
    if 命令 == "列表":
        return ["list", *其余]
    if 命令 == "已过时":
        return ["list", "--outdated", *其余]
    if 命令 == "查看":
        return ["show", *其余]
    if 命令 == "文件":
        return ["show", "--files", *其余]
    if 命令 == "导出":
        return ["freeze", *其余]
    if 命令 == "检查":
        return ["check", *其余]
    if 命令 == "下载":
        return ["download", *其余]
    if 命令 == "缓存信息":
        return ["cache", "info", *其余]
    if 命令 == "缓存列表":
        return ["cache", "list", *其余]
    if 命令 == "清缓存":
        return ["cache", "purge", *其余]
    if 命令 == "配置列表":
        return ["config", "list", *其余]
    if 命令 == "配置获取":
        return ["config", "get", *其余]
    if 命令 == "配置设置":
        return ["config", "set", *其余]
    if 命令 == "配置删除":
        return ["config", "unset", *其余]
    if 命令 == "版本":
        return ["--version", *其余]
    if 命令 == "自检":
        return ["debug", *其余]
    if 命令 in ("帮助", "help", "--help", "-h"):
        return None
    return []  # 未知命令的标记（调用方再报错）


def 主函数(参数: list[str] | None = None) -> int:
    参数 = sys.argv[1:] if 参数 is None else 参数
    if not 参数 or 参数[0] in ("帮助", "help", "--help", "-h", "-?"):
        显示帮助()
        return 0
    命令, 其余 = 参数[0], 参数[1:]
    pip参数 = 构建pip参数(命令, 其余)
    if pip参数 is None:  # 帮助
        显示帮助()
        return 0
    if not pip参数:  # 未知命令
        print(f"未知命令：{命令}\n", file=sys.stderr)
        显示帮助()
        return 2
    if 命令 in 需要参数 and not 其余:
        print(f"命令“{命令}”缺少参数。示例：python -m 库 {命令} <包名>\n", file=sys.stderr)
        显示帮助()
        return 2
    命令行 = [sys.executable, "-m", "pip", *pip参数]
    print("执行：pip " + " ".join(pip参数), flush=True)
    try:
        结果 = subprocess.run(命令行)
    except FileNotFoundError:
        print("找不到 pip（python -m pip 不可用）。", file=sys.stderr)
        return 1
    return 结果.returncode


main = 主函数  # 英文别名，方便测试与复用


if __name__ == "__main__":
    sys.exit(主函数())
