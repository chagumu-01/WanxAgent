import os
import threading
import time
import sys
from fastapi import FastAPI
import uvicorn

# ====================== 后台执行你的Pico Agent ======================
def start_pico_agent():
    """独立线程运行你的原始Agent"""
    try:
        # 等价于本地执行 python -m pico
        from pico import main
        main()
    except Exception as e:
        print(f"Agent运行异常: {e}")

# 创建守护线程运行Agent
agent_thread = threading.Thread(target=start_pico_agent, daemon=True)
agent_thread.start()

# ====================== Web服务（专门用来骗过Render端口检测） ======================
app = FastAPI()

@app.get("/health")
def health_check():
    """健康检测接口，ping这个地址就能防止Render休眠"""
    return {
        "status": "online",
        "message": "Pico Agent 正在后台运行"
    }

if __name__ == "__main__":
    # Render硬性规定 host必须是0.0.0.0，端口读取环境变量PORT
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host=HOST, port=PORT)