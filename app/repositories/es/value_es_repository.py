"""
字段取值 ES 仓储

把字段真实取值组织成 Elasticsearch 全文索引，并提供索引创建 批量写入和关键词检索能力

Service 层负责决定哪些字段需要同步
Repository 只关心索引是否存在 ValueInfo 如何写进 ES 以及如何按关键词召回
"""

from dataclasses import asdict
from http import client

from elasticsearch import AsyncElasticsearch, Elasticsearch

from app.entities.value_info import ValueInfo

class ValueESRepository:
    """负责字段取值全文索引的创建,写入,和基础检索"""

    index_name =  "value_index"
    #value字段使用IK分词,这样地区,会员等级,品类等中文才能按全文方式检索
    index_mappings = {
        "dynamic": False,
        "properties": {
            "id": {"type": "keyword"},
            "value": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word",
            },
            "column_id": {"type": "keyword"},
        },
    }
    def __init__(self, client: AsyncElasticsearch):
        self.client = client
    async def ensure_index(self):
        """确保字段取值缩影已经创建好"""
        if not await self.client.indices.exists(index = self.index_name):
            await self.client.indices.create(
                index = self.index_name, mappings=self.index_mappings
            )
    async def index(self,value_infos: list[ValueInfo],batch_size = 20):
        """分批次写入字段取值,避免一次bulk过大"""
        if not value_infos:
            return
        for i in range(0, len(value_infos), batch_size):
            batch_value_infos = value_infos[i : i + batch_size]
            batch_operations = []
            for value_info in batch_value_infos:
                #用ValueInfo.id 作为文档id,这样重复构建时会覆盖同一条值记录
                batch_operations.append(
                    {"index":{"_index":self.index_name,"_id":value_info.id}}
                )
                batch_operations.append(asdict(value_info))
            await self.client.bulk(operations=batch_operations)
