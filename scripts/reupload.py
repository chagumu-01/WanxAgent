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
    print("📦 重新打包项目...")
    os.chdir("d:\\OmniAgent")
    subprocess.run(["tar", "-czf", "wanxagent_new.tar.gz", "--exclude=.git", "--exclude=node_modules", "--exclude=__pycache__", "--exclude=*.pyc", "."], check=True)
    
    print("📤 上传到服务器...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    sftp = ssh.open_sftp()
    sftp.put("d:\\OmniAgent\\wanxagent_new.tar.gz", "/opt/wanxagent_new.tar.gz")
    sftp.close()
    ssh.close()
    
    print("🔧 解压并替换文件...")
    ssh_exec("cd /opt/wanxagent && tar -xzf /opt/wanxagent_new.tar.gz --strip-components=1")
    
    print("🔄 重启服务...")
    ssh_exec("pkill -f uvicorn")
    ssh_exec("sleep 3")
    ssh_exec("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
    
    print("⏳ 等待启动...")
    ssh_exec("sleep 15")
    
    output, error = ssh_exec("curl -s http://localhost:7860/health")
    print("健康检查:", output)
    
    if "OK" in output:
        print("✅ 服务重启成功!")
        output, error = ssh_exec('curl -X POST http://localhost:7860/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testuser4","user_password":"123456"}\'')
        print("注册测试:", output)
        
        output, error = ssh_exec('curl -X POST http://localhost:7860/api/v1/user/login -H "Content-Type: application/json" -d \'{"user_name":"testuser4","user_password":"123456"}\'')
        print("登录测试:", output)
    else:
        output, error = ssh_exec("cat /var/log/wanxagent.log")
        print("日志:", output[-2000:])

if __name__ == "__main__":
    main()