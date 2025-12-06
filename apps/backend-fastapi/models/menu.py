from sqlalchemy import Column, Integer, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Menu(Base):
    """菜单模型"""
    __tablename__ = "sys_menu"
    
    id = Column(Integer, primary_key=True, index=True, comment="菜单ID")
    name = Column(String(50), nullable=False, comment="菜单名称")
    path = Column(String(100), comment="路由路径")
    component = Column(String(255), comment="组件路径")
    redirect = Column(String(100), comment="重定向路径")
    parent_id = Column(Integer, default=0, comment="父菜单ID")
    type = Column(Integer, nullable=False, comment="菜单类型：0目录，1菜单，2按钮")
    permission = Column(String(100), comment="权限标识")
    icon = Column(String(50), comment="菜单图标")
    sort = Column(Integer, default=0, comment="排序")
    status = Column(Boolean, default=True, comment="状态：0禁用，1启用")
    is_visible = Column(Boolean, default=True, comment="是否可见")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
