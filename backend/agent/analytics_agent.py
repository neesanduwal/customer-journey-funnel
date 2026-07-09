import re

from backend.services.llm_service import ask_llm

from backend.tools.revenue_tool import get_revenue
from backend.tools.orders_tool import get_orders
from backend.tools.running_total_tool import get_running_total
from backend.tools.wow_tool import get_wow
from backend.tools.yoy_tool import get_yoy


def analytics_agent(question: str):

    q = question.lower()

    dates = re.findall(r"\d{4}-\d{2}-\d{2}", question)
    years = re.findall(r"\b20\d{2}\b", question)

    date = dates[0] if dates else None

    # =====================================================
    # Revenue
    # =====================================================

    if "revenue" in q and "running" not in q:

        # Revenue supports either a date or a year
        if not dates and not years:
            return "Please provide a date (YYYY-MM-DD) or a year."

        return get_revenue(question)

    # =====================================================
    # Orders
    # =====================================================

    elif "order" in q:

        if not date:
            return "Please provide a date in YYYY-MM-DD format."

        return get_orders(date)

    # =====================================================
    # Running Total
    # =====================================================

    elif "running" in q:

        if not date:
            return "Please provide a date in YYYY-MM-DD format."

        return get_running_total(date)

    # =====================================================
    # Week over Week
    # =====================================================

    elif "wow" in q or "week" in q:

        if not date:
            return "Please provide a date in YYYY-MM-DD format."

        return get_wow(date)

    # =====================================================
    # Year over Year
    # =====================================================

    elif (
        "yoy" in q
        or "year over year" in q
        or ("compare" in q and (len(years) >= 2 or len(dates) >= 2))
    ):

        if not dates and not years:
            return "Please provide one date, two dates, or two years."

        return get_yoy(question)

    # =====================================================
    # Default LLM
    # =====================================================

    return ask_llm(question)