from collections import defaultdict

MAX_MESSAGES = 10

conversation_store = defaultdict(list)


def add_message(session_id, role, content):

    conversation_store[session_id].append({
        "role": role,
        "content": content
    })

    conversation_store[session_id] = (
        conversation_store[session_id][-MAX_MESSAGES:]
    )


def get_history(session_id):

    return conversation_store[session_id]


def clear_history(session_id):

    if session_id in conversation_store:
        del conversation_store[session_id]