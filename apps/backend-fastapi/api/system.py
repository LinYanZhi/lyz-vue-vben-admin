from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any, Optional

from core.database import get_db
from api.auth import get_current_user
from models.user import User
from models.role import Role
from models.dept import Dept
from models.menu import Menu
from schemas.base import ResponseBase
from utils.response import success_response, error_response

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

# 用户相关路由
@router.get("/user/list", response_model=ResponseBase[Dict[str, Any]])
async def get_user_list(
    page: int = Query(default=1, ge=1, description="页码"),
    pageSize: int = Query(default=20, ge=1, le=100, description="每页条数"),
    username: Optional[str] = Query(default=None, description="用户名"),
    nickname: Optional[str] = Query(default=None, description="昵称"),
    name: Optional[str] = Query(default=None, description="姓名"),
    email: Optional[str] = Query(default=None, description="邮箱"),
    phone: Optional[str] = Query(default=None, description="手机号"),
    status: Optional[bool] = Query(default=None, description="状态"),
    role_id: Optional[int] = Query(default=None, description="角色ID"),
    dept_id: Optional[int] = Query(default=None, description="部门ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户列表"""
    # 构建查询，使用selectinload预加载角色信息
    query = select(User).options(selectinload(User.roles))
    
    # 条件过滤
    if username:
        query = query.where(User.username.like(f"%{username}%"))
    if nickname:
        query = query.where(User.nickname.like(f"%{nickname}%"))
    if name:
        query = query.where(User.name.like(f"%{name}%"))
    if email:
        query = query.where(User.email.like(f"%{email}%"))
    if phone:
        query = query.where(User.phone.like(f"%{phone}%"))
    if status is not None:
        query = query.where(User.status == status)
    if dept_id:
        query = query.where(User.dept_id == dept_id)
    
    # 统计总条数
    count_query = select(func.count(User.id)).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    # 分页查询
    offset = (page - 1) * pageSize
    query = query.offset(offset).limit(pageSize).order_by(User.id.desc())
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    # 格式化用户数据
    user_list = []
    for user in users:
        # 获取部门信息
        dept_name = None
        if user.dept_id:
            dept_result = await db.execute(select(Dept).where(Dept.id == user.dept_id))
            dept = dept_result.scalars().first()
            if dept:
                dept_name = dept.name
        
        # 获取角色信息（已通过预加载获取）
        roles = []
        for role in user.roles:
            roles.append({
                "id": role.id,
                "name": role.name,
                "code": role.code
            })
        
        user_list.append({
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "avatar": user.avatar,
            "dept_id": user.dept_id,
            "deptName": dept_name,
            "roles": roles,
            "status": user.status,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if user.updated_at else None
        })
    
    # 构建分页响应
    response_data = {
        "items": user_list,
        "total": total,
        "page": page,
        "pageSize": pageSize
    }
    
    return success_response(data=response_data)

# 创建用户
@router.post("/user", response_model=ResponseBase)
async def create_user(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建用户"""
    # 检查用户名是否已存在
    existing_user = await db.execute(select(User).where(User.username == data.get("username")))
    if existing_user.scalar():
        return error_response(code=400, message="用户名已存在")
    
    # 创建新用户
    new_user = User(
        username=data.get("username"),
        nickname=data.get("nickname"),
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        avatar=data.get("avatar"),
        dept_id=data.get("dept_id"),
        status=data.get("status", True),
        password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 默认密码：123456
    )
    
    # 添加角色关联
    if "role_ids" in data and data["role_ids"]:
        role_result = await db.execute(select(Role).where(Role.id.in_(data["role_ids"])))
        new_user.roles.extend(role_result.scalars().all())
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return success_response(message="用户创建成功")

# 更新用户
@router.put("/user/{id}", response_model=ResponseBase)
async def update_user(
    id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    # 查询用户
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalars().first()
    
    if not user:
        return error_response(code=404, message="用户不存在")
    
    # 更新用户基本信息
    if "nickname" in data:
        user.nickname = data["nickname"]
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "phone" in data:
        user.phone = data["phone"]
    if "avatar" in data:
        user.avatar = data["avatar"]
    if "dept_id" in data:
        user.dept_id = data["dept_id"]
    if "status" in data:
        user.status = data["status"]
    if "password" in data:
        user.password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 密码：123456
    
    # 更新角色关联
    if "role_ids" in data:
        # 清除现有角色
        user.roles.clear()
        
        # 添加新角色
        if data["role_ids"]:
            role_result = await db.execute(select(Role).where(Role.id.in_(data["role_ids"])))
            user.roles.extend(role_result.scalars().all())
    
    await db.commit()
    await db.refresh(user)
    
    return success_response(message="用户更新成功")

# 删除用户
@router.delete("/user", response_model=ResponseBase)
async def delete_user(
    request_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除用户"""
    ids = request_data.get("ids")
    
    if not ids:
        return error_response(code=400, message="请选择要删除的用户")
    
    # 删除用户
    await db.execute(User.__table__.delete().where(User.id.in_(ids)))
    await db.commit()
    
    return success_response(message="用户删除成功")

# 更新用户状态
@router.put("/user/status", response_model=ResponseBase)
async def update_user_status(
    request_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户状态"""
    ids = request_data.get("ids")
    status = request_data.get("status", False)
    
    if not ids:
        return error_response(code=400, message="请选择要更新的用户")
    
    # 更新用户状态
    await db.execute(User.__table__.update().where(User.id.in_(ids)).values(status=status))
    await db.commit()
    
    return success_response(message="用户状态更新成功")

# 菜单相关路由
@router.get("/menu/list", response_model=ResponseBase[Dict[str, Any]])
async def get_menu_list(
    page: int = Query(default=1, ge=1, description="页码"),
    pageSize: int = Query(default=20, ge=1, le=100, description="每页条数"),
    name: Optional[str] = Query(default=None, description="菜单名称"),
    status: Optional[bool] = Query(default=None, description="状态"),
    type: Optional[int] = Query(default=None, description="菜单类型"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取菜单列表"""
    # 构建查询
    query = select(Menu)
    
    # 条件过滤
    if name:
        query = query.where(Menu.name.like(f"%{name}%"))
    if status is not None:
        query = query.where(Menu.status == status)
    if type is not None:
        query = query.where(Menu.type == type)
    
    # 统计总条数
    count_query = select(func.count(Menu.id)).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    # 分页查询
    offset = (page - 1) * pageSize
    query = query.offset(offset).limit(pageSize).order_by(Menu.sort)
    
    result = await db.execute(query)
    menus = result.scalars().all()
    
    # 格式化菜单数据
    menu_list = []
    for menu in menus:
        menu_list.append({
            "id": menu.id,
            "name": menu.name,
            "path": menu.path,
            "component": menu.component,
            "redirect": menu.redirect,
            "parent_id": menu.parent_id,
            "type": menu.type,
            "permission": menu.permission,
            "icon": menu.icon,
            "sort": menu.sort,
            "status": menu.status,
            "hidden": not menu.is_visible,
            "created_at": menu.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": menu.updated_at.strftime("%Y-%m-%d %H:%M:%S") if menu.updated_at else None
        })
    
    # 构建分页响应
    response_data = {
        "items": menu_list,
        "total": total,
        "page": page,
        "pageSize": pageSize
    }
    
    return success_response(data=response_data)

# 创建菜单
@router.post("/menu", response_model=ResponseBase)
async def create_menu(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建菜单"""
    # 检查菜单名称是否已存在
    existing_menu = await db.execute(select(Menu).where(Menu.name == data.get("name")))
    if existing_menu.scalar():
        return error_response(code=400, message="菜单名称已存在")
    
    # 创建新菜单
    new_menu = Menu(
        name=data.get("name"),
        path=data.get("path"),
        component=data.get("component"),
        redirect=data.get("redirect"),
        parent_id=data.get("parentId", 0),
        type=data.get("type"),
        permission=data.get("permission"),
        icon=data.get("icon"),
        sort=data.get("sort", 0),
        status=data.get("status", True),
        is_visible=not data.get("hidden", False)
    )
    
    db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    
    return success_response(message="菜单创建成功")

# 更新菜单
@router.put("/menu/{id}", response_model=ResponseBase)
async def update_menu(
    id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新菜单信息"""
    # 查询菜单
    result = await db.execute(select(Menu).where(Menu.id == id))
    menu = result.scalars().first()
    
    if not menu:
        return error_response(code=404, message="菜单不存在")
    
    # 更新菜单信息
    menu.name = data.get("name", menu.name)
    menu.path = data.get("path", menu.path)
    menu.component = data.get("component", menu.component)
    menu.redirect = data.get("redirect", menu.redirect)
    menu.parent_id = data.get("parentId", menu.parent_id)
    menu.type = data.get("type", menu.type)
    menu.permission = data.get("permission", menu.permission)
    menu.icon = data.get("icon", menu.icon)
    menu.sort = data.get("sort", menu.sort)
    menu.status = data.get("status", menu.status)
    menu.is_visible = not data.get("hidden", not menu.is_visible)
    
    await db.commit()
    await db.refresh(menu)
    
    return success_response(message="菜单更新成功")

# 删除菜单
@router.delete("/menu", response_model=ResponseBase)
async def delete_menu(
    request_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除菜单"""
    ids = request_data.get("ids")
    
    if not ids:
        return error_response(code=400, message="请选择要删除的菜单")
    
    # 删除菜单
    await db.execute(Menu.__table__.delete().where(Menu.id.in_(ids)))
    await db.commit()
    
    return success_response(message="菜单删除成功")

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
