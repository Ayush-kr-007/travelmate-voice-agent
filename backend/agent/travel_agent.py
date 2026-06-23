import os
import time
from groq import Groq
from google.genai import errors
from backend.prompt import TRAVEL_SYSTEM_PROMPT
from backend.services.gemini_client import client as gemini_client
from backend.agent.state import add_message, get_history

# Initialize the Groq client separately
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_travel_response(user_message: str):
    # 1. Fetch and compile conversation history
    history = get_history()
    conversation = ""
    for msg in history:
        conversation += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
{TRAVEL_SYSTEM_PROMPT}

Conversation History:
{conversation}

User:
{user_message}

Assistant:
"""

    # 2. Try Primary Pipeline: Groq (Llama 3.3 70B)
    try:
        print("Processing with Groq (Llama 3.3)...")
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=120
        )
        answer = response.choices[0].message.content
        
        # Save history on success
        add_message("user", user_message)
        add_message("assistant", answer)
        return answer

    except Exception as groq_error:
        print(f"Groq Error: {groq_error}. Dropping back to Gemini fallback...")
        
        # 3. Fallback Pipeline: Gemini (if Groq hits a rate limit or fails)
        models_to_try = ["gemini-2.5-flash-lite", "gemini-3.5-flash"]
        
        for model_name in models_to_try:
            try:
                print(f"Trying Gemini Fallback ({model_name})...")
                response_stream = gemini_client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt
                )
                
                answer = ""
                for chunk in response_stream:
                    if chunk.text:
                        answer += chunk.text
                
                add_message("user", user_message)
                add_message("assistant", answer)
                return answer
                
            except errors.APIError as gemini_error:
                if gemini_error.code == 503:
                    continue
                print(f" Gemini API Error: {gemini_error}")
                break
            except Exception as e:
                print(f" Gemini Unexpected Error: {e}")
                break

    return (
        "Sorry, I'm having trouble accessing travel information "
        "right now. Please try again shortly."
    )
