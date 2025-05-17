import os
from fastapi import FastAPI, Request, HTTPException
import requests

app = FastAPI()

BOT_TOKEN = os.getenv("ENV_BOT_TOKEN")
BOT_SECRET = os.getenv("ENV_BOT_SECRET")
ADMIN_UID = os.getenv("ENV_ADMIN_UID")

send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

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
        chat_id = str(message["chat"]["id"])
        text = message.get("text", "")

        if chat_id == ADMIN_UID:
            if "reply_to_message" in message:
                replied_message = message["reply_to_message"]
                if "from" in replied_message and "id" in replied_message["from"]:
                    user_id = str(replied_message["from"]["id"])
                    requests.post(send_url, json={
                        "chat_id": user_id,
                        "text": text
                    })
                    return {"status": f"message sent to user {user_id}"}
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": "请通过回复用户消息来发送回复。"
            })
            return {"status": "no reply_to_message"}

        else:
            forward_text = f"【来自用户 {chat_id} 的消息】：\n{text}"
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": forward_text
            })
            return {"status": "forwarded to admin"}

    return {"status": "ok"}
