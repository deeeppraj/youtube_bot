from utils.transciptextract import load_language,load_data
from utils.translator import detect_language,translate
from utils.chunker import split
from utils.vectorstore import vecstor
from functools import lru_cache
from utils.model import chat
from dotenv import load_dotenv
import asyncio

@lru_cache(maxsize=20)
def build_retriver(id:str):
    lang = load_language(id)
    if lang[0] == "en":
        raw = load_data(id=id,lang=lang[0])
        a = split(raw)
        data = "".join(a)
    else:
        raw = load_data(id,lang=lang[0])
        chunks = split(raw)
        data = asyncio.run(translate(text = chunks))
    
    vectorstore = vecstor(text=data)
    retriver = vectorstore.as_retriever(
        search_type = "mmr",
        search_kwargs = {"k" : 5}
    )
    return retriver

model = chat()

def mychain(id):
    retriver = build_retriver(id)
    return model,retriver




