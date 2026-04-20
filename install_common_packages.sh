#!/bin/bash
# 常用 Python 套件一鍵安裝腳本
# 用法: bash install_common_packages.sh

PYTHON="/usr/bin/python3"  # 指定使用系統 Python

echo "=== 安裝常用 Python 套件 ==="

$PYTHON -m pip install --upgrade pip  # 先升級 pip

$PYTHON -m pip install \
    requests \           # HTTP 請求
    pandas \             # 資料處理
    numpy \              # 數值運算
    matplotlib \         # 繪圖
    seaborn \            # 統計繪圖
    scipy \              # 科學計算
    scikit-learn \       # 機器學習
    beautifulsoup4 \     # HTML 解析
    lxml \               # XML/HTML 解析器
    tqdm \               # 進度條
    openpyxl \           # 讀寫 Excel (.xlsx)
    xlrd \               # 讀取舊版 Excel (.xls)
    pillow \             # 圖片處理
    yfinance \           # Yahoo Finance 股票資料
    ta \                 # 技術指標
    mplfinance \         # 股票K線圖

echo "=== 安裝完成 ==="
$PYTHON -m pip list | grep -E "requests|pandas|numpy|matplotlib|yfinance"  # 確認安裝
