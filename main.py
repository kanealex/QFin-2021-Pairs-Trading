from sklearn.linear_model import LinearRegression
from datetime import datetime, date, time
import numpy as np

class PairsTradingAlgorithm(QCAlgorithm):
    
    closes_by_symbol = {}
    
    def Initialize(self):
        
        #first month is always training, doesnt start trading until one month from this date
        self.SetStartDate(2021,2,1) 
        self.SetEndDate(2021,5,1)
        self.SetCash(20000)
        
        #ensures trading does not happen until training period complete
        self.counter = 0
        #sets the start of trading
        self.startTrading = datetime(2021,4,1)
        # set the length of training period, currently ~1 month (1 (month)* 4 (weeks)* 9 (hours)* 60 (minutes))
        self.slidingWindow = 10800  
        
        #number of standard deviations from spread pairs are before trading
        #higher number; less trades
        self.threshold = 2.
        
        self.x_symbol = self.AddEquity('NOV', Resolution.Minute).Symbol
        self.y_symbol = self.AddEquity('HAL', Resolution.Minute).Symbol
        
        #sets fees to 0.01%
        self.Securities[self.x_symbol].SetFeeModel(CustomFeeModel())
        self.Securities[self.y_symbol].SetFeeModel(CustomFeeModel())
        
        #starts default training 
        for symbol in [self.x_symbol, self.y_symbol]:
            history = self.History(symbol, self.slidingWindow, Resolution.Minute)
            if not history.empty:
                self.closes_by_symbol[symbol] = history.loc[symbol].close.values
            else:
                self.closes_by_symbol[symbol] = np.array([])
                

    def OnData(self, data):
        
        #checks if data is empty
        for symbol in self.closes_by_symbol.keys():
            if not data.Bars.ContainsKey(symbol):
                return
        
        #moves rolling window across by one
        for symbol, closes in self.closes_by_symbol.items():
            self.closes_by_symbol[symbol] = np.append(closes, data[symbol].Close)[-len(closes):]
    
        
        #checks if still in training period
        if(self.Time < self.startTrading): return
        
    
        #linear regression preparation
        log_close_x = np.log(self.closes_by_symbol[self.x_symbol])
        log_close_y = np.log(self.closes_by_symbol[self.y_symbol])

        spread = self.regr(log_close_x, log_close_y)
        mean = np.mean(spread)
        std = np.std(spread)
        
        x_holdings = self.Portfolio[self.x_symbol]
        
        if x_holdings.Invested:
            if x_holdings.IsShort and spread[-1] <= mean or \
                x_holdings.IsLong and spread[-1] >= mean:
                self.Liquidate()
        else:
            if spread[-1] < mean - self.threshold * std:
                #short HAL, long NOV
                self.SetHoldings(self.y_symbol, -0.5) 
                self.SetHoldings(self.x_symbol, 0.5)
            if spread[-1] > mean + self.threshold * std:
                #short NOV, long HAL
                self.SetHoldings(self.x_symbol, -0.5)
                self.SetHoldings(self.y_symbol, 0.5) 

    
    #imports standard linear regression model
    def regr(self, x, y):
        regr = LinearRegression()
        x_constant = np.column_stack([np.ones(len(x)), x])
        regr.fit(x_constant, y)
        beta = regr.coef_[1]
        alpha = regr.intercept_
        #calculates spread
        spread = y - x*beta - alpha
        return spread
        
        
#sets custom fees to 0.01% per trade
class CustomFeeModel:
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity* 0.0001
        return OrderFee(CashAmount(fee, 'USD'))