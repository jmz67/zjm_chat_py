import os
import  multiprocessing as mp
from contextlib import asynccontextmanager

try:
    import numexpr  # 尝试导入numexpr库
    n_cores = numexpr.utils.detect_number_of_cores()  # 获取计算机CPU的核心数量
    os.environ["NUMEXPR_MAX_THREADS"] = str(n_cores)  # 设置环境变量NUMEXPR_MAX_THREADS为检测到的核心数量
    print("NUMEXPR_MAX_THREADS", os.environ["NUMEXPR_MAX_THREADS"])
except ImportError as ie:
    # 如果是导入失败（例如numexpr未安装），则记录或打印错误信息
    print(f"ImportError: {ie}")
except Exception as e:
    # 捕获其他类型的异常，并打印出异常类型和信息
    print(f"An error occurred: {type(e).__name__} - {e}")

import click 
from typing import Dict, List 

from fastapi import FastAPI
from utils import build_logger

logger = build_logger()

def _set_app_event(app: FastAPI, started_event: mp.Event = None):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if started_event is not None:
            started_event.set()
        yield

    app.router.lifespan_context = lifespan

def run_api_server(
        started_event: mp.Event = None, run_mode: str = None
):
    import uvicorn

if __name__ == '__main__':
    print('Hello World!') 