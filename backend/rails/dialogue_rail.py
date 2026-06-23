def check_conversation(history):

    MAX_TURNS = 20

    if len(history) > MAX_TURNS:
        return False

    return True