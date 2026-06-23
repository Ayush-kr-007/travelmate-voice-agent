def validate_tool_input(data):

    if len(str(data)) > 500:
        return False

    return True