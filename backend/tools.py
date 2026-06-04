from langchain.tools import Tool

def calculator_tool(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

calculator = Tool(
    name="Calculator",
    func=calculator_tool,
    description="Useful for solving math calculations."
)