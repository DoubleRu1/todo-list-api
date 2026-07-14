import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import dotenv

dotenv.load_dotenv()

# 获取环境变量中的 DATABASE_URL，如果没有则使用默认的本地 PostgreSQL 地址
# 格式: postgresql://[user]:[password]@[host]:[port]/[db_name]
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/todo_list"
)

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建数据库会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建声明性基类，供 ORM 模型继承
Base = declarative_base()

# 获取数据库会话的依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
