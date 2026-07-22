import subprocess
import os

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    tar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend_dist.tar.gz"))
    
    plink_path = r"C:\Program Files\PuTTY\plink.exe"
    pscp_path = r"C:\Program Files\PuTTY\pscp.exe"
    
    if os.path.exists(pscp_path):
        print("📤 使用 PSCP 上传文件...")
        cmd = f'"{pscp_path}" -pw "{SERVER_PASSWORD}" "{tar_path}" {SERVER_USER}@{SERVER_IP}:/tmp/frontend_dist.tar.gz'
        print(f"执行: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        print("输出:", result.stdout)
        print("错误:", result.stderr)
        print("返回码:", result.returncode)
        
        if result.returncode == 0:
            print("\n🔄 使用 Plink 执行命令...")
            cmd = f'"{plink_path}" -pw "{SERVER_PASSWORD}" {SERVER_USER}@{SERVER_IP} "rm -rf /opt/wanxagent/src/frontend/dist && mkdir -p /opt/wanxagent/src/frontend/dist && tar -xzf /tmp/frontend_dist.tar.gz -C /opt/wanxagent/src/frontend && rm /tmp/frontend_dist.tar.gz && pkill -f uvicorn; sleep 5; cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 & && sleep 15 && curl -s http://localhost:7860/health && nginx -t && systemctl reload nginx"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
            print("输出:", result.stdout)
            print("错误:", result.stderr)
            print("返回码:", result.returncode)
    else:
        print("❌ PuTTY 未安装")

if __name__ == "__main__":
    main()