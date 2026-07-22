import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=120, banner_timeout=120)
        
        print("🔄 重启后端服务...")
        stdin, stdout, stderr = ssh.exec_command("pkill -f uvicorn; sleep 3; cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
        stdout.read()
        
        print("⏳ 等待 15 秒...")
        stdin, stdout, stderr = ssh.exec_command("sleep 15")
        stdout.read()
        
        print("📡 测试健康检查...")
        stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:7860/health")
        print("健康检查:", stdout.read().decode())
        
        print("📡 测试注册...")
        stdin, stdout, stderr = ssh.exec_command('curl -X POST http://localhost:7860/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testfinal","user_password":"123456"}\'')
        print("注册结果:", stdout.read().decode())
        
        ssh.close()
        
        print("\n✅ 完成!")
    except Exception as e:
        print(f"❌ 失败: {e}")

if __name__ == "__main__":
    main()