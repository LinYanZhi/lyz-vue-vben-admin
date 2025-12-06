from typing import Optional, TypeVar, Generic
from ..schemas.base import ResponseBase

T = TypeVar('T')

def success_response(
    data: Optional[T] = None,
    message: str = "ok"
) -> ResponseBase[T]:
    """成功响应"""
    return ResponseBase(
        code=0,
        data=data,
        error=None,
        message=message
    )

def error_response(
    code: int = -1,
    error: Optional[str] = None,
    message: str = "error"
) -> ResponseBase:
    """错误响应"""
    return ResponseBase(
        code=code,
        data=None,
        error=error or message,
        message=message
    )

def page_response(
    items: list[T],
    total: int,
    page: int = 1,
    page_size: int = 10,
    message: str = "ok"
) -> ResponseBase[dict]:
    """分页响应"""
    return ResponseBase(
        code=0,
        data={
            "items": items,
            "total": total
        },
        error=None,
        message=message
    )
