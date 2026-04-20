#!/usr/bin/env python
# coding: utf-8

# In[31]:


i

# In[33]:


import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from tqdm import tqdm, trange

"***********************************************"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

res=requests.get("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm")
#df=pd.read_html("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm")
#df=pd.read_table("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm")
#print(res.text)
soup=BeautifulSoup(res.text)
#print(soup)
table=soup.find_all("table")[0]
symbol=table.find_all(class_="t3t1")

symbols=[]
symbols_chines=[]
for i in symbol:
    symbolnumber=str(i.text[:4])+".TW"
    symbols.append(symbolnumber)
    symbolname=i.text[4:].replace("\n","").replace(" ","")
    symbols_chines.append(symbolname)

df=pd.DataFrame({"symbol":symbols,"symbols_chines":symbols_chines})
df.to_csv("./wallstreet/"+"Top100Symbols"+".csv")
df
newsymbols=symbols
#print(newsymbols)
exchanges=[]
for symbol in newsymbols:
    if len(symbol)==7:
        exchange="TWSE"
    else:
        exchange="TPEX"
    exchanges.append(exchange)
#print(exchanges)
symbols=[]
for txt in newsymbols:
    symbol=txt.split(".")[0]
    symbols.append(symbol)
#print(symbols)
print("Reload symbols")


"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"


length=len(symbols)

Benchmark="TWII"
#Benchmark="2330.TW"
Bench=pd.read_csv("./wallstreet/"+Benchmark+".csv",usecols=["Date","Close"],index_col="Date").rename(columns={"Close":Benchmark}) 
print("Bench=\n",Bench.tail())
#print(symbols)
UsedData={}
for symbol,i in zip(newsymbols,tqdm(range(length))):
    #print(symbol)
    sleep(0.01)
    df_S=pd.read_csv("./wallstreet/"+symbol+".csv",usecols=["Date","Close"],index_col="Date")
    df_S.index=pd.to_datetime(df_S.index).strftime("%Y/%m/%d")
    #print(df_S.tail())
    #df_S=Bench.join(df_S).fillna(method="ffill")
    df_S=Bench.join(df_S).ffill()
    #print(df_S.tail())
    #df_S.plot(title=symbol,secondary_y="Close",figsize=(15,5),grid=True)
    #plt.show()
    df_S["20-day-deduction"]=df_S["Close"].rolling(10).min().shift(10)#移動式停損用
    df_S["sma20"]=df_S["Close"].rolling(20).mean()#定義20均     月線定義
    df_S["sma60"]=df_S["Close"].rolling(60).mean()#定義60均     季線定義
    df_S["sma120"]=df_S["Close"].rolling(120).mean()#定義120均  半年線定義 
    df_S["CS"]=(df_S.Close/df_S.sma20)-1#收盤大於月線的幅度％
    df_S["SM"]=(df_S.sma20/df_S.sma60)-1#月線大於季線的幅度％
    df_S["ML"]=(df_S.sma60/df_S.sma120)-1#季線大於半年線的幅度％
    df_S["r1"]=(df_S.Close/df_S.Close.shift(1))-1#股價自己最近一天的漲跌幅％
    df_S["r5"]=(df_S.Close/df_S.Close.shift(5))-1#股價自己最近五天的漲跌幅％
    df_S["r20"]=(df_S.Close/df_S.Close.shift(20))-1#股價自己最近二十天的漲跌幅％
    #print(df_S.tail())
    df_S["r1_Bench"]=(df_S[Benchmark]/df_S[Benchmark].shift(1))-1#大盤自己最近一天的漲跌幅％
    df_S["r5_Bench"]=(df_S[Benchmark]/df_S[Benchmark].shift(5))-1#大盤自己最近五天的漲跌幅％
    df_S["r20_Bench"]=(df_S[Benchmark]/df_S[Benchmark].shift(20))-1#大盤自己最近二十天的漲跌幅％
    df_S["Alpha1"]=df_S["r1"]-df_S["r1_Bench"]#股價最近一天強於大盤的幅度％
    df_S["Alpha5"]=df_S["r5"]-df_S["r5_Bench"]#股價最近五天強於大盤的幅度％
    df_S["Alpha20"]=df_S["r20"]-df_S["r20_Bench"]#股價最近二十天強於大盤的幅度％
    condition1=(df_S["CS"]>0)&(df_S["SM"]>0)&(df_S["ML"]<0)&(df_S["r1"]>df_S["r1_Bench"])&(df_S["r5"]>df_S["r5_Bench"])&(df_S["r20"]>df_S["r20_Bench"])
    #篩選條件:收盤大於月線 且 月線大於季線 且 季線小於半年線 且 股價最近一天強於大盤 且 股價最近五天強於大盤 且 股價最近二十天強於大盤
    condition2=(df_S["CS"]<0)&(df_S["SM"]<0)&(df_S["ML"]<0)&(df_S["r1"]<df_S["r1_Bench"])&(df_S["r5"]<df_S["r5_Bench"])&(df_S["r20"]<df_S["r20_Bench"])
    df_S["signal_long"]=np.where(condition1,1,0)
    #df_S["signal_short"]=np.where(condition2,-1,0)
    
    UsedData[symbol]=df_S#============================================>算好的資料再丟進去UsedData={}
    df_S=df_S["2000":"2027"]
    
    #df_S[["Close","20-day-deduction","sma20","sma60","sma120","signal_long"]].plot(title=symbol,figsize=(15,3),secondary_y="signal_long",grid=True)
    #df_S[["r1_Bench","r5_Bench","r20_Bench"]].plot(title=symbol+"  Relative Strength to "+Benchmark,figsize=(15,3),secondary_y="Close",grid=True)
    #plt.show()
