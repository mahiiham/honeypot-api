import os
import logging
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from src.honeypot_agent import HoneypotAgent
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
CALLBACK_URL = os.getenv("CALLBACK_URL")  

app = FastAPI()
agent = HoneypotAgent()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class Metadata(BaseModel):
    channel: str
    language: str
    locale: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: list
    metadata: Metadata

@app.post("/honeypot")
async def honeypot_endpoint(data: HoneypotRequest, x_api_key: str = Header(None)):

    try:
        # Proper 403 response instead of fake success
        if API_KEY:
            if not x_api_key or x_api_key != API_KEY:
                raise HTTPException(status_code=403, detail="Invalid API key")

        reply = agent.generate_reply(
            data.sessionId,
            data.message.text,
            data.conversationHistory
        )

        return {"status": "success", "reply": reply}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return {
            "status": "success",
            "reply": "I need to verify your identity first. Can you provide your employee ID?"
        }
@app.post("/final")
async def final_output(sessionId: str):
    output = agent.get_final_output(sessionId)
    if not output:
        raise HTTPException(status_code=404, detail="Session not found")

    
    if CALLBACK_URL:
        try:
            requests.post(CALLBACK_URL, json=output, timeout=5)
        except Exception as e:
            logger.warning(f"Callback failed: {e}")

    return output

@app.get("/")
async def home():
    return {"message": "Honeypot API is running"}