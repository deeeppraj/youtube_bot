from functools import lru_cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.pipeline import mychain       
from utils.parser import parser            
from finalchain import final_chain         


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoadRequest(BaseModel):
    videoId: str


class ChatRequest(BaseModel):
    videoId: str
    query: str


@lru_cache(maxsize=20)
def get_chain(video_id: str):
    """
    Build + cache the RAG chain for a given video.
    Heavy pipeline (transcript, translate, vectorstore) runs ONCE per video_id
    while the server is alive.
    """
    myparser = parser()
    model, retriever = mychain(video_id)
    chain = final_chain(model, retriever, myparser)
    return chain


@app.get("/")
def root():
    return {"status": "ok", "message": "YouTube RAG backend running"}


@app.post("/load-transcript")
def load_transcript(payload: LoadRequest):
    video_id = payload.videoId
    _ = get_chain(video_id)  
    return {"status": "ok", "message": f"Transcript for {video_id} loaded"}


@app.post("/chat")
def chat(payload: ChatRequest):
    video_id = payload.videoId
    query = payload.query

    chain = get_chain(video_id)
    result = chain.invoke(query)

    answer = getattr(result, "answer", str(result))

    return {"response": answer}
