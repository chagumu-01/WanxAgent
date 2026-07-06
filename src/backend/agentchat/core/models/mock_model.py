import time
from typing import List, AsyncGenerator, Optional, Any, ClassVar
from langchain_core.messages import BaseMessage, HumanMessage, AIMessageChunk
from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatGenerationChunk


class MockChatModel(BaseChatModel):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        pass

    async def _astream(self, messages, stop=None, run_manager=None, **kwargs):
        for msg in messages:
            if isinstance(msg, HumanMessage):
                user_input = msg.content
                response = f"您好！我收到了您的消息：'{user_input}'。\n\n这是WanxAgent智能助手的响应。由于当前未配置有效的模型API Key，我正在使用本地模拟模式为您服务。\n\n您可以在系统设置中配置真实的大语言模型API（如通义千问、OpenAI等），以获得完整的AI对话能力。"
                
                chunks = [response[i:i+30] for i in range(0, len(response), 30)]
                for chunk in chunks:
                    time.sleep(0.1)
                    chunk_msg = AIMessageChunk(content=chunk)
                    yield ChatGenerationChunk(message=chunk_msg)
                break

    @property
    def _llm_type(self):
        return "mock"

    def _get_invocation_params(self, **kwargs):
        return {}