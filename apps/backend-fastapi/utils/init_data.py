from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.security import get_password_hash
from models.user import User
from models.role import Role
from models.menu import Menu
from models.dept import Dept

async def init_superuser(db: AsyncSession):
    """初始化超级管理员"""
    # 检查是否已存在超级管理员
    result = await db.execute(select(User).where(User.username == "admin"))
    existing_user = result.scalars().first()
    
    if existing_user:
        print("超级管理员已存在")
        return
    
    # 创建超级管理员
    superuser = User(
        username="admin",
        password=get_password_hash("admin123"),
        nickname="超级管理员",
        name="超级管理员",
        email="admin@example.com",
        phone="13800138000",
        dept_id=1,  # 分配到总公司
        is_superuser=True,
        status=True
    )
    
    db.add(superuser)
    
    try:
        await db.commit()
        print("超级管理员创建成功：用户名=admin，密码=admin123")
    except IntegrityError:
        await db.rollback()
        print("超级管理员创建失败，可能是用户名已存在")
    except Exception as e:
        await db.rollback()
        print(f"超级管理员创建失败：{e}")

async def init_roles(db: AsyncSession):
    """初始化角色"""
    roles = [
        {
            "name": "超级管理员",
            "code": "super",
            "status": True,
            "remark": "系统超级管理员"
        },
        {
            "name": "管理员",
            "code": "admin",
            "status": True,
            "remark": "系统管理员"
        },
        {
            "name": "普通用户",
            "code": "user",
            "status": True,
            "remark": "普通用户"
        }
    ]
    
    for role_data in roles:
        result = await db.execute(select(Role).where(Role.code == role_data["code"]))
        existing_role = result.scalars().first()
        
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
    
    try:
        await db.commit()
        print("角色初始化成功")
    except Exception as e:
        await db.rollback()
        print(f"角色初始化失败：{e}")

async def init_menus(db: AsyncSession):
    """初始化菜单"""
    menus = [
        # 目录
        {
            "name": "系统管理",
            "path": "/system",
            "component": "Layout",
            "redirect": "/system/user",
            "parent_id": 0,
            "type": 0,
            "permission": "",
            "icon": "setting",
            "sort": 1,
            "status": True,
            "is_visible": True
        },
        # 用户管理
        {
            "name": "用户管理",
            "path": "user",
            "component": "system/user/index",
            "redirect": "",
            "parent_id": 1,
            "type": 1,
            "permission": "sys:user:list",
            "icon": "user",
            "sort": 1,
            "status": True,
            "is_visible": True
        },
        # 角色管理
        {
            "name": "角色管理",
            "path": "role",
            "component": "system/role/index",
            "redirect": "",
            "parent_id": 1,
            "type": 1,
            "permission": "sys:role:list",
            "icon": "team",
            "sort": 2,
            "status": True,
            "is_visible": True
        },
        # 菜单管理
        {
            "name": "菜单管理",
            "path": "menu",
            "component": "system/menu/index",
            "redirect": "",
            "parent_id": 1,
            "type": 1,
            "permission": "sys:menu:list",
            "icon": "menu",
            "sort": 3,
            "status": True,
            "is_visible": True
        },
        # 部门管理
        {
            "name": "部门管理",
            "path": "dept",
            "component": "system/dept/index",
            "redirect": "",
            "parent_id": 1,
            "type": 1,
            "permission": "sys:dept:list",
            "icon": "company",
            "sort": 4,
            "status": True,
            "is_visible": True
        }
    ]
    
    for menu_data in menus:
        result = await db.execute(
            select(Menu)
            .where(Menu.name == menu_data["name"])
            .where(Menu.parent_id == menu_data["parent_id"])
        )
        existing_menu = result.scalars().first()
        
        if not existing_menu:
            menu = Menu(**menu_data)
            db.add(menu)
    
    try:
        await db.commit()
        print("菜单初始化成功")
    except Exception as e:
        await db.rollback()
        print(f"菜单初始化失败：{e}")

async def init_depts(db: AsyncSession):
    """初始化部门"""
    depts = [
        {
            "name": "总公司",
            "parent_id": 0,
            "leader": "张三",
            "phone": "13800138000",
            "email": "zhangsan@example.com",
            "sort": 1,
            "status": True
        },
        {
            "name": "技术部",
            "parent_id": 1,
            "leader": "李四",
            "phone": "13800138001",
            "email": "lisi@example.com",
            "sort": 1,
            "status": True
        },
        {
            "name": "市场部",
            "parent_id": 1,
            "leader": "王五",
            "phone": "13800138002",
            "email": "wangwu@example.com",
            "sort": 2,
            "status": True
        },
        {
            "name": "财务部",
            "parent_id": 1,
            "leader": "赵六",
            "phone": "13800138003",
            "email": "zhaoliu@example.com",
            "sort": 3,
            "status": True
        }
    ]
    
    for dept_data in depts:
        result = await db.execute(
            select(Dept)
            .where(Dept.name == dept_data["name"])
            .where(Dept.parent_id == dept_data["parent_id"])
        )
        existing_dept = result.scalars().first()
        
        if not existing_dept:
            dept = Dept(**dept_data)
            db.add(dept)
    
    try:
        await db.commit()
        print("部门初始化成功")
    except Exception as e:
        await db.rollback()
        print(f"部门初始化失败：{e}")

async def init_all_data(db: AsyncSession):
    """初始化所有数据"""
    # 先创建部门（用户依赖部门）
    await init_depts(db)
    # 然后创建角色（用户依赖角色）
    await init_roles(db)
    # 然后创建菜单
    await init_menus(db)
    # 最后创建用户（依赖部门和角色）
    await init_superuser(db)
