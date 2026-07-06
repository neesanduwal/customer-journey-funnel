from fastapi import APIRouter

from backend.models.chat import ChatRequest
from backend.services.llm_service import ask_llm
from backend.services.metrics_service import total_revenue

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Customer Journey AI Backend Running"
    }


@router.get("/revenue")
def revenue():

    return {
        "revenue": float(total_revenue())
    }


@router.post("/chat")
def chat(request: ChatRequest):

    answer = ask_llm(request.question)

    return {
        "answer": answer
    }