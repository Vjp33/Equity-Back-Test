# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:47:35 2015

@author: Vraj Patel
"""
#Import pandas
import pandas as pd

# Decile Price MoM Function
def RankPriceMoM(LookBack,Lag):
    #Import Last Price from Main NameSpace
    from __main__ import PX_LAST Check
    
    RetLB = PX_LAST.pct_change(periods=LookBack-Lag,fill_method=None)
    RetLB = RetLB*Check
    RetTran = RetLB.T
    Ret_Dec = pd.qcut(RetTran.ix[:],10,labels=False)+1
    Ret_Dec= Ret_Dec.T
    Ret_Dec = pd.DataFrame(Ret_Dec)
    Ret_Dec.columns = RetLB.columns
    Ret_Dec.index = RetLB.index
    return Ret_Dec

# Decile Value Function
def RankValue():
    #Import Book2Price from Main NameSpace
    from __main__ import Book2Price
    
    B2PT = Book2Price.T
    B2P_Dec = pd.qcut(B2PT.ix[:],10,labels=False)+1
    B2P_Dec= B2P_Dec.T
    B2P_Dec = pd.DataFrame(B2P_Dec)
    B2P_Dec.columns = Book2Price.columns
    B2P_Dec.index = Book2Price.index
    return B2P_Dec

# Zscore Gross Profit
def Zscore(Data):
    Metric = Data
    for x in Metric.index:
        Metric.loc[x,:]= (Metric.loc[x,:]-Metric.loc[x,:].mean(axies=0))/Metric.loc[x,:].std(axies=0)
    ZScore = Metric
    return ZScore

# Test Model Function
def ModelCheck(Model,LookBack,Rebalance,Lag):
    #Import Variables from Main NameSpace
    from __main__ import PX_LAST,TopD,BotD
    
    Ret = PX_LAST.pct_change(periods=Rebalance,fill_method=None)
    Ret = Ret.fillna(method='ffill')
    for x in range(LookBack,(PX_LAST.index.size-Rebalance), Rebalance):
        one = Model.ix[x-Lag].order(ascending=False).dropna()
        TopName = one[:(one.size/10)].index # Names to buy
        TopD.append(Ret[TopName].ix[x+Rebalance].mean()) # Return when sold 
        BotName = one[-(one.size/10):].index # Buy
        BotD.append(Ret[BotName].ix[x+Rebalance].mean())
    return   

