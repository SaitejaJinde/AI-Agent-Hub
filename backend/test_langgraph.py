from langgraph_agent import app

result = app.invoke(
    {
        "message": "245 * 67"
    }
)

print(result)