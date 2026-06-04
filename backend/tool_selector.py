from llm_client import get_llm

llm = get_llm()

def select_tool(message: str):

    prompt = f"""
You are an AI router.

Choose ONLY one of these tool names:

calculator
search
weather
trip
chat

Message:
{message}

Return ONLY the tool name.
"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()