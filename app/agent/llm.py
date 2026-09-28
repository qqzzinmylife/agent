"""
电商问数 Agent 使用的大模型实例

集中初始化一个 OpenAI 兼容的 Chat Model，供节点或本地测试直接复用
"""

from langchain.chat_models import init_chat_model

from app.conf.app_config import app_config

#统一配置读取模型三件套,节点只复用llm,不重复初始化模型连接
llm = init_chat_model(
    model = app_config.llm.model_name,
    model_provider ="openai",
    base_url = app_config.llm.base_url,
    api_key = app_config.llm.api_key,
    #字段扩展 SQL生成更看重稳定性,所以这里关闭随机发散
    temperature = 0
)

