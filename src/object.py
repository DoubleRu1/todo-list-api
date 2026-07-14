import pydantic
from typing import Optional

class register_param(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr
    password: str = pydantic.Field(min_length=6)

class login_param(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str

class todos_param(pydantic.BaseModel):
    title: str = pydantic.Field(min_length=1, max_length=100)
    description: Optional[str] = None
    completed: Optional[bool] = False

# =================
# 响应数据模型
# =================
class TodoResponse(pydantic.BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True

class UserResponse(pydantic.BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
