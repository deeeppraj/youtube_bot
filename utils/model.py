from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()

def chat():
    model= ChatGroq(
        model= "qwen/qwen3-32b",
        temperature= 0.4
    )
    return model

