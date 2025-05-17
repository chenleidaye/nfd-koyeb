@app.post("/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != BOT_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    data = await request.json()
    if "message" in data:
        message = data["message"]
        chat_id = str(message["chat"]["id"])
        text = message.get("text", "")

        # 管理员回复某个用户
        if chat_id == ADMIN_UID:
            if "reply_to_message" in message:
                replied_message = message["reply_to_message"]
                if "from" in replied_message and "id" in replied_message["from"]:
                    user_id = str(replied_message["from"]["id"])
                    try:
                        # 回复用户
                        response = requests.post(send_url, json={
                            "chat_id": user_id,
                            "text": text
                        })
                        response.raise_for_status()
                        return {"status": f"Message sent to user {user_id}"}
                    except requests.exceptions.RequestException as e:
                        # 如果发送失败，输出错误日志
                        return {"status": f"Error sending message: {e}"}
            
            # 如果没有找到回复消息，提醒管理员
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": "请通过回复用户消息来发送回复。"
            })
            return {"status": "No reply_to_message"}

        else:
            forward_text = f"【来自用户 {chat_id} 的消息】：\n{text}"
            requests.post(send_url, json={
                "chat_id": ADMIN_UID,
                "text": forward_text
            })
            return {"status": "Forwarded to admin"}
    
    return {"status": "ok"}
