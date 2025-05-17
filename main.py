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

        # 管理员发消息给机器人，格式要求：回复某条消息（那条消息是用户消息）
        if chat_id == ADMIN_UID:
            # 判断是否为回复消息
            if "reply_to_message" in message:
                # 取出被回复的消息的用户ID
                replied_message = message["reply_to_message"]
                if "from" in replied_message and "id" in replied_message["from"]:
                    user_id = str(replied_message["from"]["id"])
                    # 转发管理员消息给普通用户
                    requests.post(send_url, json={
                        "chat_id": user_id,
                        "text": text
                    })
                    return {"status": f"message sent to user {user_id}"}
            # 如果不是回复消息，提示管理员
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": "请通过回复用户消息来发送回复。"
            })
            return {"status": "no reply_to_message"}

        else:
            # 普通用户消息，转发给管理员，带上用户id方便回复
            forward_text = f"【来自用户 {chat_id} 的消息】：\n{text}"
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": forward_text
            })
            return {"status"
