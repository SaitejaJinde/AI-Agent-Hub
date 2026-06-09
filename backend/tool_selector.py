def select_tools(message):

    message = message.lower()

    tools = []

    if any(op in message for op in ["+", "-", "*", "/"]):
        tools.append("calculator")

    if any(word in message for word in [
        "trip",
        "travel",
        "itinerary",
        "vacation"
    ]):
        tools.append("trip")

    if any(word in message for word in [
        "file",
        "folder",
        "directory",
        ".py",
        ".json",
        "read",
        "open"
    ]):
        tools.append("filesystem")

    if not tools:
        tools.append("chat")

    return tools