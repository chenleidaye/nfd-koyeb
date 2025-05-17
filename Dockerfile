# 使用官方 Python 3.11 轻量镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制代码到容器
COPY main.py /app/

# 安装依赖
RUN pip install fastapi uvicorn requests

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
