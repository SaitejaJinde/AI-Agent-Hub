from tool_selector import select_tool
from tools.calculator import calculator
from tools.search import search
from tools.weather import weather
from tools.trip_planner import build_trip_prompt
from llm_client import get_llm

llm = get_llm()

conversation_history = []


def chat(message: str):
    global conversation_history

    try:
        intent = select_tool(message)

        print(f"Selected Tool: {intent}")

        # Calculator Tool
        if intent == "calculator":
            result = calculator(message)

            if result is not None:
                return result

        # Search Tool
        if intent == "search":
            return search(message)

        # Weather Tool
        if intent == "weather":
            return weather(message)

        # Trip Planner Tool
        if intent == "trip":
            prompt = build_trip_prompt(message)

            response = llm.invoke(prompt)

            return getattr(
                response,
                "content",
                str(response)
            )

        # Default Chat
        conversation_history.append({
            "role": "user",
            "content": message
        })

        prompt = ""

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
        return f"Agent Error: {e}"