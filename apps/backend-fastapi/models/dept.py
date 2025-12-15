from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Dept(Base):
    """部门模型"""
    __tablename__ = "sys_dept"
    
    id = Column(Integer, primary_key=True, index=True, comment="部门ID")
    name = Column(String(50), nullable=False, comment="部门名称")
    parent_id = Column(Integer, default=0, comment="父部门ID")
    leader = Column(String(20), comment="负责人")
    phone = Column(String(20), comment="联系电话")
    email = Column(String(100), comment="邮箱")
    sort = Column(Integer, default=0, comment="排序")
    status = Column(Boolean, default=True, comment="状态：0禁用，1启用")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
