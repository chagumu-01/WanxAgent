import subprocess
import os
import sys

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = ""

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_remote_command(command):
    print(f"🔌 执行远程命令: {command}")
    ssh_command = f'sshpass -p "{SERVER_PASSWORD}" ssh {SERVER_USER}@{SERVER_IP} "{command}"'
    result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 命令执行失败: {result.stderr}")
    else:
        print(f"✅ 命令执行成功: {result.stdout}")
    return result

def upload_files():
    print("📤 上传项目文件到服务器...")
    os.chdir(PROJECT_ROOT)
    zip_command = f'tar -czf /tmp/wanxagent.tar.gz --exclude=".git" --exclude="node_modules" --exclude="__pycache__" --exclude="*.pyc" .'
    subprocess.run(zip_command, shell=True, check=True)
    
    scp_command = f'sshpass -p "{SERVER_PASSWORD}" scp /tmp/wanxagent.tar.gz {SERVER_USER}@{SERVER_IP}:/opt/'
    subprocess.run(scp_command, shell=True, check=True)
    
    run_remote_command("mkdir -p /opt/wanxagent && rm -rf /opt/wanxagent/*")
    run_remote_command("tar -xzf /opt/wanxagent.tar.gz -C /opt/wanxagent")
    print("✅ 文件上传完成")

def install_dependencies():
    print("📦 在服务器上安装依赖...")
    
    run_remote_command("apt-get update && apt-get install -y python3 python3-pip nodejs npm redis-server nginx")
    
    run_remote_command("cd /opt/wanxagent && pip install -r requirements.txt")
    
    run_remote_command("cd /opt/wanxagent/src/frontend && npm install")
    print("✅ 依赖安装完成")

def configure_nginx():
    print("🔧 配置 Nginx...")
    
    nginx_config = """server {
    listen 80;
    server_name 47.104.227.189;

    location / {
        proxy_pass http://localhost:8091;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    location /local_storage/ {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
    }
}
"""
    
    with open("/tmp/nginx.conf", "w") as f:
        f.write(nginx_config)
    
    scp_command = f'sshpass -p "{SERVER_PASSWORD}" scp /tmp/nginx.conf {SERVER_USER}@{SERVER_IP}:/etc/nginx/sites-available/wanxagent'
    subprocess.run(scp_command, shell=True, check=True)
    
    run_remote_command("ln -sf /etc/nginx/sites-available/wanxagent /etc/nginx/sites-enabled/")
    run_remote_command("nginx -t && systemctl restart nginx")
    print("✅ Nginx 配置完成")

def configure_env():
    print("⚙️ 配置环境变量...")
    
    env_content = """SERVER_HOST=0.0.0.0
SERVER_PORT=7860
MYSQL_ENDPOINT=sqlite:///./wanxagent.db
MYSQL_ASYNC_ENDPOINT=sqlite+aiosqlite:///./wanxagent.db
REDIS_ENDPOINT=redis://localhost:6379
CONVERSATION_MODEL_API_KEY=your_api_key_here
CONVERSATION_MODEL_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
CONVERSATION_MODEL_NAME=glm-4.5-air
TOOL_CALL_MODEL_API_KEY=your_api_key_here
TOOL_CALL_MODEL_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
TOOL_CALL_MODEL_NAME=glm-4.5-air
REASONING_MODEL_API_KEY=your_api_key_here
REASONING_MODEL_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
REASONING_MODEL_NAME=glm-4.5-air
TEXT2IMAGE_API_KEY=your_api_key_here
TEXT2IMAGE_BASE_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
TEXT2IMAGE_MODEL_NAME=wanx2.0-t2i-turbo
QWEN_VL_API_KEY=your_api_key_here
QWEN_VL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_VL_MODEL_NAME=qwen-vl-plus
EMBEDDING_API_KEY=your_api_key_here
EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
EMBEDDING_MODEL_NAME=text-embedding-v3
RERANK_API_KEY=your_api_key_here
RERANK_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
RERANK_MODEL_NAME=qwen-vl-rerank
WEATHER_API_KEY=your_weather_api_key
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
DELIVERY_API_KEY=your_delivery_api_key
BOCHA_API_KEY=your_bocha_api_key
RAG_ENABLE_SUMMARY=False
RAG_ENABLE_ELASTICSEARCH=False
RAG_TOP_K=5
RAG_MIN_SCORE=0.2
RAG_CHUNK_SIZE=500
RAG_OVERLAP_SIZE=100
ELASTICSEARCH_HOSTS=http://127.0.0.1:9200
VECTOR_DB_HOST=127.0.0.1
VECTOR_DB_PORT=19530
VECTOR_DB_MODE=chroma
STORAGE_MODE=local
MINIO_ACCESS_KEY_ID=minioadmin
MINIO_ACCESS_KEY_SECRET=minioadmin
MINIO_ENDPOINT=127.0.0.1:9000
MINIO_BUCKET_NAME=wanxagent
MINIO_BASE_URL=http://127.0.0.1:9000/wanxagent
LOCAL_STORAGE_DIR=./storage
LOCAL_BASE_URL=/local_storage
MCP_LOGO_URL=https://wanxagent.oss-cn-beijing.aliyuncs.com/icons/mcp/mcp.png
TOOL_LOGO_URL=https://wanxagent.oss-cn-beijing.aliyuncs.com/icons/tools/default.png
AGENT_LOGO_URL=https://wanxagent.oss-cn-beijing.aliyuncs.com/icons/tools/bot.png
MARS_DAILY_URL=https://news.aibase.com/zh/news
MEMORY_COLLECTION_NAME=memory
"""
    
    with open("/tmp/.env", "w") as f:
        f.write(env_content)
    
    scp_command = f'sshpass -p "{SERVER_PASSWORD}" scp /tmp/.env {SERVER_USER}@{SERVER_IP}:/opt/wanxagent/.env'
    subprocess.run(scp_command, shell=True, check=True)
    print("✅ 环境变量配置完成")

def start_services():
    print("🚀 启动服务...")
    
    run_remote_command("systemctl start redis-server")
    run_remote_command("systemctl enable redis-server")
    
    run_remote_command("cd /opt/wanxagent/src/frontend && VITE_API_BASE_URL=http://47.104.227.189 npm run build")
    
    run_remote_command("cp -r /opt/wanxagent/src/frontend/dist/* /var/www/html/")
    
    run_remote_command("cd /opt/wanxagent/src/backend && nohup uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 &")
    print("✅ 服务启动完成")

def main():
    if not SERVER_PASSWORD:
        print("❌ 请先在脚本中设置服务器密码")
        sys.exit(1)
    
    print("============================================")
    print("      WanxAgent 一键部署脚本")
    print("      目标服务器: " + SERVER_IP)
    print("============================================")
    
    upload_files()
    install_dependencies()
    configure_env()
    configure_nginx()
    start_services()
    
    print("\n🎉 部署完成！")
    print("访问地址: http://" + SERVER_IP)
    print("API地址: http://" + SERVER_IP + "/api")

if __name__ == "__main__":
    main()