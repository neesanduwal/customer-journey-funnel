import re

from backend.services.llm_service import ask_llm

from backend.tools.revenue_tool import get_revenue
from backend.tools.orders_tool import get_orders
from backend.tools.running_total_tool import get_running_total
from backend.tools.wow_tool import get_wow
from backend.tools.yoy_tool import get_yoy


def analytics_agent(question: str):

    q = question.lower()

    date_match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", q)
    date = date_match.group(0) if date_match else None

    # Revenue / Running / Orders / WoW require a date
    if (
        ("revenue" in q or "running" in q or "wow" in q or "order" in q)
        and "yoy" not in q
        and "year" not in q
        and date is None
    ):
        return "Please provide a date in YYYY-MM-DD format."

    if "revenue" in q and "running" not in q:
        return get_revenue(date)

    elif "order" in q:
        return get_orders(date)

    elif "running" in q:
        return get_running_total(date)

    elif "week" in q or "wow" in q:
        return get_wow(date)

    elif "yoy" in q or "year" in q:
        return get_yoy(question)

    return ask_llm(question)