import logging
import os
from typing import List

import requests

from langchain_core.embeddings import Embeddings


class CommonEmbeddings(Embeddings):
    model = ""
    api_key = ""
    __url = ""

    def __init__(self, url, model, api_key):
        self.__url = url
        self.model = model
        self.api_key = api_key

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        try:
            l = []
            for d in texts:
                res = self.__query(d)
                logging.info(f"res: {res.json()}")
                l.append(res.json()['data'][0]['embedding'])
            return l
        except Exception as e:
            logging.error(f"Error: {e}") 
            return []

    def embed_query(self, text: str) -> List[float]:
        try:
            res = self.__query(text).json()
            return res['data'][0]['embedding']
        except Exception as e:
            logging.error(f"Error: {e}")
            return []

    def __query(self, input) -> requests.Response:
        logging.info(f"test: {input}")
        payload = {"model": self.model, "input": input, "encoding_format": "float"}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(self.__url, json=payload, headers=headers)
        return response

    # def aembed_documents(self,texts: List[str]) -> List[List[float]]:

    # def aembed_query(self,text: str) -> List[float]:


token = os.getenv("SILICON_FLOW_API_KEY")
model = os.getenv("EMBED_MODELS", "BAAI/bge-large-zh-v1.5")

if token is None:
    raise Exception("Silicon Flow API Key not found")

url = "https://api.siliconflow.cn/v1/embeddings"


def create_embedding(text: str):
    payload = {"model": model, "input": text, "encoding_format": "float"}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    logging.info(f"model: {model}, token: {token}")
    response = requests.post(url, json=payload, headers=headers)
    logging.info(response)
    return response.json()["data"]
