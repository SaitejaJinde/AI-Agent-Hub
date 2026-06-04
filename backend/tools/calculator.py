def calculator(expression: str):
    try:
        return str(eval(expression))
    except:
        return None