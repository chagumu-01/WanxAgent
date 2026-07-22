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
    output, error = ssh_exec("curl -s http://localhost:7860/health")
    print("健康检查:", output)
    
    if "OK" not in output:
        output, error = ssh_exec("cat /var/log/wanxagent.log")
        print("日志:", output[-2000:])

if __name__ == "__main__":
    main()