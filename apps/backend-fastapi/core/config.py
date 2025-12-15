from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """项目配置类"""
    # 项目基本信息
    project_name: str = Field(default="Vue Vben Admin FastAPI Backend")
    version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)
    
    # 数据库配置
    database_url: str = Field(..., description="数据库连接URL")
    
    # JWT配置
    secret_key: str = Field(..., description="JWT密钥")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)
    
    # CORS配置
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])
    
    # 项目根路径
    root_path: str = Field(default="")
    
    # 服务端口
    port: int = Field(default=3001)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

# 创建全局配置实例
settings = Settings()
