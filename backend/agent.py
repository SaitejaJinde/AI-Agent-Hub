from langgraph_agent import app


def chat(message: str):

    result = app.invoke(
        {
            "message": message
        }
    )

    return result["response"]