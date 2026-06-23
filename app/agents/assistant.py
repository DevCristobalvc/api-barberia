from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import TypedDict, Annotated
import operator

from app.config.settings import settings
from app.tools.availability import get_availability
from app.tools.bookings import create_booking, cancel_booking, move_booking, list_today
from app.tools.customers import search_customer, create_customer, update_customer
from app.tools.shop_info import get_shop_information, list_services, list_barbers, block_schedule, unblock_schedule

TOOLS = [
    get_availability,
    create_booking,
    cancel_booking,
    move_booking,
    list_today,
    search_customer,
    create_customer,
    update_customer,
    get_shop_information,
    list_services,
    list_barbers,
    block_schedule,
    unblock_schedule,
]


class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    shop_id: str
    phone: str
    system_prompt: str


def build_graph() -> StateGraph:
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.4,
        max_tokens=512,
    ).bind_tools(TOOLS)

    tool_node = ToolNode(TOOLS)

    def call_model(state: AgentState) -> dict:
        messages = [SystemMessage(content=state["system_prompt"])] + state["messages"]
        response = llm.invoke(messages)
        return {"messages": [response]}

    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


assistant_graph = build_graph()
