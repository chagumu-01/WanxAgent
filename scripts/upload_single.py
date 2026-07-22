import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    print("📤 上传修复后的文件...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    sftp = ssh.open_sftp()
    sftp.put("d:\\OmniAgent\\src\\backend\\agentchat\\api\\v1\\user.py", "/opt/wanxagent/src/backend/agentchat/api/v1/user.py")
    sftp.close()
    ssh.close()
    
    print("🔄 重启服务...")
    ssh_exec("pkill -f uvicorn")
    ssh_exec("sleep 3")
    ssh_exec("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
    
    print("⏳ 等待启动...")
    ssh_exec("sleep 15")
    
    output, error = ssh_exec("curl -s http://localhost:7860/health")
    print("健康检查:", output)
    
    if "OK" in output:
        print("✅ 成功!")
        output, error = ssh_exec('curl -X POST http://localhost:7860/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testuser5","user_password":"123456"}\'')
        print("注册:", output)
    else:
        output, error = ssh_exec("cat /var/log/wanxagent.log")
        print("日志:", output[-2000:])

def ssh_exec(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    ssh.close()
    return output, error

if __name__ == "__main__":
    main()