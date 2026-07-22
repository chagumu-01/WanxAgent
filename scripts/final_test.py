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
    ssh.close()
    return output

def main():
    print("🔍 最终测试...")
    
    print("\n1. 健康检查:")
    output = ssh_exec("curl -s http://localhost:7860/health")
    print(output)
    
    print("\n2. 注册新用户:")
    output = ssh_exec('curl -X POST http://localhost:7860/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"user123","user_password":"123456"}\'')
    print(output)
    
    print("\n3. 登录测试:")
    output = ssh_exec('curl -X POST http://localhost:7860/api/v1/user/login -H "Content-Type: application/json" -d \'{"user_name":"user123","user_password":"123456"}\'')
    print(output)
    
    print("\n4. 公网访问测试:")
    output = ssh_exec("curl -s http://47.104.227.189/health")
    print(output)
    
    print("\n🎉 测试完成!")
    print("访问地址: http://47.104.227.189")

if __name__ == "__main__":
    main()