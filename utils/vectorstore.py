from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from utils.chunker import split
from utils.utils import embedder

def vecstor(text:str):
    chunk = split(text)
    docs = [Document(page_content = chunks) for chunks in chunk]
    vectorstore = FAISS.from_documents(
        documents=docs,
        embedding=embedder
    )

    return vectorstore
