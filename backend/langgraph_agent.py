from typing import TypedDict
import asyncio
import threading
import inspect

from .langgraph.graph import StateGraph

from .llm_client import get_llm
from .tool_selector import select_tools

from .tools.calculator import calculator
from .tools.search import search
from .tools.trip_planner import build_trip_prompt

from .tools.mcp_filesystem import (
    list_directory,
    read_mcp_file
)

from .memory import (
    load_memory,
    save_memory
)

llm = get_llm()

conversation_history = load_memory()


class AgentState(TypedDict):
    message: str
    tools: list[str]
    response: str


# Helper to run coroutines from synchronous code even if an event loop is running
def run_coro_sync(coro):
    """Run a coroutine from sync code. If there's no running loop, use asyncio.run.
    If there is a running loop, run the coroutine in a new thread with its own loop.
    """
    if not inspect.isawaitable(coro):
        return coro

    try:
        # If there's no running loop, this will raise RuntimeError
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        result = {}

        def _run():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result['value'] = new_loop.run_until_complete(coro)
            finally:
                new_loop.close()

        t = threading.Thread(target=_run)
        t.start()
        t.join()
        return result.get('value')


# Safe invoke helper for LLM/tool that may return either a plain string, an object with .content,
# or a coroutine that resolves to one of those.
def safe_invoke(func_or_obj, *args, **kwargs):
    # func_or_obj can be a callable (like llm.invoke) or an object with invoke method
    if hasattr(func_or_obj, "invoke") and callable(func_or_obj.invoke):
        res = func_or_obj.invoke(*args, **kwargs)
    elif callable(func_or_obj):
        res = func_or_obj(*args, **kwargs)
    else:
        # Not callable; return string representation
        return str(func_or_obj)

    # If the result is awaitable, run it synchronously
    if inspect.isawaitable(res):
        res = run_coro_sync(res)

    # If the result is an object with .content, prefer that
    if hasattr(res, "content"):
        return getattr(res, "content")

    return res


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

        # Use safe_invoke to handle sync/async and .content shapes
        result = safe_invoke(llm, prompt)

        responses.append(
            f"🧳 TRIP PLAN\n\n{result}"
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

                cleaned = word.strip().strip('"\'.,;:()[]')

                if (
                    cleaned.endswith(".py")
                    or cleaned.endswith(".json")
                    or cleaned.endswith(".txt")
                ):
                    file_name = cleaned
                    break

            if file_name:

                # read_mcp_file may be async; run safely
                result = run_coro_sync(read_mcp_file(file_name))

            else:

                result = (
                    "Please specify a file name."
                )

        else:

            result = run_coro_sync(list_directory("."))

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

        result = safe_invoke(llm, prompt)

        # Ensure we store a string in memory
        conversation_history.append({
            "role": "assistant",
            "content": str(result)
        })

        save_memory(
            conversation_history
        )

        responses.append(
            str(result)
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