print(df_S.head())
print(df_S.tail())
columns=UsedData[newsymbols[0]].columns
print(columns)


# In[34]:


lastdate = pd.to_datetime(Bench.index[-1]).strftime("%Y/%m/%d") # 自動抓取 Benchmark (TWII) 最近的一天
df_All=pd.DataFrame(index=columns)#創建一個空的DataFrame 以上面運算好的欄位當作index
#df_All.index=pd.to_datetime(df_All.index).tostrftime("%Y/%m/%d")
print(df_All.tail())
for symbol in newsymbols:
    df=UsedData[symbol].T[lastdate]#以指定的日期把原來的DataFrame(以時間當index) 轉置成以欄位當作index
    #print(type(df))
    df=pd.DataFrame(df)
    #print(df)
    column=df.columns.tolist()[0]#column為指定的日期
    #print(column)
    df=df.rename(columns={column:symbol})#將日期轉換為股票代碼
    #print(df)
    df_All=df_All.join(df)#與原來空的DataFrame合併
print(df_All)#此時的DataFrame為。以計算指標當index  股票代碼為cloumns

df_All=df_All.T
print(df_All)#轉置後的DataFrame為。以股票欄位當index  計算指標為columns

newsymbols=df_All.columns#計算指標
print("newsymbols=",newsymbols)
"""
['TWII', 'Close', '20-day-deduction','sma20', 'sma60', 'sma120',
       'CS', 'SM', 'ML', 'r1', 'r5', 'r20', 'r1_Bench', 'r5_Bench',
       'r20_Bench', 'Alpha1', 'Alpha5', 'Alpha20']
"""
Benchmark_Chinesname="加權指數"
#Benchmark_Chinesname="台積電"
names=[Benchmark_Chinesname,"收","移動式停損點","20均","60均","120均","收盤相對20均乖離率","20均相對60均乖離率","60均相對120均乖離率",
      "最近1日漲跌幅","最近5日漲跌幅","最近20日漲跌幅","最近1日"+Benchmark_Chinesname+"漲跌幅","最近5日"+Benchmark_Chinesname+"漲跌幅","最近20日"+Benchmark_Chinesname+"漲跌幅",
       "最近1日相對"+Benchmark_Chinesname+"漲跌幅","最近5日相對"+Benchmark_Chinesname+"漲跌幅","最近20日相對"+Benchmark_Chinesname+"漲跌幅"]
for symbol,name in zip(newsymbols,names):
    #print(symbo)
    df_All=df_All.rename(columns={symbol:name})


df_All


# In[35]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

res=requests.get("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm")
#df=pd.read_html("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm")
#df=pd.read_table("https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm")
#print(res.text)
soup=BeautifulSoup(res.text)
#print(soup)
table=soup.find_all("table")[0]
symbol=table.find_all(class_="t3t1")

