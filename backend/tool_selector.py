from llm_client import get_llm

llm = get_llm()


def select_tools(message: str):

    prompt = f"""
You are an AI router.

Available tools:

calculator
search
trip
filesystem
chat

A message may require multiple tools.

Examples:

245 * 67
-> calculator

Latest AI news
-> search

Plan a Goa trip
-> trip

Plan a Goa trip and latest travel news
-> trip,search

List files in backend
-> filesystem

Show project files
-> filesystem

Read memory.py
-> filesystem

Open agent.py
-> filesystem

What is my name?
-> chat

My name is Teja
-> chat

Hello
-> chat

Return ONLY comma-separated tool names.

Message:
{message}
"""

    response = llm.invoke(prompt)

    tools = [
        tool.strip().lower()
        for tool in response.content.split(",")
    ]

    print("Router selected:", tools)

    return tools