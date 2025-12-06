from sqlalchemy import Column, Integer, ForeignKey
from ..core.database import Base

class UserRole(Base):
    """用户角色关联模型"""
    __tablename__ = "sys_user_role"
    
    id = Column(Integer, primary_key=True, index=True, comment="ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    role_id = Column(Integer, ForeignKey("sys_role.id"), nullable=False, comment="角色ID")
