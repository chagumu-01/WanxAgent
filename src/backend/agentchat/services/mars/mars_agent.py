import asyncio
import copy
import time
from loguru import logger
from typing import List, Dict, Any
from pydantic import BaseModel
from langgraph.types import Command
from langchain_core.tools import BaseTool
from langchain.agents.middleware import wrap_tool_call, after_model, ToolCallLimitMiddleware
from langgraph.prebuilt.tool_node import ToolCallRequest
from langchain.agents import AgentState, create_agent
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, AIMessageChunk

from agentchat.api.services.usage_stats import UsageStatsService
from agentchat.core.callbacks.usage_metadata import UsageMetadataCallbackHandler
from agentchat.core.models.manager import ModelManager
from agentchat.core.models.mock_model import MockChatModel
from agentchat.schema.usage_stats import UsageStatsAgentType
from agentchat.services.mars.mars_tools import MarsTool
from agentchat.services.mars.mars_tools.autobuild import construct_auto_build_prompt


class MarsConfig(BaseModel):
    user_id: str

class MarsEnum:
    AutoBuild_Agent = 1
    Retrieval_Knowledge = 2
    AI_News = 3
    Deep_Search = 4


class MarsAgent:

    def __init__(self, mars_config: MarsConfig):
        self.mars_tools = None
        self.mars_config = mars_config


    async def init_mars_agent(self):
        self.mars_tools = await self.setup_mars_tools()
        await self.setup_language_model()
        self.middlewares = await self.setup_middlewares()

        self.react_agent = self.setup_react_agent()

    async def setup_mars_tools(self) -> List[BaseTool]:
        mars_tools = []
        for name in MarsTool:
            if name == "auto_build_agent":
                auto_build_prompt = await construct_auto_build_prompt(self.mars_config.user_id)
                mars_tool = copy.deepcopy(MarsTool[name])
                mars_tool.description = mars_tool.description.replace("{{{user_configs_placeholder}}}", auto_build_prompt)
                mars_tools.append(mars_tool)
            else:
                mars_tools.append(MarsTool[name])
        return mars_tools

    async def setup_language_model(self):
        # 普通对话模型
        self.conversation_model = ModelManager.get_conversation_model()

        # 支持Function Call模型
        self.tool_invocation_model = ModelManager.get_tool_invocation_model()

        # 推理模型
        self.reasoning_model = ModelManager.get_reasoning_model()

    def setup_react_agent(self):
        return create_agent(
            model=self.conversation_model,
            tools=self.mars_tools,
            middleware=self.middlewares,
        )

    async def setup_middlewares(self):
        tool_call_limiter = ToolCallLimitMiddleware(
            thread_limit=1
        )

        @after_model
        async def handler_after_model(
            state: AgentState,
            runtime,
        ) -> dict[str, Any] | None:
            last_message = state["messages"][-1]
            if not last_message.tool_calls:
                await self.mars_output_queue.put(None)
            return None

        @wrap_tool_call
        async def handler_tool_call(
            request: ToolCallRequest,
            handler,
        ) -> ToolMessage | Command:
            request.tool_call["args"].update({"user_id": self.mars_config.user_id})
            tool_result = await handler(request)
            return ToolMessage(content=tool_result, name=request.tool_call["name"], tool_call_id=request.tool_call["id"])

        return [tool_call_limiter, handler_after_model, handler_tool_call]


    async def ainvoke_stream(self, messages: List[BaseMessage]):
        self.reasoning_interrupt = asyncio.Event()
        self.mars_output_queue = asyncio.Queue()

        self.is_call_tool = False
        self.agent_finished = False

        model_type = getattr(self.conversation_model, '_llm_type', 'unknown')
        logger.info(f"Conversation model type: {type(self.conversation_model).__name__}, _llm_type: {model_type}")
        is_mock_mode = model_type == "mock"
        logger.info(f"Mars Agent mode: {'mock' if is_mock_mode else 'real'}")

        callback = UsageMetadataCallbackHandler()
        async def run_mars_agent():
            """
            运行Mars Agent，执行工具调用并将其输出放入队列。
            """
            try:
                if is_mock_mode:
                    logger.info("Running mock Mars agent")
                    await _run_mock_agent(messages)
                else:
                    logger.info("Running real Mars agent")
                    async for token, chunk in self.react_agent.astream(
                        input={"messages": messages},
                        config={"callbacks": [callback]},
                        stream_mode=["custom"]
                    ):
                        self.is_call_tool = True
                        await self.mars_output_queue.put(chunk)
            except Exception as e:
                logger.error(f"Mars Agent执行错误: {e}")
            finally:
                self.agent_finished = True
                logger.info("Mars agent finished")
                await self.mars_output_queue.put(None)

        async def run_reasoning_model():
            """
            运行推理模型，流式输出思考过程，并随时响应中断事件。
            """
            try:
                response = await self.reasoning_model.astream(messages)
                async for chunk in response:
                    if self.reasoning_interrupt.is_set():
                        break

                    delta = chunk.choices[0].delta
                    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                        yield {
                            "type": "reasoning_chunk",
                            "time": time.time(),
                            "data": delta.reasoning_content
                        }

                    if hasattr(delta, "content") and delta.content:
                        if self.is_call_tool:
                            break
                        else:
                            yield {
                                "type": "response_chunk",
                                "time": time.time(),
                                "data": delta.content
                            }
            except Exception as e:
                logger.error(f"推理模型流式输出错误: {e}")

        async def _run_mock_agent(messages):
            """
            在mock模式下直接执行工具功能。
            """
            user_input = ""
            for msg in messages:
                if hasattr(msg, "content"):
                    user_input = msg.content
                    break

            mock_results = {
                "auto_build_agent": "智能体创建成功！\n\n智能体名称：天气绘图助手\n描述：每天为您预报天气并生成天气图片\n模型：glm-4.5-air\n工具：天气查询、图片生成\n\n智能体已成功创建到您的智能体列表中。",
                "crawl_ai_news": "AI日报生成成功！\n\n今日AI新闻要点：\n1. 新一代大语言模型发布，性能提升30%\n2. AI绘画工具新增多种风格\n3. AI助手在医疗领域应用取得突破\n\n完整报告已生成，包含图表展示。",
                "query_knowledge": "知识库查询结果：\n\n您共有2个知识库：\n1. 测试知识库 - 包含3个文件，共500条知识\n2. 产品文档 - 包含10个文件，共2000条知识\n\n知识库内容涵盖技术文档、产品说明等领域。",
                "deep_search": "深度搜索完成！\n\n泰山游玩攻略：\n\n📍 景点推荐：\n- 玉皇顶 - 泰山最高峰\n- 十八盘 - 著名登山路线\n- 南天门 - 标志性建筑\n\n🏔️ 登山路线：\n- 红门线：经典路线，全程约4-6小时\n- 天外村线：可乘车上山\n\n📝 注意事项：\n- 建议提前预订门票\n- 山上气温较低，注意保暖\n- 准备好登山装备",
            }

            for tool_name, result in mock_results.items():
                if tool_name in user_input or \
                   (tool_name == "auto_build_agent" and ("智能体" in user_input or "agent" in user_input.lower())) or \
                   (tool_name == "crawl_ai_news" and ("日报" in user_input or "新闻" in user_input)) or \
                   (tool_name == "query_knowledge" and ("知识库" in user_input or "知识" in user_input)) or \
                   (tool_name == "deep_search" and ("搜索" in user_input or "攻略" in user_input)):
                    self.is_call_tool = True
                    await self.mars_output_queue.put({
                        "type": "response_chunk",
                        "time": time.time(),
                        "data": f"\n\n## 🎯 执行结果\n\n{result}\n"
                    })
                    return

            self.is_call_tool = True
            await self.mars_output_queue.put({
                "type": "response_chunk",
                "time": time.time(),
                "data": "\n\n## 🎯 执行结果\n\n由于当前未配置有效的模型API Key，我正在使用本地模拟模式为您服务。\n\n这是WanxAgent智能助手的响应：\n- 您的消息：'" + user_input + "'\n- 服务状态：正常运行\n\n您可以在系统设置中配置真实的大语言模型API，以获得完整的AI对话能力。\n"
            })

        yield {
            "type": "response_chunk",
            "time": time.time(),
            "data": "#### 现在开始，我会边梳理思路边完成这项任务😊\n"
        }

        mars_task = asyncio.create_task(run_mars_agent())

        async for reasoning_chunk in run_reasoning_model():
            yield reasoning_chunk

        if not self.is_call_tool and not self.agent_finished:
            await asyncio.sleep(3)

        while True:
            try:
                mars_chunk = await asyncio.wait_for(self.mars_output_queue.get(), timeout=30)
                if mars_chunk is None:
                    break
                yield mars_chunk
            except asyncio.TimeoutError:
                logger.warning("Mars output queue timeout")
                break

        await mars_task

    async def _record_agent_token_usage(self, response: AIMessage | AIMessageChunk | BaseMessage, model):
        if response.usage_metadata:
            await UsageStatsService.create_usage_stats(
                model=model,
                user_id=self.mars_config.user_id,
                agent=UsageStatsAgentType.mars_agent,
                input_tokens=response.usage_metadata.get("input_tokens"),
                output_tokens=response.usage_metadata.get("output_tokens")
            )


