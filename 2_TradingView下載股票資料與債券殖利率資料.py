#!/usr/bin/env python
# coding: utf-8

# In[94]:


import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import time
from tvDatafeed import TvDatafeed,Interval
import random

username = 'YourTradingViewUsername'
password = 'YourTradingViewPassword'
tv=TvDatafeed(username,password)


# In[97]:


import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import time
from time import sleep
from tqdm import tqdm, trange

"""
DJI:Dow Jones Industrial Average Index
VXD:DJIA Volatility Index
VXN:Nqsdaq100 Volatility Index

RXI=全球非必需性消費品ETF  市值加權
KXI=全球1200大必須性消費品ETF 
GOL=Barrick Gold 巴菲特持股的金礦開採公司

投資者通常還會在標準普爾（Standard＆Poor）領導的這一領域中尋找行業。標準普爾的管理：

標普通信服務精選行業（XLC）
標普消費者自由選擇行業（XLY）
標普消費必需品精選板塊（XLP）
標普能源精選板塊（XLE）
標普金融精選板塊（XLF）
標普保健精選行業（XLV）
標普工業精選板塊（XLI）
標普材料精選行業（XLB）
標普房地產精選板塊（XLRE）
標普技術精選板塊（XLK）
標普公用事業精選行業（XLU）

VTI:全市場ETF
DBC:追蹤商品指數ETF



"""
symbols=["TAIEX","0050","3090","00922","00878","USDHKD","AUDUSD","USDCHF","NZDUSD","USDCAD","USDRUB","USDTWD","USDCNY","00713","2330","2317","2454","2603","2609","6505","2412","1301","1303","1326","2881","2882","0050","0056","6206","6138","3661","HYG","LQD","TIP","SPY","SOXX","QQQ","DJI","VTI","DBC","VXFXICLS","VT"]
exchanges=["TWSE","TWSE","TWSE","TWSE","TWSE","FX","FX","FX_IDC","FX_IDC","FX","FX_IDC","FX_IDC","FX_IDC","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TWSE","TPEX","TWSE","AMEX","AMEX","AMEX","AMEX","NASDAQ","NASDAQ","DJ","AMEX","AMEX","FRED","AMEX"]
newsymbols=["TWII","0050.TW","3090.TW","00922.TW","00878.TW","USDHKD","AUDUSD","USDCHF","NZDUSD","USDCAD","USDRUB","USDTWD","USDCNY","00713.TW","2330.TW","2317.TW","2454.TW","2603.TW","2609.TW","6505.TW","2412.TW","1301.TW","1303.TW","1326.TW","2881.TW","2882.TW","0050.TW","0056.TW","6206.TW","6138.TWO","3661.TW","HYG","LQD","TIP","SPY","SOXX","QQQ","DJI","VTI","DBC","ChinaVIX","VT"]
interval=Interval.in_daily
#interval=Interval.in_1_hour
#interval=Interval.in_1_minute
print("Initail length:",len(symbols))

save_path = "./wallstreet/"
if not os.path.exists(save_path):
    os.makedirs(save_path)
today_str = datetime.date.today().strftime("%Y-%m-%d")

tasks = []
for symbol, exchange, newsymbol in zip(symbols, exchanges, newsymbols):
    file_full_path = os.path.join(save_path, f"{newsymbol}.csv")
    if not os.path.exists(file_full_path):
        tasks.append((symbol, exchange, newsymbol))
    else:
        file_mtime = datetime.date.fromtimestamp(os.path.getmtime(file_full_path)).strftime("%Y-%m-%d")
        if file_mtime != today_str:
            tasks.append((symbol, exchange, newsymbol))

print("Adjusted length (tasks to download):", len(tasks))

for symbol, exchange, newsymbol in tqdm(tasks, desc="股票資料下載進度"):
    try:
        sleep(0.3)
        df = tv.get_hist(symbol=symbol, exchange=exchange, n_bars=15000, interval=interval)
        if df is not None and not df.empty:
            df.index=pd.to_datetime(df.index).strftime("%Y/%m/%d")
            df.index.name="Date"
            df=df[["open","high","low","close"]].rename(columns={"open":"Open","high":"High","low":"Low","close":"Close"})
            df = df.astype(float)
            df.to_csv(os.path.join(save_path, f"{newsymbol}.csv"))
    except Exception as e:
        print(f"\n [錯誤] 下載 {newsymbol} 時發生問題: {e}")
        sleep(5)
        continue

print("商品代碼=",newsymbols)


print("Download Finished")
date=datetime.date.today()
print("Update Date=",date)





# In[ ]:




