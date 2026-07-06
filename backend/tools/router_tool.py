from backend.tools.revenue_tool import get_total_revenue
from backend.tools.orders_tool import get_total_orders
from backend.tools.running_total_tool import get_running_total
from backend.tools.wow_tool import get_wow
from backend.tools.yoy_tool import get_yoy

from backend.services.llm_service import ask_llm


def agent(question: str):

    q = question.lower()

    if "revenue" in q:

        revenue = get_total_revenue()

        prompt = f"""
        Total Revenue = {revenue}

        User Question:
        {question}

        Explain this in business language.
        """

        return ask_llm(prompt)

    elif "order" in q:

        orders = get_total_orders()

        prompt = f"""
        Total Orders = {orders}

        User Question:
        {question}

        Explain this.
        """

        return ask_llm(prompt)

    elif "running" in q:

        value = get_running_total()

        prompt = f"""
        Running Revenue = {value}

        User Question:
        {question}
        """

        return ask_llm(prompt)

    elif "week" in q or "wow" in q:

        value = get_wow()

        prompt = f"""
        Week over Week Difference = {value}

        User Question:
        {question}
        """

        return ask_llm(prompt)

    elif "year" in q or "yoy" in q:

        value = get_yoy()

        prompt = f"""
        Year over Year Difference = {value}

        User Question:
        {question}
        """

        return ask_llm(prompt)

    else:
        return ask_llm(question)