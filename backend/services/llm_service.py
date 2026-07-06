import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Explicitly load backend/.env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

print("ENV:", env_path)
print("API:", os.getenv("GROQ_API_KEY"))
print("MODEL:", os.getenv("MODEL_NAME"))

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("MODEL_NAME"),
    temperature=0
)


def ask_llm(question: str):
    response = llm.invoke(question)
    return response.content