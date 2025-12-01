from fastapi import FastAPI
from app.api import v1
from fastapi.responses import HTMLResponse
from pathlib import Path
import logging
import logging.config


def setup_logging():
    conf_path = Path(__file__).parent / "config" / "logging.conf"
    try:
        # 优先使用文件配置，便于集中管理与覆盖
        logging.config.fileConfig(conf_path, disable_existing_loggers=False)
    except Exception:
        # 当文件缺失或解析失败时，回退到一个基础的控制台输出
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )


app = FastAPI()
setup_logging()


app.include_router(v1.router, prefix="/api/v1")
