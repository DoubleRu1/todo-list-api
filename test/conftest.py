import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from src.main import app
from src.database import get_db
from src.models import User
from src.security import get_password_hash

# 1. 使用 SQLite 内存数据库作为测试库，保证测试隔离且快速
# 加入 check_same_thread=False 和 StaticPool 保证所有会话共享同一个内存数据库状态
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 在测试开始前就创建所有表
SQLModel.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """每个测试函数拥有一个独立的事务，在测试结束后回滚，保证数据库干净"""
    connection = engine.connect()
    transaction = connection.begin()
    
    # 将 session 绑定到当前连接
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """覆盖 FastAPI 的 get_db 依赖，使用测试环境的 db_session"""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(db_session):
    """在数据库中创建一个默认的测试用户并返回"""
    user = User(
        name="Test User", 
        email="test@example.com", 
        password_hash=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """生成测试用的鉴权 Header"""
    response = client.post(
        "/login", 
        json={"email": test_user.email, "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
