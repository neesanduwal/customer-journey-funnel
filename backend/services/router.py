from fastapi import APIRouter

from backend.models.chat import ChatRequest
from backend.services.llm_service import ask_llm
from backend.services.metrics_service import (
    total_revenue,
    running_total,
    wow,
    yoy,
)

router = APIRouter()


@router.get("/")
def home():

    return {
        "message": "Customer Journey AI Running"
    }


@router.post("/chat")
def chat(request: ChatRequest):

    question = request.question.lower()

    # ----------------------------------
    # TOTAL REVENUE
    # ----------------------------------

    if "revenue" in question:

        revenue, snapshot = total_revenue()

        prompt = f"""
        Total Revenue : {revenue}

        Snapshot Used : {snapshot}

        Explain this in a professional business tone.
        Mention the snapshot date.
        """

        answer = ask_llm(prompt)

        return {
            "answer": answer
        }

    # ----------------------------------
    # RUNNING TOTAL
    # ----------------------------------

    elif "running" in question:

        total, date = running_total()

        prompt = f"""
        Running Revenue : {total}

        Snapshot : {date}

        Explain the running total in business language.
        Mention the snapshot date.
        """

        answer = ask_llm(prompt)

        return {
            "answer": answer
        }

    # ----------------------------------
    # WEEK OVER WEEK
    # ----------------------------------

    elif "week" in question or "wow" in question:

        row = wow()

        prompt = f"""
        Current Revenue : {row['revenue']}

        Previous Week : {row['last_week']}

        Week over Week Difference : {row['wow_difference']}

        Snapshot : {row['full_date']}

        Explain the weekly performance.
        Mention the snapshot.
        """

        answer = ask_llm(prompt)

        return {
            "answer": answer
        }

    # ----------------------------------
    # YEAR OVER YEAR
    # ----------------------------------

    elif "year" in question or "yoy" in question:

        row = yoy()

        prompt = f"""
        Current Revenue : {row['revenue']}

        Last Year Revenue : {row['last_year']}

        YoY Difference : {row['yoy_difference']}

        Snapshot : {row['full_date']}

        Explain the yearly comparison.
        Mention the snapshot.
        """

        answer = ask_llm(prompt)

        return {
            "answer": answer
        }

    # ----------------------------------
    # GENERAL CHAT
    # ----------------------------------

    else:

        answer = ask_llm(request.question)

        return {
            "answer": answer
        }