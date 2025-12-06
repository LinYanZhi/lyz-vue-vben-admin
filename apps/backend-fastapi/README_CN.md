# Vue Vben Admin FastAPI后端

基于FastAPI开发的Vue Vben Admin后端服务，支持MySQL和PostgreSQL数据库。

## 技术栈

- **框架**: FastAPI 0.110.0
- **ORM**: SQLAlchemy 2.0
- **数据库**: MySQL / PostgreSQL
- **认证**: JWT
- **数据验证**: Pydantic V2

## 项目结构

```
apps/backend-fastapi/
├── api/                  # API路由
│   ├── auth/             # 认证相关接口
│   ├── system/           # 系统管理接口
│   └── ...
├── core/                 # 核心配置
│   ├── config.py         # 配置管理
│   ├── database.py       # 数据库连接
│   └── security.py       # 安全相关
├── models/               # SQLAlchemy模型
├── schemas/              # Pydantic模型
├── services/             # 业务逻辑
├── utils/                # 工具函数
│   ├── init_data.py      # 初始化数据
│   └── response.py       # 响应处理
├── main.py               # 应用入口
├── requirements.txt      # 依赖列表
├── .env                  # 环境变量
├── start.sh              # Linux/Mac启动脚本
└── start.bat             # Windows启动脚本
```

## 快速开始

### 1. 安装依赖

```bash
# 进入后端目录
cd apps/backend-fastapi

# 创建虚拟环境（可选）
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `.env` 文件，配置数据库连接信息：

```env
# MySQL配置
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/vben_admin

# 或 PostgreSQL配置
# DATABASE_URL=postgresql+aiopg://postgres:password@localhost:5432/vben_admin
```

### 3. 启动服务

#### Windows

```bash
# 方式1：使用启动脚本
start.bat

# 方式2：直接运行
python -m uvicorn main:app --host 0.0.0.0 --port 3001 --reload
```

#### Linux/Mac

```bash
# 方式1：使用启动脚本
chmod +x start.sh
./start.sh

# 方式2：直接运行
python -m uvicorn main:app --host 0.0.0.0 --port 3001 --reload
```

### 4. 访问服务

- API文档：http://localhost:3001/docs
- 健康检查：http://localhost:3001/health
- 登录接口：http://localhost:3001/auth/login

## 初始化数据

首次启动服务时，会自动初始化以下数据：

### 超级管理员

- 用户名：admin
- 密码：admin123

### 默认角色

- 超级管理员 (super)
- 管理员 (admin)
- 普通用户 (user)

### 默认菜单

- 系统管理
  - 用户管理
  - 角色管理
  - 菜单管理
  - 部门管理

## API接口

### 认证相关

- `POST /auth/login` - 用户登录
- `POST /auth/refresh` - 刷新token
- `POST /auth/logout` - 退出登录
- `GET /auth/codes` - 获取权限码

### 用户相关

- `GET /user/info` - 获取用户信息

### 菜单相关

- `GET /menu/all` - 获取所有菜单（树形结构）
- `GET /menu/list` - 获取菜单列表

### 系统管理

- `GET /system/role/list` - 获取角色列表
- `GET /system/dept/list` - 获取部门列表
- `GET /system/status` - 获取系统状态

## 前端配置

修改前端项目的 `.env.development` 文件：

```env
# 接口地址
VITE_GLOB_API_URL=http://localhost:3001

# 关闭Nitro Mock服务
VITE_NITRO_MOCK=false
```

## 开发说明

### 添加新API

1. 在 `models/` 目录下创建数据库模型
2. 在 `schemas/` 目录下创建Pydantic模型
3. 在 `api/` 目录下创建路由文件
4. 在 `api/__init__.py` 中注册路由

### 数据库迁移

本项目使用SQLAlchemy的自动创建表功能，无需额外的迁移工具。首次启动时会自动创建所有表。

## 部署说明

### 生产环境配置

1. 修改 `.env` 文件：
   - 设置 `DEBUG=False`
   - 设置强随机的 `SECRET_KEY`
   - 配置生产数据库
   - 设置允许的 origins

2. 使用Gunicorn或Uvicorn运行：

```bash
# 使用Uvicorn
uvicorn main:app --host 0.0.0.0 --port 3001 --workers 4

# 使用Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:3001
```

### Docker部署

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
```

## 常见问题

### 1. 数据库连接失败

- 检查数据库服务是否启动
- 检查数据库连接URL是否正确
- 检查数据库用户是否有足够的权限

### 2. 初始化数据失败

- 检查数据库连接是否正常
- 检查数据库表是否已存在

### 3. 跨域问题

- 确保 `.env` 文件中的 `ALLOWED_ORIGINS` 包含前端地址

## 许可证

MIT
