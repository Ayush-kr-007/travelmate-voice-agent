from google import genai
from backend.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)
