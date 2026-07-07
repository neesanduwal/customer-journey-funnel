from backend.services.llm_service import ask_llm

from backend.tools.revenue_tool import get_revenue
from backend.tools.orders_tool import get_orders
from backend.tools.running_total_tool import get_running_total
from backend.tools.wow_tool import get_wow
from backend.tools.yoy_tool import get_yoy


def analytics_agent(question: str):

    q = question.lower()

    if "revenue" in q and "running" not in q:
        return get_revenue()

    elif "order" in q:
        return get_orders()

    elif "running" in q:
        return get_running_total()

    elif "week" in q or "wow" in q:
        return get_wow()

    elif "year" in q or "yoy" in q:
        return get_yoy()

    else:
        return ask_llm(question)