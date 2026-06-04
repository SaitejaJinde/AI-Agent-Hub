from typing import TypedDict

from langgraph.graph import StateGraph

from llm_client import get_llm
from tool_selector import select_tools

from tools.calculator import calculator
from tools.search import search
from tools.trip_planner import build_trip_prompt

llm = get_llm()


class AgentState(TypedDict):
    message: str
    tools: list[str]
    response: str


# Router Node
def router_node(state: AgentState):

    tools = select_tools(
        state["message"]
    )

    print("Selected Tools:", tools)

    return {
        "tools": tools
    }


# Multi Tool Executor
def multi_tool_node(state: AgentState):

    responses = []

    tools = state["tools"]

    # Calculator
    if "calculator" in tools:

        result = calculator(
            state["message"]
        )

        responses.append(
            f"🧮 CALCULATOR\n\n{result}"
        )

    # Search
    if "search" in tools:

        result = search(
            state["message"]
        )

        responses.append(
            f"🔎 SEARCH RESULTS\n\n{result}"
        )

    # Trip Planner
    if "trip" in tools:

        prompt = build_trip_prompt(
            state["message"]
        )

        result = llm.invoke(
            prompt
        )

        responses.append(
            f"🧳 TRIP PLAN\n\n{result.content}"
        )

    # Chat
    if "chat" in tools:

        result = llm.invoke(
            state["message"]
        )

        responses.append(
            result.content
        )

    return {
        "response": "\n\n".join(
            responses
        )
    }


# Build Graph
graph = StateGraph(
    AgentState
)

graph.add_node(
    "router",
    router_node
)

graph.add_node(
    "executor",
    multi_tool_node
)

graph.set_entry_point(
    "router"
)

graph.add_edge(
    "router",
    "executor"
)

graph.set_finish_point(
    "executor"
)

app = graph.compile()