from llm_client import get_llm

llm = get_llm()


def select_tools(message: str):

    prompt = f"""
You are an AI router.

Available tools:

calculator
search
trip
chat

A message may require multiple tools.

Examples:

Plan a Goa trip -> trip

Latest AI news -> search

Plan a Goa trip and latest travel news -> trip,search

245 * 67 -> calculator

Hello -> chat

Return ONLY comma-separated tool names.

Message:
{message}
"""

    response = llm.invoke(prompt)

    return [
        tool.strip().lower()
        for tool in response.content.split(",")
    ]