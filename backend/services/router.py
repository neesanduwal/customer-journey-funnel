from fastapi import APIRouter

from backend.models.chat import ChatRequest
from backend.services.metrics_service import total_revenue
from backend.tools.router_tool import agent

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Customer Journey AI Running"}


@router.get("/revenue")
def revenue():
    return {
        "revenue": float(total_revenue())
    }


@router.post("/chat")
def chat(request: ChatRequest):

    answer = agent(request.question)

    return {
        "answer": answer
    }