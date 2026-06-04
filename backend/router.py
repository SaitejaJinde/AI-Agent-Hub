def detect_intent(message: str):

    message = message.lower()

    if any(op in message for op in ["+", "-", "*", "/"]):
        return "calculator"

    if any(word in message for word in [
        "trip",
        "travel",
        "itinerary",
        "vacation",
        "holiday"
    ]):
        return "trip"

    if any(word in message for word in [
        "news",
        "latest",
        "search"
    ]):
        return "search"

    if any(word in message for word in [
        "weather",
        "temperature",
        "rain"
    ]):
        return "weather"

    return "chat"