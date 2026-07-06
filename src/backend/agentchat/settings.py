import yaml
import os
import re
from typing import Literal, Optional
from loguru import logger
from types import SimpleNamespace
from pydantic.v1 import BaseSettings, Field

from agentchat.schema.common import MultiModels, ModelConfig, Tools, Rag, StorageConfig


def coerce_type(value):
    if isinstance(value, str):
        value = value.strip()
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    return value


def substitute_env_variables(data):
    if isinstance(data, str):
        pattern = r'\$\{(\w+)(:-[^}]*)?\}'
        def replace_match(match):
            var_name = match.group(1)
            default = match.group(2)[2:] if match.group(2) else ''
            return os.environ.get(var_name, default)
        result = re.sub(pattern, replace_match, data)
        return coerce_type(result)
    elif isinstance(data, dict):
        return {key: substitute_env_variables(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [substitute_env_variables(item) for item in data]
    else:
        return data


class Settings(BaseSettings):
    redis: dict = {}
    mysql: dict = {}
    server: dict = {}
    langfuse: dict = {}
    whitelist_paths: list = []
    wechat_config: dict = {}
    default_config: dict = {}

    rag: Optional[Rag] = None
    tools: Optional[Tools] = None
    storage: Optional[StorageConfig] = None
    multi_models: Optional[MultiModels] = None


app_settings = Settings()


async def initialize_app_settings(file_path: str = None):
    global app_settings

    file_path = file_path or "agentchat/config.yaml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data is None:
                logger.error("YAML 文件解析为空")
                return

            data = substitute_env_variables(data)

            if "multi_models" in data:
                data["multi_models"] = MultiModels(**data["multi_models"])

            if "tools" in data:
                data["tools"] = Tools(**data["tools"])

            if "rag" in data:
                data["rag"] = Rag(**data["rag"])

            if "storage" in data:
                data["storage"] = StorageConfig(**data["storage"])

            for key, value in data.items():
                setattr(app_settings, key, value)
    except Exception as e:
        logger.error(f"Yaml file loading error: {e}")