from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    status: bool = True

class UserCreate(UserBase):
    """创建用户请求模型"""
    password: str

class UserUpdate(BaseModel):
    """更新用户请求模型"""
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    status: Optional[bool] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserInfoResponse(BaseModel):
    """用户信息响应模型（登录后获取）"""
    id: int
    username: str
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    is_superuser: bool = False
    roles: List[str] = []
    
    class Config:
        from_attributes = True
