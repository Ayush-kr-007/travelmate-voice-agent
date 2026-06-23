import os
import time
from groq import Groq
from google.genai import errors

from backend.prompt import TRAVEL_SYSTEM_PROMPT
from backend.services.gemini_client import client as gemini_client
from backend.agent.state import (
    add_message,
    get_history
)

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def generate_travel_response(
    user_message: str,
    session_id: str
):

    # Only keep recent context
    history = get_history(session_id)[-6:]

    conversation = ""

    for msg in history:
        conversation += (
            f"{msg['role']}: {msg['content']}\n"
        )

    prompt = f"""
{TRAVEL_SYSTEM_PROMPT}

Conversation History:
{conversation}

User:
{user_message}

Assistant:
"""

    try:

        start = time.time()

        print("Processing with Groq...")

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=120
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        print(
            f"Groq latency: "
            f"{time.time() - start:.2f}s"
        )

        add_message(
            session_id,
            "user",
            user_message
        )

        add_message(
            session_id,
            "assistant",
            answer
        )

        return answer

    except Exception as groq_error:

        print(
            f"Groq Error: {groq_error}"
        )

        models_to_try = [
            "gemini-2.5-flash-lite"
        ]

        for model_name in models_to_try:

            try:

                start = time.time()

                print(
                    f"Trying Gemini "
                    f"({model_name})"
                )

                response_stream = (
                    gemini_client.models
                    .generate_content_stream(
                        model=model_name,
                        contents=prompt
                    )
                )

                answer = ""

                for chunk in response_stream:

                    if chunk.text:
                        answer += chunk.text

                print(
                    f"Gemini latency: "
                    f"{time.time() - start:.2f}s"
                )

                # FIXED
                add_message(
                    session_id,
                    "user",
                    user_message
                )

                add_message(
                    session_id,
                    "assistant",
                    answer
                )

                return answer

            except errors.APIError as gemini_error:

                print(
                    f"Gemini API Error: "
                    f"{gemini_error}"
                )

                continue

            except Exception as e:

                print(
                    f"Gemini Error: {e}"
                )

                continue

    return (
        "Sorry, I'm having trouble accessing "
        "travel information right now."
    )