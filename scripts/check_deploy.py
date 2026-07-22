import subprocess
import os
import sys

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"

def get_password():
    if len(sys.argv) > 1:
        return sys.argv[1]
    password = input("请输入服务器密码: ")
    return password

def run_ssh_command(password, command, description=""):
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"📝 命令: {command}")
    print(f"{'='*60}")
    
    ssh_command = f'sshpass -p "{password}" ssh {SERVER_USER}@{SERVER_IP} "{command}"'
    result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("✅ 输出:")
        print(result.stdout)
    
    if result.stderr:
        print("❌ 错误:")
        print(result.stderr)
    
    return result.returncode == 0, result.stdout, result.stderr

def main():
    password = get_password()
    if not password:
        print("❌ 密码不能为空")
        sys.exit(1)
    
    print(f"\n🚀 开始排查服务器 {SERVER_IP}")
    
    # 1. 检查服务器基本信息
    success, stdout, stderr = run_ssh_command(password, "uname -a && cat /etc/os-release", "服务器基本信息")
    
    # 2. 检查项目文件
    run_ssh_command(password, "ls -la /opt/", "检查 /opt 目录")
    run_ssh_command(password, "ls -la /opt/wanxagent/ 2>&1", "检查项目根目录")
    run_ssh_command(password, "ls -la /opt/wanxagent/src/frontend/dist/ 2>&1", "检查前端构建目录")
    
    # 3. 检查后端服务
    run_ssh_command(password, "netstat -tlnp | grep 7860 2>&1 || ss -tlnp | grep 7860 2>&1", "检查 7860 端口")
    run_ssh_command(password, "ps aux | grep uvicorn 2>&1", "检查 uvicorn 进程")
    
    # 4. 检查后端日志
    run_ssh_command(password, "cat /var/log/wanxagent.log 2>&1 | tail -50", "后端日志")
    
    # 5. 检查健康检查接口
    run_ssh_command(password, "curl -s http://localhost:7860/health 2>&1", "后端健康检查")
    
    # 6. 检查 Nginx
    run_ssh_command(password, "systemctl status nginx 2>&1", "Nginx 状态")
    run_ssh_command(password, "cat /etc/nginx/sites-enabled/wanxagent 2>&1", "Nginx 配置")
    run_ssh_command(password, "nginx -t 2>&1", "Nginx 配置测试")
    
    # 7. 检查 Redis
    run_ssh_command(password, "systemctl status redis-server 2>&1", "Redis 状态")
    run_ssh_command(password, "redis-cli ping 2>&1", "Redis 连接测试")
    
    # 8. 检查前端配置
    run_ssh_command(password, "cat /opt/wanxagent/src/frontend/.env 2>&1", "前端环境配置")
    
    # 9. 检查防火墙
    run_ssh_command(password, "ufw status 2>&1 || iptables -L 2>&1", "防火墙状态")
    
    # 10. 检查安全组/端口
    run_ssh_command(password, "curl -s http://47.104.227.189/health 2>&1", "公网访问测试")
    
    print("\n" + "="*60)
    print("📊 排查完成")
    print("="*60)

if __name__ == "__main__":
    main()