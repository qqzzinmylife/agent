

import sys
from pathlib import Path

from loguru import logger

from app.conf.app_config import app_config
from app.core.context import request_id_ctx_var



log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<magenta>request_id - {extra[request_id]}</magenta> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

def inject_request_id(record):
    """把上下文中的request_ud注入到每条日志的extra字段中"""
    request_id = request_id_ctx_var.get()
    record["extra"]["request_id"] = request_id


# 移除Loguru默认的输出目标，避免和项目自定义配置重复打印
logger.remove()
# 生成带request_id注入能力的logger,后续代码统一使用
logger = logger.patch(inject_request_id)


# 根据配置决定是否输出控制条日志，适合本地开发和勇气标准输出采集
if app_config.logging.console.enable:
    logger.add(
        sink = sys.stdout,
        level = app_config.logging.console.level,
        format = log_format,
    )

# 根据配置决定是否写入日志,并在启动时确保目标日志存在
if app_config.logging.console.enable:
    path = Path(app_config.logging.file.path)
    path.mkdir(parents = True, exist_ok = True)
    logger.add(
        sink=path / "app.log",
        level=app_config.logging.file.level,
        format=log_format,
        rotation=app_config.logging.file.rotation,
        retention=app_config.logging.file.retention,
        encoding="utf-8",
    )


