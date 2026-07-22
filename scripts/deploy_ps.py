import subprocess
import os

SERVER_IP = "47.104.227.189"
SERVER_USER = "root"
SERVER_PASSWORD = "Wnd94188"

def main():
    tar_path = os.path.join(os.path.dirname(__file__), "..", "frontend_dist.tar.gz")
    
    print("📤 使用 scp 上传文件...")
    cmd = f'sshpass -p "{SERVER_PASSWORD}" scp "{tar_path}" {SERVER_USER}@{SERVER_IP}:/tmp/frontend_dist.tar.gz'
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    print("输出:", result.stdout)
    print("错误:", result.stderr)
    print("返回码:", result.returncode)

if __name__ == "__main__":
    main()