# NFD - Koyeb 部署版

这是适用于 Koyeb 的 nfd 项目，无需 Cloudflare，所有功能集中部署。

---

## 🛠 环境变量（在 Koyeb 中设置）

- `ENV_BOT_TOKEN`：从 [@BotFather](https://t.me/BotFather) 获取的 Telegram Bot Token  
- `ENV_BOT_SECRET`：使用 [uuidgenerator](https://www.uuidgenerator.net/) 随机生成的 UUID  
- `ENV_ADMIN_UID`：使用 [@username_to_id_bot](https://t.me/username_to_id_bot) 获取你的 Telegram 用户 ID  

---

## 🚀 部署步骤

1. 将项目上传至 GitHub  
2. 登录 [Koyeb 控制台](https://app.koyeb.com/)，点击 **Create App**  
3. 选择 **GitHub 仓库** 作为来源，关联你的仓库  
4. Koyeb 会自动识别 `Dockerfile`，一般无需改动 **Build Command**  
5. 设置公开端口为 `8080`  
6. 在环境变量配置页添加以上 3 个环境变量  
7. 完成创建后，获取你的 Koyeb URL，例如：  
   `https://your-app-name.koyeb.app`  

---

## 📡 设置 Telegram Webhook

部署完成后，运行命令设置 Webhook（替换为真实值）：

```bash
# 将 <ENV_BOT_TOKEN> 替换为你的 Telegram Bot Token
# 将 <ENV_BOT_SECRET> 替换为你设置的 BOT_SECRET（UUID）

curl -X POST https://api.telegram.org/bot<ENV_BOT_TOKEN>/setWebhook \
  -d url=https://your-app-name.koyeb.app/webhook/<ENV_BOT_SECRET>
