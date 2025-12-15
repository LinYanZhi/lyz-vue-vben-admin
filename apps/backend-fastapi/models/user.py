from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "sys_user"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    nickname = Column(String(50), comment="昵称")
    name = Column(String(50), comment="姓名")
    avatar = Column(String(255), comment="头像")
    email = Column(String(100), comment="邮箱")
    phone = Column(String(20), comment="手机号")
    dept_id = Column(Integer, ForeignKey("sys_dept.id"), nullable=True, comment="部门ID")
    status = Column(Boolean, default=True, comment="状态：0禁用，1启用")
    is_superuser = Column(Boolean, default=False, comment="是否为超级管理员")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    roles = relationship("Role", secondary="sys_user_role", back_populates="users")
    dept = relationship("Dept", backref="users")
