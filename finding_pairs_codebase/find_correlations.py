from typing import final
import pandas as pd                   
import numpy as np   
from statsmodels.tsa.stattools import coint


df = pd.read_csv('sectors_merged\Utilities_Merged.csv')
df['time_tick']=pd.to_datetime(df['time_tick'])

df = df.set_index(pd.DatetimeIndex(df['time_tick']))
corr_mat=df.corr(method ='pearson').apply(lambda x : x.abs())

sorted_corr = corr_mat.unstack().sort_values(kind="quicksort", ascending=False)
sc=pd.DataFrame(sorted_corr, columns=["Correlation"])[64:74]


sc = sc.iloc[1:]
finalvalues =[]

for position, index in enumerate(sc.index.values):
    if(position%2 == 0):
        _,value,_ = coint(df[index[0]],df[index[1]])
        finalvalues.append([index[0],index[1],float(value),sc.iat[position,0]])

finalvalues.sort()

for stocks in finalvalues:
    print(stocks)



