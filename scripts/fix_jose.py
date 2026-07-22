import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def ssh_exec(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    ssh.close()
    return output, error

def main():
    print("🔧 安装缺失依赖...")
    
    ssh_exec("pkill -f uvicorn")
    
    ssh_exec("/opt/wanxagent/venv/bin/pip install python-jose")
    
    ssh_exec("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
    
    print("⏳ 等待服务启动...")
    ssh_exec("sleep 20")
    
    output, error = ssh_exec("curl -s http://localhost:7860/health")
    print("\n健康检查:", output)
    
    if "OK" in output:
        print("✅ 服务启动成功!")
        print("访问地址: http://47.104.227.189")
        
        output, error = ssh_exec("curl -X POST http://localhost:7860/api/v1/user/register -H 'Content-Type: application/json' -d '{\"user_name\":\"newuser\",\"user_password\":\"123456\"}'")
        print("注册测试:", output)
    else:
        output, error = ssh_exec("cat /var/log/wanxagent.log")
        print("日志:", output[-2000:])

if __name__ == "__main__":
    main()