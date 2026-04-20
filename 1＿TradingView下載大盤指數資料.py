#!/usr/bin/env python # 指定Python直譯器路徑
# coding: utf-8 # 設定檔案編碼為 UTF-8

# In[8]: # Jupyter Notebook 的儲存格標記

import pandas as pd # 匯入 pandas 套件並簡稱 pd，用於資料處理
import numpy as np # 匯入 numpy 套件並簡稱 np，用於數值運算
import matplotlib.pyplot as plt # 匯入 matplotlib.pyplot 套件並簡稱 plt，用於繪圖
from bs4 import BeautifulSoup # 從 bs4 模組匯入 BeautifulSoup，用於解析 HTML
import requests # 匯入 requests 套件，用於發送 HTTP 請求

res=requests.get("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm") # 向指定的網址發送 GET 請求取得網頁資料
#df=pd.read_html("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm") # 嘗試用 pandas 的 read_html 讀取網頁表格（原本被註解掉）
#df=pd.read_table("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm") # 嘗試用 pandas 的 read_table 讀取網頁表格（原本被註解掉）
#print(res.text) # 印出請求回傳的網頁文字內容（原本被註解掉）
soup=BeautifulSoup(res.text, "html.parser") # 將取得的網頁文字丟給 BeautifulSoup 進行解析，並指定為 soup 變數 (加 html.parser 避免警告)
#print(soup) # 印出解析後的 soup 物件（原本被註解掉）
table=soup.find_all("table")[0] # 在 soup 物件中尋找所有的 "table" 標籤，並取得第一個（索引為0）
symbol=table.find_all(class_="t3t1") # 在該表格中找出所有 HTML 類別 (class) 為 "t3t1" 的元素，儲存到 symbol 變數

symbols=[] # 建立一個空的串列，用來準備儲存股票代號
symbols_chines=[] # 建立一個空的串列，用來準備儲存股票中文名稱
for i in symbol: # 使用 for 迴圈遍歷剛剛找到的每一個 symbol 元素
    symbolnumber=str(i.text[:4])+".TW" # 提取文字的前 4 個字元作為股票代號，轉為字串後加上 ".TW" 字尾
    symbols.append(symbolnumber) # 將組合好的股票代號加進 symbols 串列中
    symbolname=i.text[4:].replace("\n","").replace(" ","") # 提取從第 5 個字元開始的文字作為股票名稱，並移除換行符號與空白
    symbols_chines.append(symbolname) # 將處理好的股票名稱加進 symbols_chines 串列中

import os # 匯入 os 模組處理資料夾建立
if not os.path.exists("./wallstreet"): # 若當前目錄下沒有 wallstreet 資料夾
    os.makedirs("./wallstreet") # 建立該資料夾以避免寫入 CSV 失敗
df=pd.DataFrame({"symbol":symbols,"symbols_chines":symbols_chines}) # 使用 pandas 將這兩個串列整理成一個 DataFrame
df.to_csv("./wallstreet/"+"Top100Symbols"+".csv") # 將這個 DataFrame 輸出儲存成 CSV 檔案，指定檔名與路徑
df # 在 Jupyter 裡面代表印出 DataFrame 內容 (如果在一般腳本則無作用)
newsymbols=symbols # 將 symbols 串列賦值給另一個變數 newsymbols
print(newsymbols) # 印出 newsymbols 這個包含所有股票代號的串列
exchanges=[] # 建立一個空的串列 exchanges，準備儲存所屬交易所資訊
for symbol in newsymbols: # 再次把 newsymbols 裡面每一個股票代號拿出來跑迴圈
    if len(symbol)==7: # 判斷如果股票代號長度剛好為 7 (例如 "2330.TW")
        exchange="TWSE" # 設定交易所為 "TWSE" (台灣證券交易所，即上市)
    else: # 否則 (例如代號長度較長或較短)
        exchange="TPEX" # 設定交易所為 "TPEX" (櫃買中心，即上櫃)
    exchanges.append(exchange) # 將判定好的交易所資訊加入到 exchanges 串列
print(exchanges) # 印出所有的交易所串列結果
symbols=[] # 重新將 symbols 變數歸零成空串列
for txt in newsymbols: # 在 newsymbols 裡面每個帶有 ".TW" 的字串跑迴圈
    symbol=txt.split(".")[0] # 用 "." 當作分隔符號切割字串，並只取第一個元素 (純粹的股票數字代號部分)
    symbols.append(symbol) # 把切割好的純數字代號加回到 symbols 串列裡面
