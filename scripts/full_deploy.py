import paramiko
import os
import tarfile
import time

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    print("📦 打包前端文件...")
    dist_path = os.path.join(os.path.dirname(__file__), "..", "src", "frontend", "dist")
    tar_path = os.path.join(os.path.dirname(__file__), "..", "frontend_dist.tar.gz")
    
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(dist_path, arcname="dist")
    print(f"✅ 打包完成: {tar_path}")
    
    print("\n🔌 连接服务器...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            SERVER_IP, 
            username=SERVER_USER, 
            password=SERVER_PASSWORD, 
            timeout=120, 
            banner_timeout=120,
            auth_timeout=120
        )
        
        print("✅ 连接成功")
        
        print("\n📤 上传前端文件...")
        sftp = ssh.open_sftp()
        sftp.put(tar_path, "/tmp/frontend_dist.tar.gz")
        sftp.close()
        print("✅ 上传完成")
        
        print("\n📥 解压前端文件...")
        stdin, stdout, stderr = ssh.exec_command("rm -rf /opt/wanxagent/src/frontend/dist && mkdir -p /opt/wanxagent/src/frontend/dist && tar -xzf /tmp/frontend_dist.tar.gz -C /opt/wanxagent/src/frontend && rm /tmp/frontend_dist.tar.gz")
        stdout.read()
        print("✅ 解压完成")
        
        print("\n🔄 重启后端服务...")
        stdin, stdout, stderr = ssh.exec_command("pkill -f uvicorn; sleep 5")
        stdout.read()
        
        stdin, stdout, stderr = ssh.exec_command("cd /opt/wanxagent/src/backend && nohup /opt/wanxagent/venv/bin/python -m uvicorn agentchat.main:app --host 0.0.0.0 --port 7860 > /var/log/wanxagent.log 2>&1 &")
        stdout.read()
        print("✅ 后端重启中...")
        
        print("\n⏳ 等待 20 秒...")
        stdin, stdout, stderr = ssh.exec_command("sleep 20")
        stdout.read()
        
        print("\n📡 测试健康检查...")
        stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:7860/health")
        health_result = stdout.read().decode()
        print("健康检查:", health_result)
        
        if "OK" in health_result:
            print("\n📡 测试注册...")
            stdin, stdout, stderr = ssh.exec_command('curl -X POST http://localhost:7860/api/v1/user/register -H "Content-Type: application/json" -d \'{"user_name":"testdeploy","user_password":"123456"}\'')
            print("注册结果:", stdout.read().decode())
            
            print("\n📡 测试登录...")
            stdin, stdout, stderr = ssh.exec_command('curl -X POST http://localhost:7860/api/v1/user/login -H "Content-Type: application/json" -d \'{"user_name":"testdeploy","user_password":"123456"}\'')
            print("登录结果:", stdout.read().decode())
        
        print("\n🔄 重启 Nginx...")
        stdin, stdout, stderr = ssh.exec_command("nginx -t && systemctl reload nginx")
        print("Nginx:", stdout.read().decode())
        
        ssh.close()
        
        print("\n🎉 部署完成!")
        
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            ssh.close()
        except:
            pass

if __name__ == "__main__":
    main()