
import numpy as np
from statsmodels.tsa.stattools import coint



def general_comparison(comparison_function, company_tickers, time_period=50, resolution="daily" ):
    """
    Returns a list of company pairs in order of correlation (lowest to highest value) based on the comparison_function passed to it.
    
    INPUT:
        comparison_function         Any comparison function (correlation between two companies) that returns a integer/float
        company_tickers             List of companies to be compared
        resolution                  Resolution/granularity of data desired. May be "Tick","Second","Minute","Hour","Daily"
        time_period                 Number of values of given resolution to be compared for correlation
    
    
    OUTPUT:
        pairs                       list of company pairs and their correlation values, ordered from lowest to highest correlation values
    
    Last Edited:                    30/04/2021 Kevin SM
    """
    
    pairs = []
    qb = QuantBook()
    
    for ticker in company_tickers:
        qb.AddEquity(ticker)
        
    
    #create pairs array
    for i in range(len(tickers)-1):
        for j in range(i+1,len(tickers)):
            pairs.append([tickers[i],tickers[j],1])
    
    if (resolution=="daily"):
        h1 = qb.History(qb.Securities.Keys, time_period, Resolution.Daily)
    elif (resolution=="hour"):
        h1 = qb.History(qb.Securities.Keys, time_period, Resolution.Hour)
    elif (resolution=="Minute"):
        h1 = qb.History(qb.Securities.Keys, time_period, Resolution.Minute)
    elif (resolution=="Second"):
        h1 = qb.History(qb.Securities.Keys, time_period, Resolution.Second)
    elif (resolution=="Tick"):
        h1 = qb.History(qb.Securities.Keys, time_period, Resolution.Tick)
    else:
        print("Invalid resolution")
        return -1
        
    for pair in pairs:
        score= comparison_function(h1.loc[pair[0]]['close'], h1.loc[pair[1]]['close'])
        pair[2] = score
      
    pairs.sort(key=lambda x: x[2]) 
    return pairs
        
    
def coint_evaluator(history1,history2):
    score, pval, _ = coint(h1.loc[pair[0]]['close'], h1.loc[pair[1]]['close'])
    return pval
        
        
    

    

# Your New Python File