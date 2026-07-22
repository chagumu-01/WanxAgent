import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def ssh_exec(command, description=""):
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"📝 命令: {command}")
    print(f"{'='*60}")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    
    if output:
        print("✅ 输出:", output[:500] if len(output) > 500 else output)
    
    if error:
        print("❌ 错误:", error[:500] if len(error) > 500 else error)
    
    ssh.close()
    return output, error

def main():
    print(f"\n🚀 修复 langgraph 版本问题")
    
    ssh_exec("pkill -f uvicorn", "停止旧进程")
    
    ssh_exec("/opt/wanxagent/venv/bin/pip install --upgrade langgraph", "升级 langgraph")
    
    ssh_exec("/opt/wanxagent/venv/bin/pip show langgraph", "检查 langgraph 版本")
    
    ssh_exec("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &", "启动后端服务")
    
    ssh_exec("sleep 15", "等待服务启动")
    
    output, error = ssh_exec("curl -s http://localhost:7860/health")
    print("\n健康检查:", output)
    
    if "OK" in output:
        print("✅ 服务启动成功!")
        print("访问地址: http://47.104.227.189")
    else:
        output, error = ssh_exec("cat /var/log/wanxagent.log")
        print("日志:", output[-2000:])

if __name__ == "__main__":
    main()