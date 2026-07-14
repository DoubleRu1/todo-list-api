from src.jwt import create_access_token, verify_token
import time

def test_create_and_verify_token():
    email = "test@example.com"
    data = {"sub": email}
    
    # 1. 测试 Token 生成
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0
    
    # 2. 测试 Token 解析
    decoded_email = verify_token(token)
    assert decoded_email == email

def test_verify_invalid_token():
    # 测试伪造的或损坏的 Token
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"
    decoded_email = verify_token(invalid_token)
    assert decoded_email is None
