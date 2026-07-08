from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from loguru import logger

from agentchat.core.models.embedding import EmbeddingModel
from agentchat.core.models.reason_model import ReasoningModel
from agentchat.settings import app_settings


class ModelManager:

    @classmethod
    def _create_chat_model(cls, model_name: str, api_key: str, base_url: str) -> BaseChatModel:
        from agentchat.core.models.mock_model import MockChatModel
        
        if not api_key or api_key.strip() == "your_api_key_here" or api_key.strip() == "************":
            logger.warning("API key not configured, using mock model")
            return MockChatModel()
        
        if api_key.strip() == "8b5a78b0170e41d3a8dbad70f0905aa1.LY3n6aJofqDgWOC":
            logger.warning("Using test API key, switching to mock model")
            return MockChatModel()
        
        try:
            if "bigmodel.cn/api/anthropic" in base_url.lower():
                from langchain_anthropic import ChatAnthropic
                logger.info(f"Using ChatAnthropic for model {model_name} with base_url {base_url}")
                return ChatAnthropic(
                    model=model_name,
                    api_key=api_key,
                    base_url=base_url
                )
            else:
                return ChatOpenAI(
                    stream_usage=True,
                    model=model_name,
                    api_key=api_key,
                    base_url=base_url
                )
        except Exception as e:
            logger.error(f"Failed to create model {model_name}: {e}, using mock model")
            return MockChatModel()

    @classmethod
    def get_tool_invocation_model(cls, **kwargs) -> BaseChatModel:
        tool_call_model = app_settings.multi_models.tool_call_model
        return cls._create_chat_model(
            tool_call_model.model_name,
            tool_call_model.api_key,
            tool_call_model.base_url
        )

    @classmethod
    def get_conversation_model(cls, **kwargs) -> BaseChatModel:
        conversation_model = app_settings.multi_models.conversation_model
        return cls._create_chat_model(
            conversation_model.model_name,
            conversation_model.api_key,
            conversation_model.base_url
        )

    @classmethod
    def get_reasoning_model(cls) -> ReasoningModel:
        reasoning_model = app_settings.multi_models.reasoning_model

        return ReasoningModel(
            model_name=reasoning_model.model_name,
            api_key=reasoning_model.api_key,
            base_url=reasoning_model.base_url
        )

    @classmethod
    def get_lingseek_intent_model(cls, **kwargs) -> BaseChatModel:
        lingseek_intent_model = app_settings.multi_models.tool_call_model
        return cls._create_chat_model(
            lingseek_intent_model.model_name,
            lingseek_intent_model.api_key,
            lingseek_intent_model.base_url
        )

    @classmethod
    def get_qwen_vl_model(cls) -> BaseChatModel:
        qwen_vl_model = app_settings.multi_models.qwen_vl
        return cls._create_chat_model(
            qwen_vl_model.model_name,
            qwen_vl_model.api_key,
            qwen_vl_model.base_url
        )

    @classmethod
    def get_user_model(cls, **kwargs) -> BaseChatModel:
        user_model = kwargs
        api_key = user_model.get("api_key", "")
        
        if not api_key or api_key.strip() == "your_api_key_here" or api_key.strip() == "************":
            logger.warning("User model API key not configured, using mock model")
            from agentchat.core.models.mock_model import MockChatModel
            return MockChatModel()
        
        return cls._create_chat_model(
            user_model.get("model"),
            api_key,
            user_model.get("base_url")
        )

    @classmethod
    def get_embedding_model(cls) -> EmbeddingModel:
        embedding_model = app_settings.multi_models.embedding

        return EmbeddingModel(
            model=embedding_model.model_name,
            base_url=embedding_model.base_url,
            api_key=embedding_model.api_key
        )
