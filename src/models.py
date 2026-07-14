from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str

    # 建立与 Todo 模型的一对多关系
    todos: List["Todo"] = Relationship(back_populates="owner")


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    owner_id: int = Field(foreign_key="users.id")

    # 建立与 User 模型的多对一关系
    owner: Optional[User] = Relationship(back_populates="todos")
