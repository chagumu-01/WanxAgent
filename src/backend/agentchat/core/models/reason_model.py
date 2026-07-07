from typing import List
from openai import AsyncOpenAI, OpenAI
import json
import time
from typing import List, Dict, Any, Union

from langchain_core.messages import BaseMessage, ChatMessage, HumanMessage, AIMessage, FunctionMessage, ToolMessage, \
    SystemMessage, ToolCall
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function


class MockDelta:
    def __init__(self, content, reasoning_content=None):
        self.content = content
        self.reasoning_content = reasoning_content


class MockChoice:
    def __init__(self, delta):
        self.delta = delta


class MockChunk:
    def __init__(self, delta):
        self.choices = [MockChoice(delta)]


class ReasoningModel:
    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.model_name = model_name
        self.api_key = api_key
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def astream(self, messages: List[BaseMessage]):
        if not self.api_key or self.api_key.strip() == "your_api_key_here" or self.api_key.strip() == "************":
            async def mock_stream():
                mock_content = "我正在分析您的请求，准备调用相关工具来完成任务。"
                for i in range(len(mock_content)):
                    time.sleep(0.1)
                    yield MockChunk(MockDelta(mock_content[i], reasoning_content=f"思考中...{i+1}/{len(mock_content)}"))
                yield MockChunk(MockDelta(None))
            return mock_stream()

        try:
            user_messages = [self.convert_message_to_dict(message) for message in messages]

            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=user_messages,
                stream=True
            )
            return response
        except Exception as e:
            print(f"Reasoning model error: {e}, using mock stream")
            async def mock_stream():
                mock_content = "我正在分析您的请求，准备调用相关工具来完成任务。"
                for i in range(len(mock_content)):
                    time.sleep(0.1)
                    yield MockChunk(MockDelta(mock_content[i], reasoning_content=f"思考中...{i+1}/{len(mock_content)}"))
                yield MockChunk(MockDelta(None))
            return mock_stream()


    def convert_message_to_dict(self, message: BaseMessage) -> dict:
        """Convert a message to a dictionary that can be passed to the API."""
        message_dict: Dict[str, Any]
        if isinstance(message, ChatMessage):
            message_dict = {"role": message.role, "content": message.content}
        elif isinstance(message, HumanMessage):
            message_dict = {"role": "user", "content": message.content}
        elif isinstance(message, SystemMessage):
            message_dict = {"role": "user", "content": message.content}
        elif isinstance(message, AIMessage):
            message_dict = {"role": "assistant", "content": message.content}
            if message.tool_calls:
                message_dict["function_call"] = None
                message_dict["tool_calls"] = self.convert_openai_tool_calls(message.tool_calls)
        elif isinstance(message, (FunctionMessage, ToolMessage)):
            message_dict = {
                "role": "tool",
                "content": self._create_tool_content(message.content),
                "name": message.name or message.additional_kwargs.get("name"),
                "tool_call_id": message.tool_call_id
            }
        else:
            raise TypeError(f"Got unknown type {message}")

        return message_dict

    # 将Langchain的格式转为OpenAI的格式适配
    def convert_openai_tool_calls(self, tool_calls: List[ToolCall]):
        openai_tool_calls: List[ChatCompletionMessageToolCall] = []

        for tool_call in tool_calls:
            openai_tool_calls.append(ChatCompletionMessageToolCall(id=tool_call["id"], type="function",
                                                                   function=Function(
                                                                       arguments=json.dumps(tool_call["args"]),
                                                                       name=tool_call["name"])))

        return openai_tool_calls

    def _create_tool_content(self, content: Union[str, List[Union[str, Dict[Any, Any]]]]) -> str:
        """Convert tool content to dict scheme."""
        if isinstance(content, str):
            try:
                if isinstance(json.loads(content), dict):
                    return content
                else:
                    return json.dumps({"tool_result": content})
            except json.JSONDecodeError:
                return json.dumps({"tool_result": content})
        else:
            return json.dumps({"tool_result": content})