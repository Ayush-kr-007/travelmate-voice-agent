BANNED_PHRASES = [
    "system prompt",
    "developer mode",
    "internal instructions",
    "hidden prompt"
]


def validate_output(text: str):

    lower = text.lower()

    for phrase in BANNED_PHRASES:

        if phrase in lower:
            return False

    return True


def safe_output(text: str):

    if validate_output(text):
        return text

    return (
        "I'm here to help with travel planning, flights, "
        "hotels, and destinations."
    )