from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from core.config import settings
from core.database import init_db
from api import api_router
from schemas.base import ResponseBase

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("初始化数据库...")
    await init_db()
    print("数据库初始化完成")
    
    # 初始化数据
    from utils.init_data import init_all_data
    from core.database import AsyncSessionLocal
    
    # 获取数据库会话并初始化数据
    async with AsyncSessionLocal() as db:
        await init_all_data(db)
    
    yield
    
    # 关闭时执行
    print("应用关闭")

# 创建FastAPI应用
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
    root_path=settings.root_path,
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content=ResponseBase(
            code=500,
            data=None,
            error=str(exc),
            message="Internal Server Error"
        ).model_dump()
    )

# 健康检查
@app.get("/health", response_model=ResponseBase[dict])
async def health_check():
    """健康检查"""
    return ResponseBase(
        data={
            "status": "ok",
            "message": "Service is running"
        }
    )

# 注册API路由
app.include_router(api_router, prefix="")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
