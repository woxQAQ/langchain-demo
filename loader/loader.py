from typing import Iterable
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class DirectoryLoader(BaseLoader):
    file_path: str
    def __init__(
        self,
        file_path: str,
    )->None:
        self.file_path = file_path
    
    def lazy_load(self) -> Iterable[Document]:
        line_number = 0
        with open(self.file_path, "r") as f:
            for line in f:
                yield Document(page_content=line, metadata={"source": self.file_path})
                line_number += 1