symbols=[]
symbols_chines=[]
for i in symbol:
    symbolnumber=str(i.text[:4])+".TW"
    symbols.append(symbolnumber)
    symbolname=i.text[4:].replace("\n","").replace(" ","")
    symbols_chines.append(symbolname)

df=pd.DataFrame({"symbol":symbols,"symbols_chines":symbols_chines})
df.to_csv("./wallstreet/"+"Top100Symbols"+".csv")
print(df)
newsymbols=symbols
print(newsymbols)
print(symbols_chines)


# In[36]:


print("最近一日交易日=",lastdate)
print("Benchmark=",Benchmark_Chinesname)
df_All=df_All[["收","移動式停損點","最近1日相對"+Benchmark_Chinesname+"漲跌幅","最近5日相對"+Benchmark_Chinesname+"漲跌幅","最近20日相對"+Benchmark_Chinesname+"漲跌幅","收盤相對20均乖離率","20均相對60均乖離率","60均相對120均乖離率"]]

sort_condition1=["R20","R5","R1","CS","SM","ML"]
sort_condition2=["最近20日相對"+Benchmark_Chinesname+"漲跌幅","最近5日相對"+Benchmark_Chinesname+"漲跌幅","最近1日相對"+Benchmark_Chinesname+"漲跌幅","60均相對120均乖離率","20均相對60均乖離率","收盤相對20均乖離率"]
#這是另一個排序  
#就是先排最近20天強於大盤的％ 再排最近5天強於大盤的％ 最後排序是最近一天相對大盤的％
#再排60相對於120均的乖離(ML)  再排20相對於60均的乖離(SM) 再排收盤相對20均的乖離(CS)
df_All=df_All.sort_values(sort_condition2,ascending=[False,False,False,False,False,False])#排序順序分別以最近20天 最近5天 最近1天
df_All.insert(0,"股票名稱","")#先在原來的df_All的第0欄位向後插入一欄叫做股票名稱。給空值

for cell in range(0,df_All.index.size):#一行一行搜尋
    name=df_All.index[cell]#尋找index的值，取得股票代碼
    idx=newsymbols.index(name)#股票代碼在symbols list的位置
    df_All["股票名稱"][cell]=symbols_chines[idx]#將以上的位置帶入symbols_chines list
    #df_All.loc[cell,"股票名稱"]=symbols_chines[idx]#將以上的位置帶入symbols_chines list
    
print("排序邏輯")
print("先跟大盤比==>")
print("先排最近20天強於大盤的％ 再排最近5天強於大盤的％ 最後排序是最近一天相對大盤的％ ")
print("再跟自己比==>")
print("再排60相對於120均的乖離(ML)  再排20相對於60均的乖離(SM) 再排收盤相對20均的乖離(CS)")
#print(df_All)
#df_All.style.format('{:.2%}',subset=["r1","r1_Bench","r5","r5_Bench","r20","r20_Bench","CS","SM","ML"])
formatdic={"收":"{:.1f}","20天前扣抵值":"{:.1f}","最近1日漲跌幅":"{:.2%}","最近5日漲跌幅":"{:.2%}","最近20日漲跌幅":"{:.2%}","最近1日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","最近5日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","最近20日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","收盤相對20均乖離率":"{:.2%}","20均相對60均乖離率":"{:.2%}","60均相對120均乖離率":"{:.2%}"}
df_All=df_All.dropna()
df_All.style.bar(color=["green","red"], align="zero").format(formatdic)




# In[37]:


print("最近一日交易日=",lastdate)
print("===============100大權值股中＿前10強=====================")
print("相對加權指數漲跌幅定義：就是個股跟大盤比(Alpha)=個股最近Ｎ天漲跌幅減大盤最近Ｎ天漲跌幅")
print("排序邏輯")
print("先跟大盤比==>")
print("先排序個股最近20天強於大盤的％ 再排序個股最近5天強於大盤的％ 最後排序是個股最近一天強於大盤的％ ")
print("再跟自己比==>")
print("再排個股自己60均相對於120均的乖離(ML)程度  再排序個股自己的20均相對於60均的乖離(SM)程度 再排序個股自己收盤相對20均的乖離(CS)")
formatdic={"收":"{:.1f}","20天前扣抵值":"{:.1f}","最近1日漲跌幅":"{:.2%}","最近5日漲跌幅":"{:.2%}","最近20日漲跌幅":"{:.2%}","最近1日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","最近5日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","最近20日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","收盤相對20均乖離率":"{:.2%}","20均相對60均乖離率":"{:.2%}","60均相對120均乖離率":"{:.2%}"}
df_All.head(10).style.bar(color=["green","red"], align="zero").format(formatdic)



