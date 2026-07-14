import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import dotenv
import os
# 1. 密钥
dotenv.load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_secret_key")

# 2. 加密算法，HS256 是最常用的标准
ALGORITHM = "HS256"

# 3. Token 的有效期（比如 30 分钟）
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict[str, Any]) -> str:
    """
    根据传入的数据（如用户 email）生成 JWT Token
    """
    to_encode = data.copy()
    
    # 获取当前 UTC 时间，并加上过期分钟数
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 往 payload 中放入过期时间 "exp" (JWT 的标准字段)
    to_encode.update({"exp": expire})
    
    # 使用 jwt.encode 方法生成 Token 字符串
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """
    验证 Token，如果合法则返回 payload 中的 sub (email)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except InvalidTokenError:
        return None
