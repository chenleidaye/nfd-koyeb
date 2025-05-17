# NFD - Koyeb 部署版

这是适用于 Koyeb 的 nfd 项目，无需 Cloudflare，所有功能集中部署。

## 🛠 环境变量（在 Koyeb 中设置）

- `ENV_BOT_TOKEN`: 从 @BotFather 获取的 Telegram Bot Token
- `ENV_BOT_SECRET`: 使用 uuidgenerator.net 随机生成的 UUID
- `ENV_ADMIN_UID`: 使用 @username_to_id_bot 获取你的 Telegram 用户 ID

## 🚀 部署步骤

1. 将本项目上传至 GitHub
2. 打开 [Koyeb 控制台](https://app.koyeb.com/)，点击 Create App
3. 选择 GitHub 仓库作为来源
4. 自动识别 Dockerfile，无需改动 Build Command
5. 设置公开端口为 `8080`
6. 设置环境变量（见上）
7. 完成后，获取你的 Koyeb URL，例如：https://nfd.koyeb.app

## 📡 设置 Telegram Webhook

部署完成后，在本地终端运行：

```
curl -X POST https://api.telegram.org/bot<ENV_BOT_TOKEN>/setWebhook \
  -d url=https://nfd.koyeb.app/webhook/<ENV_BOT_SECRET>
```

将 `<ENV_BOT_TOKEN>` 和 `<ENV_BOT_SECRET>` 替换为你的真实值。

## ✅ 完成！

现在你可以向你的 Telegram Bot 发送消息，它将在 Koyeb 中回应。
