import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def ssh_exec(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=60)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    ssh.close()
    return output, error

def main():
    print("📦 在服务器上构建前端...")
    
    print("1. 安装前端依赖...")
    output, error = ssh_exec("cd /opt/wanxagent/src/frontend && npm install --legacy-peer-deps")
    print("安装结果:", output[-500:] if len(output) > 500 else output)
    if "ERR!" in output or "error" in error.lower():
        print("❌ 依赖安装失败:", error)
        return
    
    print("\n2. 构建前端...")
    output, error = ssh_exec("cd /opt/wanxagent/src/frontend && npm run build")
    print("构建结果:", output[-500:] if len(output) > 500 else output)
    if "ERR!" in output or "error" in error.lower():
        print("❌ 构建失败:", error)
        return
    
    print("\n3. 重启 Nginx...")
    output, error = ssh_exec("nginx -t && systemctl reload nginx")
    print("Nginx:", output)
    
    print("\n4. 测试页面...")
    output, error = ssh_exec("curl -s http://47.104.227.189/ | grep -o '<title>.*</title>'")
    print("页面标题:", output)
    
    print("\n5. 测试注册...")
    output, error = ssh_exec('curl -X POST http://47.104.227.189/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testblack","user_password":"123456"}\'')
    print("注册结果:", output)
    
    print("\n🎉 完成!")
    print("访问地址: http://47.104.227.189")

if __name__ == "__main__":
    main()