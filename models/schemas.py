from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    """
    请求模型验证：
    username:
    password:
    """
    password: str
    role: str
    jobnum: Optional[int] = None
    studentnum: Optional[int] = None
    sex: str = '男'
    age: int


class UserLogin(UserBase):
    password: str


class UserToken(BaseModel):
    token: str


class UsernameRole(UserBase):
    role: str
