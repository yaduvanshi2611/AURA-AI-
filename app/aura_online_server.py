from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from app.services.inference import LocalQwenProvider, AURA_SYSTEM_PROMPT

app = FastAPI(title="AURA Online Engine", version="1.0.0")

provider = LocalQwenProvider()


class OnlineInput(BaseModel):
    message: str
    system: str | None = None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "aura-online-engine",
        "model": provider.model_name,
    }


@app.post("/v1/chat")
def chat(data: OnlineInput, x_aura_key: str | None = Header(default=None)):
    expected = "aura-dev-key"

    if x_aura_key != expected:
        raise HTTPException(status_code=401, detail="Invalid AURA API key")

    reply = provider.generate(data.message)

    return {
        "reply": reply,
        "model": provider.model_name,
        "service": "aura-online-engine",
    }
