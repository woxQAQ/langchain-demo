from pydantic import Field
from pydantic_settings import BaseSettings


class RepoConfig(BaseSettings):
    REPO_PATH: str = Field(
        default="",
        description="Target Path to read",
    )

    REPO_OUTPUT_PATH: str = Field(
        default="./repos",
        description="Output Path to save",
    )