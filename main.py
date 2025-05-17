import logging
from fastapi import FastAPI, Request, HTTPException
import requests
import os

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info(f"Received request with secret: {secret}")
    if secret != BOT_SECRET:
        logger.warning("Invalid secret received")
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    data = await request.json()
    logger.info(f"Received data: {data}")

    if "message" in data:
        message = data["message"]
        chat_id = str(message["chat"]["id"])
        text = message.get("text", "")
        logger.info(f"Received message from chat {chat_id}: {text}")

        if chat_id == ADMIN_UID:
            if "reply_to_message" in message:
                replied_message = message["reply_to_message"]
                if "from" in replied_message and "id" in replied_message["from"]:
                    user_id = str(replied_message["from"]["id"])
                    logger.info(f"Replying to user {user_id} with message: {text}")
                    requests.post(send_url, json={
                        "chat_id": user_id,
                        "text": text
                    })
                    return {"status": f"Message sent to user {user_id}"}
            
            logger.info("No reply_to_message found. Sending reminder to admin.")
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": "请通过回复用户消息来发送回复。"
            })
            return {"status": "No reply_to_message"}

        else:
            forward_text = f"【来自用户 {chat_id} 的消息】：\n{text}"
            logger.info(f"Forwarding message from user {chat_id} to admin.")
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": forward_text
            })
            return {"status": "Forwarded to admin"}

    return {"status": "ok"}
