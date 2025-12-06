# FastAPI Backend for Vue Vben Admin

## 技术栈

- FastAPI
- SQLAlchemy 2.0
- MySQL/PostgreSQL
- Pydantic V2

## 项目结构

```
apps/backend-fastapi/
├── api/                  # API路由
│   ├── auth/             # 认证相关接口
│   ├── system/           # 系统管理接口
│   └── ...
├── core/                 # 核心配置
│   ├── config.py         # 配置管理
│   └── security.py       # 安全相关
├── models/               # SQLAlchemy模型
├── schemas/              # Pydantic模型
├── services/             # 业务逻辑
├── utils/                # 工具函数
├── main.py               # 应用入口
├── requirements.txt      # 依赖列表
└── .env                  # 环境变量
```
