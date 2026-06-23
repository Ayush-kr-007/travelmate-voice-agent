ALLOWED_TOOLS = [
    "search_flights"
]

def validate_tool(tool_name: str):

    return tool_name in ALLOWED_TOOLS