from fastapi import FastAPI
from pydantic import BaseModel
from memory import save_message, get_memory
import httpx

app = FastAPI()

class Message(BaseModel):
    text: str

# You can later replace this with HuggingFace/OpenRouter
async def call_llm(prompt: str) -> str:
    response = f"I'm here for you! You said: {prompt}"
    return response

@app.post("/talk")
async def talk(msg: Message):
    user_input = msg.text
    save_message(user_input, source="user")

    reply = await call_llm(user_input)
    save_message(reply, source="jarvis")

    return {"reply": reply}
