conversation_history = []

MAX_MESSAGES = 10


def add_message(role, content):
    global conversation_history

    conversation_history.append({
        "role": role,
        "content": content
    })

    conversation_history = conversation_history[-MAX_MESSAGES:]


def get_history():
    return conversation_history


def clear_history():
    global conversation_history
    conversation_history = []