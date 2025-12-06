from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

# 泛型类型变量
T = TypeVar('T')

class ResponseBase(BaseModel, Generic[T]):
    """基础响应模型"""
    code: int = 0
    data: Optional[T] = None
    error: Optional[str] = None
    message: str = "ok"
    
    class Config:
        from_attributes = True

class PageInfo(BaseModel):
    """分页信息"""
    total: int = 0
    page: int = 1
    page_size: int = 10

class PageResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    code: int = 0
    data: Optional[dict] = None
    error: Optional[str] = None
    message: str = "ok"
    
    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int = 1,
        page_size: int = 10
    ) -> "PageResponse[T]":
        """创建分页响应"""
        return cls(
            data={
                "items": items,
                "total": total
            }
        )
    
    class Config:
        from_attributes = True
