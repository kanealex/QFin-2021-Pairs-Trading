# -*- coding: utf-8 -*-
"""
Created on Wed May 12 20:50:42 2021

@author: User01
"""
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
from datetime import date
import numpy as np
import os 
import time
import itertools


file_location="D:\My Desktop\QFin\Data\quantitativeFinance-master"

def __main__():
    tickers=return_industry_list("Health_Care")
    print(compare_all(tickers,up_down_comparison))
    
def return_industry_list(industry):
    DIR=file_location+"\\SectorTickers\\"+industry+".csv"
    try: 
        industry_file=pd.read_csv(DIR)
    except FileNotFoundError:
        print("Industry not found:"+industry)
    #print(industry_file)
    return industry_file.Ticker

def compare_all(tickers, comparison_algorithm):
    
    pairs=generate_pairs(tickers)
    scores=[]
    for i in tqdm(range(len(pairs))):
        
        score=comparison_algorithm(pairs[i][0],pairs[i][1])
        
        pairs[i].append(score)
        if (i//100==0):
            
            pairs_df=pd.DataFrame(pairs,columns=["ticker1","ticker2","score"])
            pairs_df.to_csv(file_location+"\\partial_results.csv")
                
        #scores.append(comparison_algorithm([pairs[i][0]],[pairs[i][1]]))
        
    pairs.sort(key=lambda x: x[2])
    pairs = pairs[::-1]
    pairs_df.to_csv(file_location+"\\final_results.csv")
    return pairs
    
def test_comparison(ticker1,ticker2):
    print(len(str(ticker1)))
    a=len(ticker1)+len(ticker2)
    return a

def return_ticker_file(ticker):
    DIR=file_location+"\\ticker_breakdown\\"+ticker+".csv"
    try: 
        
        ticker_file=pd.read_csv(DIR,header=None)
        ticker_file.columns=["date","price"]
    except FileNotFoundError:
        print("Ticker not found:"+ticker)
    #print(industry_file)
    return ticker_file

def up_down_comparison(ticker1,ticker2):
    t1_data=return_ticker_file(ticker1)
    t2_data=return_ticker_file(ticker2)
    t1_up_down=[]
    t2_up_down=[]
    same=[]
    if (len(t1_data)==len(t2_data)):
        
        for i in range(len(t1_data)-1):
           
            if (t1_data.iloc[i+1][1]>t1_data.iloc[i][1]):
                t1_up_down.append(1)
            elif (t1_data.iloc[i+1][1]==t1_data.iloc[i][1]):
                t1_up_down.append(0)
            else:
                t1_up_down.append(-1)
            
            if (t2_data.iloc[i+1][1]>t2_data.iloc[i][1]):
                t2_up_down.append(1)
            elif (t2_data.iloc[i+1][1]==t2_data.iloc[i][1]):
                t2_up_down.append(0)
            else:
                t2_up_down.append(-1)
            
    else:
        print("Failed")
        return -1
    
    score=0
    #print(len(t1_up_down))
    #print(len(t2_up_down))
    for i in range(len(t1_up_down)):
        
        if (t1_up_down[i]==t2_up_down[i]):
            score=score+1
    final_score=score/len(t1_up_down)
    return final_score
            
    
    
        
def generate_pairs(tickers):
    pairs=[]
    for pair in itertools.combinations(tickers,2):
        pairs.append([pair[0],pair[1]])
    #print(len(pairs))
    return pairs
        
    
__main__()