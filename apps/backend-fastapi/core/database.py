from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
from core.config import settings
import re

# 从数据库URL中提取数据库名称
async def create_database_if_not_exists():
    """如果数据库不存在则创建"""
    # 提取数据库名称
    db_name_match = re.search(r'/([^/]+)(?:\?|$)', settings.database_url)
    if not db_name_match:
        raise ValueError(f"无法从URL中提取数据库名称: {settings.database_url}")
    db_name = db_name_match.group(1)
    
    # 创建不包含数据库名称的连接URL
    base_url = settings.database_url.replace(f"/{db_name}", "")
    
    # 创建临时引擎连接到MySQL服务器
    temp_engine = create_async_engine(
        base_url,
        echo=settings.debug,
        future=True,
    )
    
    try:
            async with temp_engine.begin() as conn:
                # 创建数据库
                await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                await conn.execute(text(f"USE `{db_name}`"))
    finally:
        await temp_engine.dispose()

# 创建异步引擎
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# 创建基础模型类
Base = declarative_base()

async def get_db():
    """获取数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """初始化数据库"""
    # 先创建数据库（如果不存在）
    await create_database_if_not_exists()
    
    # 先删除所有表，然后重新创建（用于开发环境更新表结构）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
