#!/bin/bash

# 1. 切換到你的專案目錄
cd /Users/markchao/mark_Antigravity/download

# 2. 依序執行 Python 獲取最新資料
# 若有其他需要執行的可接續往下寫
python3 1＿TradingView下載大盤指數資料.py
python3 2_TradingView下載股票資料與債券殖利率資料.py

# 3. 將腳本與下載好的資料夾加入 Git 追蹤
git add 1＿TradingView下載大盤指數資料.py 
git add 2_TradingView下載股票資料與債券殖利率資料.py 
git add wallstreet/

# 4. 提交這些異動紀錄
git commit -m "Auto update data: $(date '+%Y-%m-%d %H:%M:%S')"

# 5. 推送至 GitHub（假設分支是 main，如果是 master 請改掉 origin master）
git push origin main
