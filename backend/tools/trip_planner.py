from prompts import TRIP_PLANNER_PROMPT

def build_trip_prompt(query: str):
    return TRIP_PLANNER_PROMPT.format(
        query=query
    )