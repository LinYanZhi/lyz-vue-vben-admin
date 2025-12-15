from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from api.auth import get_current_user
from models.user import User
from schemas.user import UserInfoResponse
from schemas.base import ResponseBase
from utils.response import success_response, error_response

router = APIRouter()

@router.get("/info", response_model=ResponseBase[UserInfoResponse])
async def get_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户信息"""
    # 构建用户信息响应
    user_info = UserInfoResponse(
        id=current_user.id,
        username=current_user.username,
        nickname=current_user.nickname,
        email=current_user.email,
        phone=current_user.phone,
        avatar=current_user.avatar,
        is_superuser=current_user.is_superuser,
        roles=["admin"],  # 这里简化处理，实际应该从角色表获取
        homePath="/analytics"  # 设置默认首页路径
    )
    
    return success_response(data=user_info)
