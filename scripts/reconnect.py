import paramiko
import time

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    print("🔌 尝试重新连接服务器...")
    
    for attempt in range(3):
        try:
            print(f"尝试 {attempt + 1}/3...")
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                SERVER_IP, 
                username=SERVER_USER, 
                password=SERVER_PASSWORD, 
                timeout=120, 
                banner_timeout=120,
                auth_timeout=120
            )
            
            print("✅ 连接成功!")
            
            print("\n🔄 重启后端服务...")
            stdin, stdout, stderr = ssh.exec_command("pkill -f uvicorn; sleep 5")
            stdout.read()
            
            stdin, stdout, stderr = ssh.exec_command("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
            stdout.read()
            
            print("⏳ 等待 20 秒...")
            stdin, stdout, stderr = ssh.exec_command("sleep 20")
            stdout.read()
            
            print("📡 测试健康检查...")
            stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:7860/health")
            health_result = stdout.read().decode()
            print("健康检查:", health_result)
            
            if "OK" in health_result:
                print("\n📡 测试注册...")
                stdin, stdout, stderr = ssh.exec_command('curl -X POST http://localhost:7860/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testnew2","user_password":"123456"}\'')
                print("注册结果:", stdout.read().decode())
                
                print("\n📡 测试登录...")
                stdin, stdout, stderr = ssh.exec_command('curl -X POST http://localhost:7860/api/v1/user/login -H "Content-Type: application/json" -d \'{"user_name":"testnew2","user_password":"123456"}\'')
                print("登录结果:", stdout.read().decode())
            
            ssh.close()
            
            print("\n🎉 完成!")
            return
            
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            time.sleep(10)
    
    print("\n❌ 所有尝试均失败，请稍后再试")

if __name__ == "__main__":
    main()