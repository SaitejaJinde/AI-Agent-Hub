from llm_client import get_llm

llm = get_llm()

def search(query: str):
    try:
        prompt = f"""
Provide a concise web-style summary for:

{query}

Include:
1. Key points
2. Recent developments if known
3. Short summary
"""

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:
        return f"Search error: {e}"