# In[38]:


print("最近一日交易日=",lastdate)
print("===============100大權值股中＿後10弱=====================")
print("相對加權指數漲跌幅定義：就是跟大盤比(Alpha)=個股最近Ｎ天漲跌幅減大盤最近Ｎ天漲跌幅")
print("排序邏輯")
print("先跟大盤比==>")
print("先排最近20天弱於大盤的％個股 再排最近5天弱於大盤的％個股 最後再排序是最近一天弱於大盤的％個股 ")
print("再跟自己比==>")
print("再排個股自己60均相對於120均的乖離(ML)  再排序個股自己20均相對於60均的乖離(SM) 再排序個股自己收盤相對20均的乖離(CS)")
formatdic={"收":"{:.1f}","20天前扣抵值":"{:.1f}","最近1日漲跌幅":"{:.2%}","最近5日漲跌幅":"{:.2%}","最近20日漲跌幅":"{:.2%}","最近1日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","最近5日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","最近20日相對"+Benchmark_Chinesname+"漲跌幅":"{:.2%}","收盤相對20均乖離率":"{:.2%}","20均相對60均乖離率":"{:.2%}","60均相對120均乖離率":"{:.2%}"}
df_All.tail(10).style.bar(color=["green","red"], align="zero").format(formatdic)


# # 寬度指標

# In[39]:


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime

print(newsymbols)
print("newsymbols Number=",len(newsymbols))
length=len(newsymbols)
AllData={}
for symbol in newsymbols:
    df=pd.read_csv("./wallstreet/"+symbol+".csv",index_col="Date",parse_dates=["Date","Close"]).dropna()
    df.index=pd.to_datetime(df.index).strftime("%Y/%m/%d")
    AllData[symbol]=df
UsedData={}
for symbol in newsymbols:
    df_S=AllData[symbol]
    #print(df_S.tail())
    df_S["Close"]=df_S["Close"].astype(float)
    #print(df_S["Close"].tail())
    df_S["sma20"]=df_S["Close"].rolling(20).mean()
    #print(df_S["sma20"].tail())
    df_S["sma60"]=df_S["Close"].rolling(60).mean()
    df_S["sma120"]=df_S["Close"].rolling(120).mean()  
    
    condition1=df_S["Close"]>df_S["sma20"]
    condition2=df_S["Close"]>df_S["sma60"]
    condition3=df_S["Close"]>df_S["sma120"]
    df_S["signal_sma20"]=np.where(condition1,1,0)
    df_S["signal_sma60"]=np.where(condition2,1,0)
    df_S["signal_sma120"]=np.where(condition3,1,0)
    UsedData[symbol]=df_S
print(newsymbols[-1])
print(UsedData[newsymbols[-1]].tail())
UsedData.keys()


# In[40]:


df_sig_sma20 = pd.DataFrame()
df_sig_sma60 = pd.DataFrame()
df_sig_sma120 = pd.DataFrame()
df_Close = pd.DataFrame()
for symbol in newsymbols:
    df=UsedData[symbol]#df is DataFrame 計算後的
    sig_sma20=df["signal_sma20"]
    sig_sma60=df["signal_sma60"]
    sig_sma120=df["signal_sma120"]
    Close=df["Close"]#Close is Series
    
    df_sig_sma20[symbol] = sig_sma20
    df_sig_sma60[symbol] = sig_sma60
    df_sig_sma120[symbol] = sig_sma120
    df_Close[symbol]=Close
TWII=pd.read_csv("./wallstreet/TWII.csv",usecols=["Date","Close"],index_col="Date").rename(columns={"Close":"TWII"}) 
TWII.index=pd.to_datetime(TWII.index).strftime("%Y/%m/%d")

df_sig_sma20=df_sig_sma20#.dropna()
columns=df_sig_sma20.columns
lenghth=len(columns)

df_sig_sma20["Market_Breadth_Num_sma20"]=df_sig_sma20.sum(axis=1)
df_sig_sma20["Total_StockNum"]=length
df_sig_sma20["Market_Breadth_Ratio_sma20"]=df_sig_sma20["Market_Breadth_Num_sma20"]/df_sig_sma20["Total_StockNum"]

