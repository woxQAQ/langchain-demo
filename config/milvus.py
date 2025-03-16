from pydantic import Field
from pydantic_settings import BaseSettings

class MilvusConfig(BaseSettings):
    MILVUS_DSN : str = Field(
        default="tcp://localhost:19530",
        description="Milvus DSN",
    )

    MILVUS_COLLECTION_NAME: str = Field(
        default="langchain",
        description="Milvus Collection Name",
    )