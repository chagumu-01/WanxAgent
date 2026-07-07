import json
import time
from typing import Optional, Any
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


SECRET_KEY = "wanxagent-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 86400


class Settings:
    authjwt_secret_key: str = SECRET_KEY
    authjwt_token_location: list = ['cookies', 'headers']
    authjwt_cookie_csrf_protect: bool = False


class AuthJWT:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
    
    def create_access_token(self, subject: str, expires_time: int = ACCESS_TOKEN_EXPIRE_TIME):
        expire = datetime.utcnow() + timedelta(seconds=expires_time)
        to_encode = {"exp": expire, "sub": subject}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, subject: str):
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode = {"exp": expire, "sub": subject}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def set_access_cookies(self, access_token: str, response=None):
        pass
    
    def set_refresh_cookies(self, refresh_token: str, response=None):
        pass
    
    def jwt_required(self):
        pass
    
    def get_jwt_subject(self) -> str:
        return ""
    
    @staticmethod
    def load_config(func):
        return func
    
    @staticmethod
    def exception_handler(app):
        def handler(request, exc):
            raise HTTPException(status_code=401, detail=str(exc))
        return handler


class AuthJWTException(Exception):
    status_code = 401
    message = "Invalid authentication credentials"


security = HTTPBearer()


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_login_user(request: Request) -> Any:
    from agentchat.api.services.user import UserPayload
    
    if hasattr(request.state, 'is_whitelisted') and request.state.is_whitelisted:
        return UserPayload(user_id="1", user_name="Admin")
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    token = auth_header[7:]
    payload = decode_token(token)
    
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        user_data = json.loads(payload["sub"])
        return UserPayload(**user_data)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


def get_user_jwt(db_user):
    from agentchat.api.services.user import get_user_role
    
    role = get_user_role(db_user)
    payload = {'user_name': db_user.user_name, 'user_id': db_user.user_id, 'role': role}
    
    access_token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_TIME), "sub": json.dumps(payload)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    refresh_token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(days=7), "sub": db_user.user_name},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return access_token, refresh_token, role
