import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv("backend/.env")

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("MODEL_NAME"),
    temperature=0
)


def ask_llm(question: str):

    response = llm.invoke(question)

    return response.content