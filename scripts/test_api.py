import urllib.request
import json

def main():
    print("📡 测试注册API...")
    try:
        data = json.dumps({"user_name": "testapiuser", "user_password": "123456"}).encode()
        req = urllib.request.Request(
            "http://47.104.227.189/api/v1/user/register",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=15)
        print("注册结果:", resp.read().decode())
    except Exception as e:
        print("注册失败:", e)
    
    print("\n📡 测试登录API...")
    try:
        data = json.dumps({"user_name": "testapiuser", "user_password": "123456"}).encode()
        req = urllib.request.Request(
            "http://47.104.227.189/api/v1/user/login",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=15)
        print("登录结果:", resp.read().decode())
    except Exception as e:
        print("登录失败:", e)

if __name__ == "__main__":
    main()