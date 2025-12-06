@echo off

:: 启动FastAPI后端服务
echo 启动FastAPI后端服务...
python -m uvicorn main:app --host 0.0.0.0 --port 3001 --reload
