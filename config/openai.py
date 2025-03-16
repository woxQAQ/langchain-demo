from pydantic import Field
from pydantic_settings import BaseSettings

class OpenAIConfig(BaseSettings):
    OPENAI_API_COMPATIBLE_PATH: str = Field(
        default="https://api.openai.com",
        description="OpenAI API Compatible Path",
    ) 

    OPENAI_API_COMPATIBLE_API_KEY: str = Field(
        default="",
        description="OpenAI API Compatible API Key",
    )

    EMBED_API_PATH : str = Field(
        default="",
        description="Embed Model API Path",
    )

    EMBED_API_KEY: str = Field(
        default="",
        description="Embed Model API Key",
    )

    EMBED_MODELS: str = Field(
        default="",
        description="Embed Models",
    )