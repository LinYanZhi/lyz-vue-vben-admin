from fastapi import APIRouter
from .auth import router as auth_router
from .user import router as user_router
from .menu import router as menu_router
from .system import router as system_router

# 创建主路由
api_router = APIRouter(prefix="")

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证管理"])
api_router.include_router(user_router, prefix="/user", tags=["用户管理"])
api_router.include_router(menu_router, prefix="/menu", tags=["菜单管理"])
api_router.include_router(system_router, prefix="/system", tags=["系统管理"])
