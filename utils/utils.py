from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedder = NVIDIAEmbeddings(model="nvidia/llama-3.2-nemoretriever-300m-embed-v2")

def generate_embedding(query):
    return embedder.embed_query(query)
