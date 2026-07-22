import paramiko
import os

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def ssh_exec(command, description=""):
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"📝 命令: {command}")
    print(f"{'='*60}")
    
    try:
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
        return True, output, error
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False, "", str(e)

def main():
    print(f"\n🚀 开始远程排查服务器 {SERVER_IP}")
    
    success, stdout, stderr = ssh_exec("uname -a && cat /etc/os-release", "服务器基本信息")
    if not success:
        print("❌ SSH连接失败，请检查网络和密码")
        return
    
    ssh_exec("ls -la /opt/", "检查 /opt 目录")
    ssh_exec("ls -la /opt/wanxagent/ 2>&1", "检查项目根目录")
    ssh_exec("ls -la /opt/wanxagent/src/frontend/dist/ 2>&1", "检查前端构建目录")
    
    ssh_exec("netstat -tlnp | grep 7860 2>&1 || ss -tlnp | grep 7860 2>&1", "检查 7860 端口")
    ssh_exec("ps aux | grep uvicorn 2>&1", "检查 uvicorn 进程")
    ssh_exec("cat /var/log/wanxagent.log 2>&1 | tail -50", "后端日志")
    
    ssh_exec("curl -s http://localhost:7860/health 2>&1", "后端健康检查")
    
    ssh_exec("systemctl status nginx 2>&1", "Nginx 状态")
    ssh_exec("cat /etc/nginx/sites-enabled/wanxagent 2>&1", "Nginx 配置")
    ssh_exec("nginx -t 2>&1", "Nginx 配置测试")
    
    ssh_exec("systemctl status redis-server 2>&1", "Redis 状态")
    ssh_exec("redis-cli ping 2>&1", "Redis 连接测试")
    
    ssh_exec("cat /opt/wanxagent/src/frontend/.env 2>&1", "前端环境配置")
    ssh_exec("ufw status 2>&1 || iptables -L 2>&1", "防火墙状态")
    ssh_exec("curl -s http://47.104.227.189/health 2>&1", "公网访问测试")
    
    print("\n" + "="*60)
    print("📊 排查完成")
    print("="*60)

if __name__ == "__main__":
    main()