import asyncio
import random
from typing import Optional

from qdrant_client import AsyncQdrantClient,models

from app.conf.app_config import QdrantConfig, app_config

class QdrantClientManager:
    def __init__(self,qdrant_config:QdrantConfig):
        # 保存配置对象,后面初始化客户端时从这里取host和port
        self.qdrant_config = qdrant_config
        # 先把client声明出来,真正初始化放到init()中进行
        self.client: Optional[AsyncQdrantClient] = None
    def _get_url(self) -> str:
        """拼接Qdrant 服务地址"""
        return f"http://{self.qdrant_config.host}:{self.qdrant_config.port}"
    def init(self):
        """显式初始化 Qdrant 客户端
        这里不在__init__中直接初始化,是为了和项目周期管理一致
        """
        self.client = AsyncQdrantClient(url = self._get_url())

        async def close(self):
            await self.client.close()

# 创建一个全局的管理器对象
# 后续项目中的其他模块都通过它来获取同一套 Qdrant 客户端
qdrant_client_manager = QdrantClientManager(app_config.qdrant)


