import re

from tool_selector import select_tools
from tools.calculator import calculator
from tools.search import search
from tools.trip_planner import build_trip_prompt
from llm_client import get_llm

llm = get_llm()

conversation_history = []


def chat(message: str):
    global conversation_history

    try:
        # Fast calculator detection
        if re.search(r"\d+\s*[\+\-\*/]\s*\d+", message):
            result = calculator(message)

            if result is not None:
                return result

        tools = select_tools(message)

        print("Selected Tools:", tools)

        responses = []

        # Trip Planner
        if "trip" in tools:
            prompt = build_trip_prompt(message)

            trip_response = llm.invoke(prompt)

            responses.append(
                f"🧳 TRIP PLAN\n\n{trip_response.content}"
            )

        # Search
        if "search" in tools:
            search_response = search(message)

            responses.append(
                f"🔎 SEARCH RESULTS\n\n{search_response}"
            )

        # Calculator
        if "calculator" in tools:
            result = calculator(message)

            if result is not None:
                responses.append(
                    f"🧮 CALCULATION\n\n{result}"
                )

        # Return combined tool results
        if responses:
            return "\n\n".join(responses)

        # Default Chat Memory
        conversation_history.append({
            "role": "user",
            "content": message
        })

        prompt = """
You are a helpful AI assistant.

Use the conversation history below to answer.

"""

        for msg in conversation_history:
            prompt += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        response = llm.invoke(prompt)

        ai_response = getattr(
            response,
            "content",
            str(response)
        )

        conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })

        return ai_response

    except Exception as e:
        print("AGENT ERROR:", e)
        return f"Agent Error: {e}"