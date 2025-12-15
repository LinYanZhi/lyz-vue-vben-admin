from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import uuid

from core.database import get_db
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_jwt
)
from core.config import settings
from models.user import User
from schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenResponse
)
from schemas.base import ResponseBase
from utils.response import success_response, error_response

router = APIRouter()

# OAuth2密码Bearer模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    payload = decode_jwt(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # 查询用户
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    
    return user

@router.options("/login", status_code=200, response_model=None, include_in_schema=False)
async def login_options(response: Response):
    """处理登录接口的OPTIONS请求"""
    # 设置CORS头信息
    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@router.post("/login", response_model=ResponseBase[LoginResponse])
async def login(
    login_data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    print("收到登录请求！")
    print(f"请求数据: {login_data}")
    # 查询用户
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalars().first()
    
    # 验证用户和密码
    if not user or not verify_password(login_data.password, user.password):
        return error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message="Username or password is incorrect"
        )
    
    if not user.status:
        return error_response(
            code=status.HTTP_403_FORBIDDEN,
            message="User is disabled"
        )
    
    # 创建访问令牌
    access_token = create_access_token(user.username)
    
    # 创建刷新令牌
    refresh_token = create_refresh_token(user.username)
    
    # 设置refresh_token到cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        samesite="lax"
    )
    
    # 构建响应数据
    login_response = LoginResponse(
        id=user.id,
        username=user.username,
        nickname=user.nickname,
        email=user.email,
        phone=user.phone,
        avatar=user.avatar,
        access_token=access_token,
        is_superuser=user.is_superuser,
        homePath="/analytics"  # 设置默认首页路径
    )
    
    return success_response(data=login_response)

@router.post("/refresh", response_model=ResponseBase[RefreshTokenResponse])
async def refresh_token(
    response: Response,
    refresh_token: str = None,
    db: AsyncSession = Depends(get_db)
):
    """刷新访问令牌"""
    # 从cookie获取refresh_token
    if not refresh_token:
        return error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message="Refresh token is required"
        )
    
    # 验证refresh_token
    payload = decode_jwt(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        return error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid refresh token"
        )
    
    username: str = payload.get("sub")
    if username is None:
        return error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid refresh token"
        )
    
    # 查询用户
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    
    if not user or not user.status:
        return error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message="User not found or disabled"
        )
    
    # 创建新的访问令牌
    new_access_token = create_access_token(user.username)
    
    return success_response(
        data=RefreshTokenResponse(access_token=new_access_token)
    )

@router.post("/logout", response_model=ResponseBase)
async def logout(response: Response):
    """用户退出登录"""
    # 清除refresh_token cookie
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="lax"
    )
    
    return success_response()

@router.get("/codes", response_model=ResponseBase[List[str]])
async def get_access_codes(
    current_user: User = Depends(get_current_user)
):
    """获取用户权限码"""
    # 这里简化处理，实际应该根据用户角色获取权限码
    codes = [
        "sys:user:list",
        "sys:user:add",
        "sys:user:edit",
        "sys:user:delete",
        "sys:role:list",
        "sys:role:add",
        "sys:role:edit",
        "sys:role:delete",
        "sys:menu:list",
        "sys:menu:add",
        "sys:menu:edit",
        "sys:menu:delete"
    ]
    
    # 超级管理员拥有所有权限
    if current_user.is_superuser:
        return success_response(data=codes)
    
    # 普通用户根据角色获取权限（这里简化处理）
    return success_response(data=codes[:4])
