from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional

from src.object import register_param, login_param, todos_param, TodoResponse
from src.jwt import create_access_token, verify_token
from src.database import engine, Base, get_db
from src.security import get_password_hash, verify_password
import src.models

# 在应用启动时创建数据库表
src.models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

# 定义 FastAPI 内置的 OAuth2 Bearer Token，以便在 Swagger UI 中使用自动认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    依赖注入：获取当前用户信息
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败，Token无效或已过期",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_token(token)
    if email is None:
        raise credentials_exception
        
    user = db.query(src.models.User).filter(src.models.User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user

@app.post(path="/register", status_code=status.HTTP_201_CREATED)
def register(params: register_param, db: Session = Depends(get_db)):
    # 从数据库中查找用户是否存在
    user = db.query(src.models.User).filter(src.models.User.email == params.email).first()

    # 用户存在，则返回错误信息
    if user:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")

    # 用户不存在，则创建用户，将用户密码hash后存入数据库
    hashed_password = get_password_hash(params.password)
    db_user = src.models.User(
        name=params.name, 
        email=params.email, 
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 并返回token
    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post(path="/login", status_code=status.HTTP_200_OK)
def login(params: login_param, db: Session = Depends(get_db)):
    # 用户不存在或密码错误，则返回错误信息
    user = db.query(src.models.User).filter(src.models.User.email == params.email).first()
    if not user or not verify_password(params.password, user.password_hash):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    # 用户存在，则验证密码，验证通过则返回token
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post(path="/todos", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(params: todos_param, db: Session = Depends(get_db), current_user: src.models.User = Depends(get_current_user)):
    # Dependency 会自动校验 Token，如果没有则返回401
    db_todo = src.models.Todo(
        title=params.title,
        description=params.description,
        completed=params.completed,
        owner_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put(path="/todos/{id}", response_model=TodoResponse)
def update_todo(id: int, params: todos_param, db: Session = Depends(get_db), current_user: src.models.User = Depends(get_current_user)):
    # 查找该 TODO 并且属于当前登录用户
    db_todo = db.query(src.models.Todo).filter(src.models.Todo.id == id, src.models.Todo.owner_id == current_user.id).first()
    
    # 查不到可能是没权限（不是你的）或者不存在，统一返回404（为了安全可以统一404防止枚举，或403）
    if db_todo is None:
        raise HTTPException(status_code=404, detail="未找到该待办事项或您没有权限")

    # 更新 todo
    db_todo.title = params.title
    db_todo.description = params.description
    if params.completed is not None:
        db_todo.completed = params.completed
        
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete(path="/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db), current_user: src.models.User = Depends(get_current_user)):
    # 查看用户是否有权限删除
    db_todo = db.query(src.models.Todo).filter(src.models.Todo.id == id, src.models.Todo.owner_id == current_user.id).first()
    
    # 没有权限或不存在返回404
    if db_todo is None:
        raise HTTPException(status_code=404, detail="未找到该待办事项或您没有权限")

    # 有权限则删除todo，返回204
    db.delete(db_todo)
    db.commit()
    return None

@app.get(path="/todos", response_model=List[TodoResponse])
def get_todos(
    skip: int = 0, 
    limit: int = 10, 
    completed: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user: src.models.User = Depends(get_current_user)
):
    # 初始化基础查询，只能查自己的数据
    query = db.query(src.models.Todo).filter(src.models.Todo.owner_id == current_user.id)
    
    # 根据完成状态过滤
    if completed is not None:
        query = query.filter(src.models.Todo.completed == completed)
        
    # 根据 title 进行模糊过滤搜索
    if search is not None:
        query = query.filter(src.models.Todo.title.ilike(f"%{search}%"))
        
    # 分页查询
    todos = query.offset(skip).limit(limit).all()
    return todos
