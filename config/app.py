from pydantic_settings import SettingsConfigDict
from .milvus import MilvusConfig
from .openai import OpenAIConfig
from .repos import RepoConfig


class AppConfig(MilvusConfig, RepoConfig,OpenAIConfig):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


