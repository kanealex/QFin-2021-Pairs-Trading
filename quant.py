from sklearn import linear_model
import numpy as np
import pandas as pd
from scipy import stats
from math import floor
from datetime import timedelta


class PairsTradingAlgorithm(QCAlgorithm):
    
    def Initialize(self):
        
        self.SetStartDate(2019,1,1)
        self.SetEndDate(2019,1,20)
        self.SetCash(2000)
        self.numdays = 3780  # set the length of training period
        tickers = ['SYK', 'IQV']
        self.symbols = []
        
        self.threshold = 2
        
        for i in tickers:
            self.symbols.append(self.AddSecurity(SecurityType.Equity, i, Resolution.Minute).Symbol)
        
        for i in self.symbols:
            i.hist_window = RollingWindow[TradeBar](self.numdays) 


    def OnData(self, data):
        
        if not (data.ContainsKey("SYK") and data.ContainsKey("IQV")): return
        
        for symbol in self.symbols:
            symbol.hist_window.Add(data[symbol])
        
    
        price_x = pd.Series([float(i.Close) for i in self.symbols[0].hist_window], 
                             index = [i.Time for i in self.symbols[0].hist_window])
                             
        price_y = pd.Series([float(i.Close) for i in self.symbols[1].hist_window], 
                             index = [i.Time for i in self.symbols[1].hist_window])
                             
        self.Log(len(price_x))     
        if len(price_x) < self.numdays: return
    
        spread = self.regr(np.log(price_x), np.log(price_y))
        mean = np.mean(spread)
        std = np.std(spread)
        ratio = floor(self.Portfolio[self.symbols[1]].Price / self.Portfolio[self.symbols[0]].Price)
        # quantity = float(self.CalculateOrderQuantity(self.symbols[0],0.4)) 
        
        if spread[-1] > mean + self.threshold * std:
            if not self.Portfolio[self.symbols[0]].Quantity > 0 and not self.Portfolio[self.symbols[0]].Quantity < 0:
                self.Sell(self.symbols[1], 10) 
                self.Buy(self.symbols[0],  ratio * 10)
        
        elif spread[-1] < mean - self.threshold * std:
            if not self.Portfolio[self.symbols[0]].Quantity < 0 and not self.Portfolio[self.symbols[0]].Quantity > 0:
                self.Sell(self.symbols[0], 10)
                self.Buy(self.symbols[1], ratio * 10) 

        else:
            self.Liquidate()
        

    
    def regr(self,x,y):
        regr = linear_model.LinearRegression()
        x_constant = np.column_stack([np.ones(len(x)), x])
        regr.fit(x_constant, y)
        beta = regr.coef_[0]
        alpha = regr.intercept_
        spread = y - x*beta - alpha
        return spread