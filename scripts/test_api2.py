import urllib.request
import json
import time

def main():
    print("📡 测试后端API...")
    
    for attempt in range(3):
        print(f"\n尝试 {attempt + 1}/3")
        
        try:
            print("1. 测试健康检查...")
            req = urllib.request.Request("http://47.104.227.189/api/v1/user/health")
            resp = urllib.request.urlopen(req, timeout=15)
            print("健康检查:", resp.read().decode())
            
            print("\n2. 测试注册...")
            data = json.dumps({"user_name": f"testuser{int(time.time())}", "user_password": "123456"}).encode()
            req = urllib.request.Request(
                "http://47.104.227.189/api/v1/user/register",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=15)
            print("注册结果:", resp.read().decode())
            
            print("\n✅ 所有测试通过!")
            return
            
        except Exception as e:
            print(f"失败: {e}")
            time.sleep(5)
    
    print("\n❌ 所有尝试均失败")

if __name__ == "__main__":
    main()