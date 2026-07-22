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
    print("🔍 检查服务状态...")
    
    output, error = ssh_exec("ps aux | grep uvicorn")
    print("进程:", output)
    
    output, error = ssh_exec("netstat -tlnp | grep 7860")
    print("端口:", output)
    
    output, error = ssh_exec("curl -s http://localhost:7860/health")
    print("健康检查:", output)
    
    if "OK" in output:
        print("\n✅ 后端服务已启动成功!")
        print("访问地址: http://47.104.227.189")
    else:
        print("\n❌ 服务未启动，尝试重启...")
        ssh_exec("pkill -f uvicorn")
        ssh_exec("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
        ssh_exec("sleep 10")
        
        output, error = ssh_exec("curl -s http://localhost:7860/health")
        print("重启后:", output)
        
        if "OK" in output:
            print("✅ 服务启动成功!")
        else:
            output, error = ssh_exec("cat /var/log/wanxagent.log")
            print("日志:", output)

if __name__ == "__main__":
    main()