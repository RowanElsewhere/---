@echo off
chcp 65001 >nul
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python3
    echo 下载地址: https://www.python.org
    pause
    exit /b 1
)

pip install -r requirements.txt -q
python auto_clicker.py
