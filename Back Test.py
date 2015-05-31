# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 09:45:15 2015

@author: Vraj Patel
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import VrajModel as VM

#Load Data
os.chdir('F:\Media\Drive\Quant\Data')
Data = pd.HDFStore('Data.h5')
Tickers = Data.R1K_Ticker
Tickers = Tickers.ix[695:].resample('M')
PX_LAST = Tickers.loc[:,(slice(None),slice('PX_LAST','PX_LAST'))]
PX_LAST.columns = PX_LAST.columns.get_level_values(0)
Flds = ['BOOK_VAL_PER_SH','GROSS_PROFIT','BS_TOT_ASSET','NORMALIZED_ROA','NORMALIZED_ROE','CF_FREE_CASH_FLOW','GROSS_MARGIN']
Data_Field = {}
for x in Flds:
    Data_Field[x] = Tickers.loc[:,(slice(None),slice(x,x))].ffill()
    Data_Field[x].columns = Data_Field[x].columns.get_level_values(0)
del x

# Formating Data For Quality Measuers
GrossProfitOverAssets = Data_Field['GROSS_PROFIT']/Data_Field['BS_TOT_ASSET']
CashFlowOverAssets = Data_Field['CF_FREE_CASH_FLOW']/Data_Field['BS_TOT_ASSET']

# Check to see if Tickers were on Russel Index at given date
    # Fix the way you check, Maybe get rid of the Excel component
os.chdir('F:\Media\Drive\Quant\Excel Files')
Check = pd.read_csv('RIY Check.csv',index_col=0,parse_dates=True).resample('M',how='sum')
# PX_LAST = PX_LAST*Check # Line shoud not be Hear
Book2Price = (Data_Field['BOOK_VAL_PER_SH']/PX_LAST)*Check

# Get Price Scores
Price_MoM = VM.RankPriceMoM(9,0)


# Get Value Scores
Value_Rank = VM.RankValue()
MFM = Price_MoM + Value_Rank

# Get Z Score for Profitability Metrics
GPOA_Z = VM.Zscore(GrossProfitOverAssets)
CFOA_Z = VM.Zscore(CashFlowOverAssets)
ROA_Z = VM.Zscore(Data_Field['NORMALIZED_ROA'])
ROE_Z = VM.Zscore(Data_Field['NORMALIZED_ROE'])
GM_Z = VM.Zscore(Data_Field['GROSS_MARGIN'])
Profiability = GPOA_Z+CFOA_Z+ROA_Z+ROE_Z+GM_Z
Prof_Z = VM.Zscore(Profiability)*Check



# Test Model
TopD= []
BotD= []
VM.ModelCheck(Value_Rank,9,1,0)
Top = pd.Series(data=TopD)
Bot = pd.Series(data=BotD)
TminusB = Top-Bot
del TopD,BotD

# Growth of a Dollar
Tg = [1]
Bg = [1]
LSg= [1]

# Had to Add +1 to Top[i] because of NaN in first cell of Tg
for i in range(0,(Top.size-1)):
    Tg.append(Tg[i]*Top[i+1]+Tg[i])
    Bg.append(Bg[i]*Bot[i+1]+Bg[i])
    LSg.append(LSg[i]*TminusB[i+1]+LSg[i])

Tg = pd.Series(data=Tg)
Bg = pd.Series(data=Bg)
TBg = Tg-Bg
LSg = pd.Series(data=LSg)

plt.figure
Tg.plot(label='Top Port')
Bg.plot(label='Bot Port')
LSg.plot(label='Long Short Port')
plt.legend(loc='best')
plt.title('Test')
