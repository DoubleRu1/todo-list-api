from src.security import get_password_hash, verify_password

def test_password_hashing():
    password = "secret_password"
    hashed = get_password_hash(password)
    
    # 哈希结果不应该等于明文
    assert hashed != password
    # 验证正确的密码
    assert verify_password(password, hashed) is True
    # 验证错误的密码
    assert verify_password("wrong_password", hashed) is False
