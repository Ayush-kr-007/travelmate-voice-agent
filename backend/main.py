from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.agent.state import clear_history

from backend.rails.input_rail import (
    check_input,
    handle_input_result
)

from backend.rails.output_rail import safe_output

from backend.agent.travel_agent import (
    generate_travel_response
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str
class ResetRequest(BaseModel):
    session_id: str

@app.get("/")
async def root():

    return {
        "status": "running"
    }


@app.post("/chat")
async def chat(req: ChatRequest):

    result = check_input(req.message)

    allowed, rail_response = handle_input_result(result)

    if not allowed:

        return {
            "response": rail_response,
            "blocked": True
        }

    answer = generate_travel_response(
        req.message,
        req.session_id
    )
    answer = safe_output(
        answer
    )

    return {
        "response": answer,
        "blocked": False
    }




@app.post("/reset")
async def reset_chat(req: ResetRequest):

    clear_history(req.session_id)

    return {
        "status": "memory cleared"
    }