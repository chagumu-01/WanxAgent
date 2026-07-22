import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=60, banner_timeout=60)
        
        print("📦 检查前端构建状态...")
        stdin, stdout, stderr = ssh.exec_command("ls -la /opt/wanxagent/src/frontend/dist/ 2>&1 | head -5")
        print("dist目录:", stdout.read().decode())
        
        print("\n📦 重新构建前端...")
        stdin, stdout, stderr = ssh.exec_command("cd /opt/wanxagent/src/frontend && npm run build 2>&1", timeout=300)
        output = stdout.read().decode()
        print("构建结果:", output[-500:] if len(output) > 500 else output)
        
        print("\n🔄 重启 Nginx...")
        stdin, stdout, stderr = ssh.exec_command("nginx -t && systemctl reload nginx")
        print("Nginx:", stdout.read().decode())
        
        ssh.close()
        
        print("\n🎉 前端更新完成!")
    except Exception as e:
        print(f"❌ 连接失败: {e}")

if __name__ == "__main__":
    main()