print(symbols) # 印出新的只包含純數字代號的 symbols 串列


# In[9]: # Jupyter Notebook 的儲存格標記


import pandas as pd # 再次匯入 pandas 套件
import datetime # 匯入 datetime 套件，用來處理日期與時間資訊
import os # 匯入 os 套件，用來處理作業系統相關的操作（例如檔案路徑）
import matplotlib.pyplot as plt # 再次匯入 matplotlib.pyplot 套件
import time # 匯入 time 套件，用來處理時間延遲功能
from tvDatafeed import TvDatafeed,Interval # 從 tvDatafeed 模組匯入我們需要的工具 TvDatafeed 跟 Interval
import random # 匯入 random 套件，用來產生隨機數

username = 'YourTradingViewUsername' # 將 TradingView 帳號名稱存入 username 變數
password = 'YourTradingViewPassword' # 將 TradingView 密碼存入 password 變數
tv=TvDatafeed(username,password) # 初始化 TvDatafeed 物件以連線 API


# In[ ]: # Jupyter Notebook 的儲存格標記


import pandas as pd # 再次匯入 pandas
import datetime # 再次匯入 datetime 
import os # 再次匯入 os
import requests # 再次匯入 requests
from bs4 import BeautifulSoup # 再次匯入 BeautifulSoup
from tqdm import tqdm # 從 tqdm 模組匯入 tqdm，用於在迴圈中顯示進度條
from time import sleep # 從 time 模組匯入 sleep 函式，用於強制暫停程式

# --- 設定儲存路徑 --- # 設定資料儲存路徑的常數與創立資料夾
save_path = "./wallstreet/" # 寫入預設要儲存的資料夾路徑到變數 save_path 中
if not os.path.exists(save_path): # 判斷如果指定的儲存路徑當前不存在這個系統裡
    os.makedirs(save_path) # 就使用作業系統指令建立好這個目錄結構

# --- 第一部分：從網站獲取最新的股票清單 --- # 第一部分主要功能是抓清單
print("正在獲取最新股票清單...") # 在畫面上印出提示訊息讓使用者知道程式沒當機
res = requests.get("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm") # 對目標網址發出 GET 請求去抓最新的報表
soup = BeautifulSoup(res.text, "html.parser") # 取得的回覆丟進 BeautifulSoup 做格式化
table = soup.find_all("table")[0] # 抓取解析結果中的第一張大表
symbol_elements = table.find_all(class_="t3t1") # 抓出所有 html css 類別為 t3t1 的元素

# 建立當前的日期標記 (YYYY-MM-DD) # 日期標記可以協助判斷資料的新舊程度
today_str = datetime.date.today().strftime("%Y-%m-%d") # 獲取今日日期，並用 .strftime() 將格式固定為年-月-日字串

# --- 第二部分：過濾邏輯（判斷哪些需要下載） --- # 第二部分利用 if 敘述篩選哪些清單真的需要下載
tasks = [] # 準備一個空的任務串列 tasks
for i in symbol_elements: # 將我們上一步抓到的標籤全部跑 for 迴圈逐一處理
    code = i.text[:4] # 該標籤文字的前四碼是股票代碼
    name = i.text[4:].strip() # 第五碼以後是此檔股票名稱，使用 .strip() 來去除不必要的換行與頭尾空格
    full_symbol = f"{code}.TW" # 把股票代碼加上 .TW 以符合 TradingView 對台股的表示方法
    exchange = "TWSE" if len(full_symbol) == 7 else "TPEX" # 如果加了 .TW 是七個字元代表上市 (TWSE)，其餘為上櫃 (TPEX)
    
    file_full_path = os.path.join(save_path, f"{full_symbol}.csv") # 利用 os 把剛設好的目標資料夾與我們要建立的股票csv名稱組合成合法路徑
    
    # 續傳邏輯： # 有了這個就可以不用每次執行都重新抓一遍
    # 1. 如果檔案不存在 -> 必須下載 # 絕對缺少檔案的判定
    # 2. 如果檔案存在，但不是今天下載的 -> 建議重新下載 (更新數據) # 但資料舊了還是得更新
    if not os.path.exists(file_full_path): # 判斷如果先前提到的檔案路徑並不存在
        tasks.append({"symbol": code, "full": full_symbol, "exchange": exchange}) # 那就肯定要下載，加入到任務中
    else: # 否則代表檔案存在的邏輯處理
        # 選項：如果您只想下載「完全沒下載過」的，就註解掉下面這兩行 # 留給開發者的客製化修改空間
        file_mtime = datetime.date.fromtimestamp(os.path.getmtime(file_full_path)).strftime("%Y-%m-%d") # 確認這個既有檔案上次修改的紀錄時間並轉成純字串
        if file_mtime != today_str: # 如果該檔案時間不是今天
            tasks.append({"symbol": code, "full": full_symbol, "exchange": exchange}) # 依舊加入重抓任務，來獲取最新的一根日K的資料

