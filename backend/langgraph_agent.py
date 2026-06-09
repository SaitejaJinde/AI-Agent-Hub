from typing import TypedDict
import asyncio

from langgraph.graph import StateGraph

from llm_client import get_llm
from tool_selector import select_tools

from tools.calculator import calculator
from tools.search import search
from tools.trip_planner import build_trip_prompt

from tools.mcp_filesystem import (
    list_directory,
    read_mcp_file
)

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

    # MCP Filesystem
    if "filesystem" in tools:

        message = state["message"].lower()

        if (
            "read" in message
            or "open" in message
            or ".py" in message
            or ".json" in message
            or ".txt" in message
        ):

            file_name = None

            for word in state["message"].split():

                if (
                    word.endswith(".py")
                    or word.endswith(".json")
                    or word.endswith(".txt")
                ):
                    file_name = word
                    break

            if file_name:

                result = asyncio.run(
                    read_mcp_file(
                        file_name
                    )
                )

            else:

                result = (
                    "Please specify a file name."
                )

        else:

            result = asyncio.run(
                list_directory(".")
            )

        responses.append(
            f"📁 MCP FILESYSTEM\n\n{result}"
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