from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from memory import save_message, get_memory
from TTS.api import TTS
import httpx
import uuid
import os

app = FastAPI()

class Message(BaseModel):
    text: str

LLM_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def call_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    async with httpx.AsyncClient() as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)


        return r.json()["choices"][0]["message"]["content"]
    

@app.get("/")
def root():
    return {"message": "Jarvis is up and running 🚀"}

@app.post("/talk")
async def talk(msg: Message):
    user_input = msg.text
    save_message(user_input, source="user")

    reply = await call_llm(user_input)
    save_message(reply, source="jarvis")

    return {"reply": reply}

# ADD THIS for voice output
tts = TTS(model_name="tts_models/en/vctk/vits", gpu=False)

@app.post("/speak")
def speak(text: str = Form(...)):
    output_dir = os.path.join(os.getcwd(), "temp_audio")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{uuid.uuid4()}.wav")

    try:
        tts.tts_to_file(text=text, speaker="p316", file_path=output_file)
        return FileResponse(output_file, media_type="audio/wav")
    except Exception as e:
        return {"error": str(e)}