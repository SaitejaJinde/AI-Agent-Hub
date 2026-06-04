from typing import TypedDict

from langgraph.graph import StateGraph

from llm_client import get_llm
from tool_selector import select_tools

from tools.calculator import calculator
from tools.search import search
from tools.trip_planner import build_trip_prompt

from memory import (
    load_memory,
    save_memory
)

llm = get_llm()

conversation_history = load_memory()


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

    global conversation_history

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

    # Chat + Persistent Memory
    if "chat" in tools:

        conversation_history.append({
            "role": "user",
            "content": state["message"]
        })

        prompt = """
You are a helpful AI assistant.

Use the conversation history below.

"""

        for msg in conversation_history:

            prompt += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        result = llm.invoke(
            prompt
        )

        conversation_history.append({
            "role": "assistant",
            "content": result.content
        })

        save_memory(
            conversation_history
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