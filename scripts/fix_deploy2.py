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
        print("✅ 输出:")
        print(output)
    
    if error:
        print("❌ 错误:")
        print(error)
    
    ssh.close()
    return output, error

def main():
    print(f"\n🚀 开始修复服务器 {SERVER_IP}")
    
    ssh_exec("apt-get update && apt-get install -y python3-venv python3-full", "安装 Python 虚拟环境工具")
    
    ssh_exec("rm -rf /opt/wanxagent/venv", "删除旧虚拟环境")
    
    ssh_exec("python3 -m venv /opt/wanxagent/venv", "创建虚拟环境")
    
    ssh_exec("/opt/wanxagent/venv/bin/pip install -r /opt/wanxagent/requirements.txt", "安装项目依赖")
    
    ssh_exec("pkill -f uvicorn 2>/dev/null; sleep 2", "停止旧进程")
    
    ssh_exec("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &", "启动后端服务")
    
    ssh_exec("sleep 10", "等待服务启动")
    
    ssh_exec("ps aux | grep uvicorn", "检查 uvicorn 进程")
    ssh_exec("netstat -tlnp | grep 7860", "检查端口")
    ssh_exec("curl -s http://localhost:7860/health", "测试健康检查")
    
    ssh_exec("curl -X POST http://localhost:7860/api/v1/user/register -H 'Content-Type: application/json' -d '{\"user_name\":\"testuser3\",\"user_password\":\"123456\"}'", "测试注册接口")
    
    print("\n" + "="*60)
    print("✅ 修复完成")
    print("="*60)

if __name__ == "__main__":
    main()