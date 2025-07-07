
# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A sqlite database assistant implemented by assistant"""

import os
import asyncio
from typing import Optional

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')


def init_agent_service():
    llm_cfg = {
        'model': 'qwen3-235b-a22b',
        # 'model': 'qwen3-30b-a3b',
        # 使用 DashScope 提供的模型服务：
        # 'model': 'qwen-max-latest',
        'model_server': 'dashscope',
        'api_key': 'sk-a758577431f646618ecbb6ee07c945bd',
        # 如果这里没有设置 'api_key'，它将读取 `DASHSCOPE_API_KEY` 环境变量。

        # 使用与 OpenAI API 兼容的模型服务，例如 vLLM 或 Ollama：
        # 'model': 'Qwen2.5-7B-Instruct',
        # 'model_server': 'http://localhost:8000/v1',  # base_url，也称为 api_base
        # 'api_key': 'EMPTY',

        # （可选） LLM 的超参数：
        'generate_cfg': {
            'top_p': 0.8
        }
    }
    system = ('你扮演一个热点新闻总结助手，你具有浏览网页的能力，此外，你还知道“正午看天下”新闻栏目的URL为：https://weibo.com/1842606855')
    # tools = [{
    #     "mcpServers": {
    #         "browsermcp": {
    #             "command": "npx",
    #             "args": ["@browsermcp/mcp@latest"]
    #         },
    #         "fetcher": {
    #             "command": "npx",
    #             "args": ["-y", "fetcher-mcp"]
    # }
    #     }
    # }]
    bot = Assistant(
        llm=llm_cfg,
        name='热点新闻总结助手',
        description='总结热点新闻',
        system_message=system,
        function_list=tools,
    )

    return bot


def test(query='数据库里有几张表', file: Optional[str] = os.path.join(ROOT_RESOURCE, 'poem.pdf')):
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []

    if not file:
        messages.append({'role': 'user', 'content': query})
    else:
        messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

    for response in bot.run(messages):
        print('bot response:', response)


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        # Query example: 数据库里有几张表
        query = input('user question: ')
        # File example: resource/poem.pdf
        file = input('file url (press enter if no file): ').strip()
        if not query:
            print('user question cannot be empty！')
            continue
        if not file:
            messages.append({'role': 'user', 'content': query})
        else:
            messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

        response = []
        for response in bot.run(messages):
            print('bot response:', response)
        messages.extend(response)


def app_gui():
    # Define the agent
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            '帮我分析今天的微博热榜，并将信息进行分类、汇总和去重，生成一份今日热点内容，每条内容需包括分类、标题、简述和链接。'
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()
