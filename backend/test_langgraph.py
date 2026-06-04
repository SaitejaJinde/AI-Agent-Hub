from langgraph_agent import app

result = app.invoke(
    {
        "message":
        "Plan a Goa trip and give me latest travel news"
    }
)

print(result["response"])