import os
from fastapi import FastAPI, Request, HTTPException
import requests

app = FastAPI()

BOT_TOKEN = os.getenv("ENV_BOT_TOKEN")
BOT_SECRET = os.getenv("ENV_BOT_SECRET")
ADMIN_UID = os.getenv("ENV_ADMIN_UID")

@app.get("/")
def root():
    return {"status": "nfd bot is running"}

@app.post("/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != BOT_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    data = await request.json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if str(chat_id) != ADMIN_UID:
            return {"status": "ignored"}

        reply = f"Echo: {text}"
        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(send_url, json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"status": "ok"}
