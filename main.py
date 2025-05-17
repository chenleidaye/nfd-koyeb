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
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "")

        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        if chat_id != ADMIN_UID:
            # 如果不是管理员，转发消息给管理员
            forward_text = f"【来自用户 {chat_id} 的消息】：\n{text}"
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": forward_text
            })
            return {"status": "forwarded to admin"}

        else:
            # 管理员发来的消息，回复 Echo
            reply = f"Echo: {text}"
            requests.post(send_url, json={
                "chat_id": chat_id,
                "text": reply
            })

    return {"status": "ok"}
