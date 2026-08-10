from .langgraph_agent import app


def chat(message: str):

    result = app.invoke(
        {
            "message": message
        }
    )

    # Safely handle multiple possible return shapes from app.invoke
    try:
        if isinstance(result, dict):
            return result.get("response", str(result))
        elif hasattr(result, "content"):
            return getattr(result, "content")
        else:
            return str(result)
    except Exception:
        # Fallback to string conversion if unexpected object
        return str(result)
