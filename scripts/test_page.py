import paramiko

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=30)
    
    print("📡 测试页面标题...")
    stdin, stdout, stderr = ssh.exec_command("curl -s http://47.104.227.189/ | grep -o '<title>.*</title>'")
    print("标题:", stdout.read().decode())
    
    print("\n📡 测试注册...")
    stdin, stdout, stderr = ssh.exec_command('curl -X POST http://47.104.227.189/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testnew","user_password":"123456"}\'')
    print("注册:", stdout.read().decode())
    
    print("\n📡 测试登录...")
    stdin, stdout, stderr = ssh.exec_command('curl -X POST http://47.104.227.189/api/v1/user/login -H "Content-Type: application/json" -d \'{"user_name":"testnew","user_password":"123456"}\'')
    print("登录:", stdout.read().decode())
    
    ssh.close()
    
    print("\n✅ 测试完成")
    print("访问地址: http://47.104.227.189")

if __name__ == "__main__":
    main()