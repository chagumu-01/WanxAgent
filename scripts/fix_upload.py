import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("📤 上传 user.py...")
    sftp = ssh.open_sftp()
    sftp.put("d:\\OmniAgent\\src\\backend\\agentchat\\api\\v1\\user.py", "/opt/wanxagent/src/backend/agentchat/api/v1/user.py")
    sftp.close()
    
    print("🔄 重启服务...")
    stdin, stdout, stderr = ssh.exec_command("pkill -f uvicorn")
    stdout.read()
    
    stdin, stdout, stderr = ssh.exec_command("sleep 3")
    stdout.read()
    
    stdin, stdout, stderr = ssh.exec_command("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
    stdout.read()
    
    print("⏳ 等待启动...")
    stdin, stdout, stderr = ssh.exec_command("sleep 15")
    stdout.read()
    
    stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:7860/health")
    output = stdout.read().decode('utf-8')
    print("健康检查:", output)
    
    if "OK" in output:
        print("✅ 服务启动成功!")
        stdin, stdout, stderr = ssh.exec_command('curl -X POST http://localhost:7860/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testuser6","user_password":"123456"}\'')
        output = stdout.read().decode('utf-8')
        print("注册结果:", output)
    else:
        stdin, stdout, stderr = ssh.exec_command("cat /var/log/wanxagent.log")
        output = stdout.read().decode('utf-8')
        print("日志:", output[-2000:])
    
    ssh.close()

if __name__ == "__main__":
    main()