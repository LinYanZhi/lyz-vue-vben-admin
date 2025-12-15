from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any

from core.database import get_db
from api.auth import get_current_user
from models.menu import Menu
from models.user import User
from schemas.base import ResponseBase
from utils.response import success_response, error_response

router = APIRouter()

async def get_menu_tree(menus: List[Menu], parent_id: int = 0) -> List[Dict[str, Any]]:
    """构建菜单树"""
    tree = []
    for menu in menus:
        if menu.parent_id == parent_id:
            children = await get_menu_tree(menus, menu.id)
            menu_dict = {
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
                "isVisible": menu.is_visible,
                "children": children if children else None
            }
            tree.append(menu_dict)
    return tree

@router.get("/all", response_model=ResponseBase[List[Dict[str, Any]]])
async def get_all_menus(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取所有菜单（树形结构）"""
    # 查询所有启用的菜单
    result = await db.execute(
        select(Menu)
        .where(Menu.status == True)
        .order_by(Menu.sort)
    )
    menus = result.scalars().all()
    
    # 构建菜单树
    menu_tree = await get_menu_tree(menus)
    
    return success_response(data=menu_tree)

@router.get("/list", response_model=ResponseBase[List[Dict[str, Any]]])
async def get_menu_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取菜单列表"""
    # 查询所有启用的菜单
    result = await db.execute(
        select(Menu)
        .where(Menu.status == True)
        .order_by(Menu.sort)
    )
    menus = result.scalars().all()
    
    # 转换为列表格式
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
            "isVisible": menu.is_visible
        })
    
    return success_response(data=menu_list)
