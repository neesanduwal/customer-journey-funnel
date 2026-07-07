from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from backend.services.llm_service import llm

from backend.tools.revenue_tool import get_revenue
from backend.tools.orders_tool import get_orders
from backend.tools.running_total_tool import get_running_total
from backend.tools.wow_tool import get_wow
from backend.tools.yoy_tool import get_yoy


tools = [

    Tool(
        name="Revenue",
        func=get_revenue,
        description="Returns total revenue."
    ),

    Tool(
        name="Orders",
        func=get_orders,
        description="Returns total orders."
    ),

    Tool(
        name="Running Total",
        func=get_running_total,
        description="Returns running revenue."
    ),

    Tool(
        name="Week Over Week",
        func=get_wow,
        description="Returns WoW revenue metrics."
    ),

    Tool(
        name="Year Over Year",
        func=get_yoy,
        description="Returns YoY revenue metrics."
    )

]


agent = initialize_agent(

    tools=tools,

    llm=llm,

    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,

    verbose=True,

    handle_parsing_errors=True

)


def data_agent(question):

    return agent.run(question)