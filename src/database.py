import os
from sqlmodel import create_engine, Session
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

# 获取数据库会话的依赖函数
def get_db():
    with Session(engine) as session:
        yield session
