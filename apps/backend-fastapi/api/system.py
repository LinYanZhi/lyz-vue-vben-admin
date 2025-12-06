from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any

from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.user import User
from ..models.role import Role
from ..models.dept import Dept
from ..schemas.base import ResponseBase
from ..utils.response import success_response, error_response

router = APIRouter()

# 角色相关路由
@router.get("/role/list", response_model=ResponseBase[List[Dict[str, Any]]])
async def get_role_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取角色列表"""
    result = await db.execute(select(Role).order_by(Role.id))
    roles = result.scalars().all()
    
    role_list = []
    for role in roles:
        role_list.append({
            "id": role.id,
            "name": role.name,
            "code": role.code,
            "status": role.status,
            "remark": role.remark,
            "created_at": role.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": role.updated_at.strftime("%Y-%m-%d %H:%M:%S") if role.updated_at else None
        })
    
    return success_response(data=role_list)

# 部门相关路由
@router.get("/dept/list", response_model=ResponseBase[List[Dict[str, Any]]])
async def get_dept_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取部门列表"""
    result = await db.execute(select(Dept).order_by(Dept.sort))
    depts = result.scalars().all()
    
    dept_list = []
    for dept in depts:
        dept_list.append({
            "id": dept.id,
            "name": dept.name,
            "parent_id": dept.parent_id,
            "leader": dept.leader,
            "phone": dept.phone,
            "email": dept.email,
            "sort": dept.sort,
            "status": dept.status,
            "created_at": dept.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": dept.updated_at.strftime("%Y-%m-%d %H:%M:%S") if dept.updated_at else None
        })
    
    return success_response(data=dept_list)

# 系统状态相关路由
@router.get("/status", response_model=ResponseBase[Dict[str, Any]])
async def get_system_status(
    current_user: User = Depends(get_current_user)
):
    """获取系统状态"""
    system_info = {
        "status": "running",
        "version": "1.0.0",
        "timestamp": "2024-01-01 00:00:00"
    }
    
    return success_response(data=system_info)
