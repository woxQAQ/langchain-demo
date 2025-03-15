import logging
import logging.config
from os import path
import os
import dotenv
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

from modules.embed.models import CommonEmbeddings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

dotenv.load_dotenv()
openapi_base = os.getenv("OPENAI_API_COMPATIBLE_PATH", "https://api.openai.com")
openapi_key = os.getenv("OPENAI_API_KEY")
if openapi_key is None:
    raise Exception("OpenAI API Key not found")

repoPath = os.getenv("TARGET_GITHUB_REPO")
if repoPath is None:
    raise Exception("Target GitHub Repo not found")
outputPath = os.getenv("REPO_OUTPUT_PATH", "./repos")
outputPath = path.abspath(outputPath)

rust_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.RUST)
rust_splitter._chunk_size = 3000
rust_splitter._chunk_overlap = 300

from modules import  stores
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_milvus import Milvus


if not path.exists(outputPath):
    stores.clone_into(
        repoPath, output_path=outputPath
    )


loader = DirectoryLoader(
    outputPath,
    glob="**/*.rs",
    show_progress=True,
    use_multithreading=True,
    loader_cls=TextLoader,
)

docs = loader.load()

rust_docs = rust_splitter.create_documents([d.page_content for d in docs])

logging.info("start embed rust code")


embed_api_path = os.getenv("EMBED_API_PATH")
embed_api_key = os.getenv("EMBED_API_KEY") 
if embed_api_key is None:
    raise Exception("Silicon Flow API Key not found")

embedder = CommonEmbeddings(
    url=embed_api_path,
    model=os.getenv("EMBED_MODELS", "BAAI/bge-large-zh-v1.5"),
    api_key=embed_api_key,
)


store = LocalFileStore("./cache/")

cached_embdder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=embedder,
    namespace=embedder.model,
    document_embedding_cache=store,
    query_embedding_cache=store,
)

res = cached_embdder.embed_query(rust_docs[0].__str__())

db = Milvus(
    embedding_function=cached_embdder,
    connection_args={
        "uri": os.getenv("MILVUS_HOST", "tcp://localhost:19530"),
    },
).from_documents([rust_docs[0]], cached_embdder)
