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
    tool: str
    response: str


# Router Node
def router_node(state: AgentState):

    tools = select_tools(
        state["message"]
    )

    tool = tools[0]

    return {
        "tool": tool
    }


# Chat Node
def chat_node(state: AgentState):

    response = llm.invoke(
        state["message"]
    )

    return {
        "response": response.content
    }


# Calculator Node
def calculator_node(state: AgentState):

    result = calculator(
        state["message"]
    )

    return {
        "response": str(result)
    }


# Search Node
def search_node(state: AgentState):

    result = search(
        state["message"]
    )

    return {
        "response": result
    }


# Trip Planner Node
def trip_node(state: AgentState):

    prompt = build_trip_prompt(
        state["message"]
    )

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


# Routing Logic
def route_tool(state: AgentState):

    return state["tool"]


graph = StateGraph(AgentState)

# Nodes
graph.add_node(
    "router",
    router_node
)

graph.add_node(
    "chat",
    chat_node
)

graph.add_node(
    "calculator",
    calculator_node
)

graph.add_node(
    "search",
    search_node
)

graph.add_node(
    "trip",
    trip_node
)

# Entry Point
graph.set_entry_point(
    "router"
)

# Conditional Routing
graph.add_conditional_edges(
    "router",
    route_tool,
    {
        "calculator": "calculator",
        "search": "search",
        "trip": "trip",
        "chat": "chat",
    },
)

# Finish Points
graph.set_finish_point(
    "calculator"
)

graph.set_finish_point(
    "search"
)

graph.set_finish_point(
    "trip"
)

graph.set_finish_point(
    "chat"
)

app = graph.compile()