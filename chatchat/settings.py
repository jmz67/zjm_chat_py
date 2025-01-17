from __future__ import annotations

import os
from pathlib import Path
import sys
import typing as t

import nltk

from pydantic_settings_file import *


# chatchat 数据目录，必须通过环境变量设置。如未设置则自动使用当前目录。
# resolve() 方法会将给定的路径转换为绝对路径，并解析任何符号链接。
# 这样可以确保 CHATCHAT_ROOT 总是指向一个明确且唯一的文件系统位置，而不会受到相对路径的影响。
CHATCHAT_ROOT = Path(os.environ.get("CHATCHAT_ROOT", ".")).resolve()

class BasicSettings(BaseFileSettings):
    """
    服务器的基本配置信息
    除 log_verbose/HTTPX_DEFAULT_TIMEOUT 修改后即时生效
    其它配置项修改后都需要重启服务器才能生效，服务运行期间请勿修改
    """
    ...

if __name__ == "__main__":
    ...

