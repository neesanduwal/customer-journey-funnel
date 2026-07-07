from fastapi import APIRouter

from backend.models.chat import ChatRequest
from backend.agent.analytics_agent import analytics_agent

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Customer Journey AI Running"
    }


@router.post("/chat")
def chat(request: ChatRequest):

    answer = analytics_agent(request.question)

    return {
        "answer": answer
    }