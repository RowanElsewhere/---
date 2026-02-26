#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================="
echo "自动点击器 - 启动脚本"
echo "=========================================="

if ! command -v python3 &> /dev/null; then
    echo ""
    echo "错误: 未检测到 Python3"
    echo ""
    echo "请先安装 Python3:"
    echo "  方法1: 访问 https://www.python.org 下载安装"
    echo "  方法2: 使用 Homebrew: brew install python3"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

echo "检测到 Python3: $(python3 --version)"

echo ""
echo "正在检查/安装依赖..."
pip3 install pyautogui pynput -q 2>/dev/null

echo ""
echo "启动程序..."
echo ""
echo "注意: 首次运行需要授予辅助功能权限"
echo "  系统设置 → 隐私与安全性 → 辅助功能 → 添加终端"
echo ""

python3 auto_clicker.py
