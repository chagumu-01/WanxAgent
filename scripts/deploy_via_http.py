import http.client
import json
import os

SERVER_IP = "47.104.227.189"

def main():
    print("📦 打包前端文件...")
    import tarfile
    dist_path = os.path.join(os.path.dirname(__file__), "..", "src", "frontend", "dist")
    tar_path = os.path.join(os.path.dirname(__file__), "..", "frontend_dist.tar.gz")
    
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(dist_path, arcname="dist")
    print(f"✅ 打包完成: {tar_path}")
    
    print("\n📤 通过HTTP上传...")
    try:
        with open(tar_path, "rb") as f:
            data = f.read()
        
        conn = http.client.HTTPConnection(SERVER_IP, 80, timeout=120)
        conn.request("POST", "/api/v1/upload", data, {
            "Content-Type": "application/octet-stream",
            "X-Filename": "frontend_dist.tar.gz"
        })
        response = conn.getresponse()
        print(f"响应: {response.status} {response.reason}")
        print(f"内容: {response.read().decode()}")
        conn.close()
    except Exception as e:
        print(f"❌ HTTP上传失败: {e}")
    
    print("\n📡 测试服务器...")
    try:
        conn = http.client.HTTPConnection(SERVER_IP, 80, timeout=30)
        conn.request("GET", "/")
        response = conn.getresponse()
        html = response.read().decode()[:500]
        print(f"响应: {response.status} {response.reason}")
        print(f"HTML: {html}")
        conn.close()
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    main()