print(f"清單總計: {len(symbol_elements)} 檔") # 在畫面上印出總共有找到幾檔股票清單
print(f"待處理任務 (未下載或需更新): {len(tasks)} 檔") # 以及印出真正過濾篩選後被放到任務內的資料有幾檔

# --- 第三部分：執行下載 --- # 開始最重要的爬蟲 API 下載邏輯
interval = Interval.in_daily # 確保此變數已在您的環境定義 # 定義 TradingView 讀取長度時間以日級別為基準

for item in tqdm(tasks, desc="執行進度"): # 將剛才建立好要抓的任務串列丟進迴圈，tqdm 用於追蹤下載的文字條進度
    try: # try 包裹住 API 連線的可能錯誤
        # 呼叫 TradingView API (tv 為您原本定義的物件) # 將這字典內容傳給 tv 物件
        df = tv.get_hist( # 呼叫 get_hist 取得這支股票的歷史 k 線結果
            symbol=item['symbol'], # 代碼
            exchange=item['exchange'], # 交易所 (TWSE/TPEX)
            n_bars=7000, # 要求拿回 7000 隨機單位的資料
            interval=interval # 就是剛剛說指定的以日為一個單位
        ) # 呼叫完成
        
        if df is not None and not df.empty: # 若回傳結果 df 不等於空值且裡面具有資料內容
            df.index = pd.to_datetime(df.index).strftime("%Y/%m/%d") # 此時先將 pandas 中的索引(原先可能是日期型態)通通重新編碼為 YYYY/MM/DD 的純時間字串
            df.index.name = "Date" # 並規定這個 index 欄位名稱叫做 Date
            df = df[["open", "high", "low", "close"]].rename( # 抽離要使用的四大數據欄位並一併呼叫 rename 直接重新命名成首字大寫
                columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"} # rename 所需輸入的字典映射規則
            ) # 欄位重新整理完成
            df = df.astype(float) # 為了避免混到非預期的資料型態（如字串），將資料整批強制轉為浮點數型態
            
            # 存檔 (會覆蓋舊的或建立新的) # 這裡就會完成檔案的保存
            df.to_csv(os.path.join(save_path, f"{item['full']}.csv")) # 丟入組好的儲存路徑，並寫入本機硬碟中成為 CSV 檔案
            
            # 微小的延遲，防止被 API 封鎖 # 若抓太快會導致 IP 被拉黑名單
            sleep(0.3) # 每次完成一檔下載後就停頓 0.3 秒再開始下一輪的資料下載，模擬人工行為
        else: # 若判定 API 沒有回傳這檔的任何 K 線資料下來
            print(f" [跳過] {item['full']} 無回傳數據") # 就印出 [跳過] 以通知開發者此股無資料
            
    except Exception as e: # 如果 try 出現任何網路連線錯誤或是資料異常，全部接在此避免閃退
        # 如果中途斷網或報錯，印出錯誤並跳過該次，等待下一次重跑 # 有寫 exception 才能跳過這檔繼續執行迴圈
        print(f"\n [錯誤] 下載 {item['full']} 時發生問題: {e}") # 詳細帶出是什麼具體錯誤狀態以便後續 Debug
        print(" 系統將在 5 秒後嘗試下一檔...") # 在這之前宣告休息五秒以平復對方伺服器的連線限制
        sleep(5) # 真的休息五秒鐘來讓網路與伺服器冷卻
        continue # 從下一次迴圈重新開始也就是去繼續下一個任務清單中的股票下載

print("\n任務處理完畢。") # 都跑完了，代表工作結束
print("更新日期:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # 最後抓了最新系統時區顯示給開發者確認當下的結束時間