df_sig_sma60=df_sig_sma60#.dropna()
columns=df_sig_sma60.columns
lenghth=len(columns)

df_sig_sma60["Market_Breadth_Num_sma60"]=df_sig_sma60.sum(axis=1)
df_sig_sma60["Total_StockNum"]=length
df_sig_sma60["Market_Breadth_Ratio_sma60"]=df_sig_sma60["Market_Breadth_Num_sma60"]/df_sig_sma60["Total_StockNum"]


df_sig_sma120=df_sig_sma120#.dropna()
columns=df_sig_sma120.columns
lenghth=len(columns)

df_sig_sma120["Market_Breadth_Num_sma120"]=df_sig_sma120.sum(axis=1)
df_sig_sma120["Total_StockNum"]=length
df_sig_sma120["Market_Breadth_Ratio_sma120"]=df_sig_sma120["Market_Breadth_Num_sma120"]/df_sig_sma120["Total_StockNum"]



df_MC=df_sig_sma20[["Market_Breadth_Ratio_sma20"]].rename(columns={"Market_Breadth_Ratio_sma20":"Open"})*100
df_MC["High"]=df_MC["Open"]
df_MC["Low"]=df_MC["Open"]
df_MC["Close"]=df_MC["Open"]
df_MC.to_csv("./wallstreet/Marketbreadth.csv")
df_sig_sma20=df_sig_sma20.join(TWII)
df_sig_sma60=df_sig_sma60.join(TWII)
df_sig_sma120=df_sig_sma120.join(TWII)
df_sig_sma20


# In[41]:


df_sig_sma20=df_sig_sma20["2020":"2027"]
df_sig_sma20[["Market_Breadth_Ratio_sma20","TWII"]].plot(title="Market_Breadth_Num_sma20",secondary_y="TWII",figsize=(15,5),grid=True)
plt.show()
df_sig_sma20.tail()


# In[42]:


df_sig_sma60=df_sig_sma60["2020":"2027"]
df_sig_sma60[["Market_Breadth_Ratio_sma60","TWII"]].plot(title="Market_Breadth_Num_sma60",secondary_y="TWII",figsize=(15,5),grid=True)
plt.show()
df_sig_sma60.tail()


# In[43]:


df_sig_sma120=df_sig_sma120["2020":"2027"]
df_sig_sma120[["Market_Breadth_Ratio_sma120","TWII"]].plot(title="Market_Breadth_Num_sma120",secondary_y="TWII",figsize=(15,5),grid=True)
plt.show()
df_sig_sma120.tail()


# In[44]:


df_sig_sma20[["Market_Breadth_Ratio_sma20","TWII"]].plot(title="Market_Breadth_Num_sma20",secondary_y="TWII",figsize=(15,3),grid=True)
df_sig_sma60[["Market_Breadth_Ratio_sma60","TWII"]].plot(title="Market_Breadth_Num_sma60",secondary_y="TWII",figsize=(15,3),grid=True)
df_sig_sma120[["Market_Breadth_Ratio_sma120","TWII"]].plot(title="Market_Breadth_Num_sma120",secondary_y="TWII",figsize=(15,3),grid=True)

plt.show()


df_sig_sma20=df_sig_sma20[["Market_Breadth_Ratio_sma20","TWII"]].join(df_sig_sma60[["Market_Breadth_Ratio_sma60"]]).join(df_sig_sma120[["Market_Breadth_Ratio_sma120"]])

formatdic={"Market_Breadth_Ratio_sma20":"{:.2%}","Market_Breadth_Ratio_sma60":"{:.2%}","Market_Breadth_Ratio_sma120":"{:.2%}"}


df_sig_sma20.tail().style.format(formatdic)




# In[45]:


df_sig_sma20.plot(title="Market_Breadth__Taiwan Top 100 Market Cap Weighted Stocks",secondary_y="TWII",figsize=(15,8),grid=True)

plt.show()

formatdic={"Market_Breadth_Ratio_sma20":"{:.2%}","TWII":"{:.1f}","Market_Breadth_Ratio_sma60":"{:.2%}","Market_Breadth_Ratio_sma120":"{:.2%}"}
df_sig_sma20.tail(10).style.bar(color=["green","red"], align="zero").format(formatdic)




# In[ ]:




