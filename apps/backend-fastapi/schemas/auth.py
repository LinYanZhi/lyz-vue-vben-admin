from typing import Optional, List
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str

class LoginResponse(BaseModel):
    """登录响应模型"""
    id: int
    username: str
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    access_token: str
    is_superuser: bool = False

class RefreshTokenResponse(BaseModel):
    """刷新token响应模型"""
    access_token: str

class AccessCodesResponse(BaseModel):
    """获取权限码响应模型"""
    codes: List[str]
