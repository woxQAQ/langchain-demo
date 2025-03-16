import json
import logging
import logging.config
from os import path
import regex
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_milvus import Milvus

from config import app_config
from config.app import AppConfig
from modules import stores
from embed.models import CommonEmbeddings

def setup() -> AppConfig:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )
    app_config.model_dump()
    
    return app_config

rust_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.RUST)
rust_splitter._chunk_size = 3000
rust_splitter._chunk_overlap = 300

config = setup()
repoPath = config.REPO_PATH
if repoPath == "":
    raise Exception("Target GitHub Repo not found")

outputPath = config.REPO_OUTPUT_PATH
if outputPath is None:
    raise Exception("Output Path not found") 
outputPath = path.abspath(outputPath)
if not path.exists(outputPath):
    stores.clone_into(repoPath, output_path=outputPath)


loader = DirectoryLoader(
    outputPath,
    glob="**/*.rs",
    show_progress=True,
    use_multithreading=True,
    loader_cls=TextLoader,
)

docs = loader.load()

with open("docs.json", "w") as f:
    json.dump([d.metadata for d in docs], f)

new_docs = []

for d in docs:
    source = str(d.metadata.get("source"))
    if (
        regex.match(pattern=r"(.*)\/dt-tests\/(.*)|.*\/docs\/(.*)", string=source)
        is None
    ):
        new_docs.append(d)

for d in new_docs:
    print(d.metadata.get("source"))
docs = loader.load()

rust_docs = rust_splitter.create_documents([d.page_content for d in docs])

logging.info("start embed rust code")

embedder = CommonEmbeddings(
    url=config.EMBED_API_PATH,
    model=config.EMBED_MODELS,
    # model=os.getenv("EMBED_MODELS", "BAAI/bge-large-zh-v1.5"),
    api_key=config.EMBED_API_KEY,
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
        "uri": config.MILVUS_DSN,
    },
).from_documents([rust_docs[0]], cached_embdder)
