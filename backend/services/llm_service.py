import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Explicitly load the .env from the project root
env_path = Path(__file__).resolve().parents[2] / ".env"
print("Loading .env from:", env_path)

load_dotenv(env_path)

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("MODEL_NAME")

print("API KEY:", repr(api_key))
print("MODEL:", repr(model))

if api_key is None:
    raise Exception("GROQ_API_KEY not found")

if model is None:
    raise Exception("MODEL_NAME not found")

llm = ChatGroq(
    api_key=api_key,
    model=model,
    temperature=0,
)


def ask_llm(question: str):
    return llm.invoke(question).content