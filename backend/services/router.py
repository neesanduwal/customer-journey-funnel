from fastapi import APIRouter

from backend.models.chat import ChatRequest
from backend.agent.analytics_agent import analytics_agent
from backend.tools.mcp_metrics_tool import execute_metrics_tool

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


@router.post("/mcp/metrics")
def metrics_tool(request: ChatRequest):
    result = execute_metrics_tool(request.question)
    return result