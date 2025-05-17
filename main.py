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
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # 管理员主动回复某个用户
        if str(chat_id) == ADMIN_UID and "reply_to_message" in message:
            reply_msg = message["reply_to_message"]
            if "forward_from" in reply_msg:
                user_id = reply_msg["forward_from"]["id"]
                reply = f"💬 管理员回复：{text}"
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                    "chat_id": user_id,
                    "text": reply
                })
                return {"status": "replied to user"}

        # 普通用户发消息，自动转发给管理员
        if str(chat_id) != ADMIN_UID:
            forward_url = f"https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage"
            requests.post(forward_url, json={
                "chat_id": ADMIN_UID,
                "from_chat_id": chat_id,
                "message_id": message["message_id"]
            })
            return {"status": "forwarded to admin"}

    return {"status": "ok"}
