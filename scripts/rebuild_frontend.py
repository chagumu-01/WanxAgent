import paramiko
import subprocess
import os

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
    print("📦 在本地构建前端...")
    os.chdir("d:\\OmniAgent\\src\\frontend")
    
    result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ 构建失败:", result.stderr)
        return
    print("✅ 构建成功")
    
    print("📤 打包并上传到服务器...")
    subprocess.run(["tar", "-czf", "dist.tar.gz", "dist"], check=True)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    sftp = ssh.open_sftp()
    sftp.put("d:\\OmniAgent\\src\\frontend\\dist.tar.gz", "/tmp/dist.tar.gz")
    sftp.close()
    
    print("🔧 在服务器上解压...")
    ssh_exec("rm -rf /opt/wanxagent/src/frontend/dist")
    ssh_exec("cd /opt/wanxagent/src/frontend && tar -xzf /tmp/dist.tar.gz")
    
    print("🔄 重启 Nginx...")
    ssh_exec("nginx -t && systemctl reload nginx")
    
    ssh.close()
    
    print("⏳ 等待 5 秒...")
    subprocess.run(["sleep", "5"], shell=True)
    
    print("📡 测试公网访问...")
    output, error = ssh_exec("curl -s http://47.104.227.189/ | head -20")
    print("页面内容:", output)
    
    print("\n🎉 前端更新完成!")
    print("访问地址: http://47.104.227.189")

if __name__ == "__main__":
    main()