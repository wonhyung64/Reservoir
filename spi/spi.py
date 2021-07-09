#%%
import pandas as pd
import openpyxl as xl
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime as dt
from scipy.stats import gamma
from scipy.stats import norm


#%%
os.chdir("E:\Data\무수저수지")
print("Current Working Directory ", os.getcwd())

data = pd.read_excel("강수량_1999-2020.xls")

data = data.iloc[:7676,:2]

data['cum_30'] = data['금년일강수량'].rolling(30).sum()
data['cum_60'] = data['금년일강수량'].rolling(60).sum()
data['cum_90'] = data['금년일강수량'].rolling(90).sum()
data['cum_120'] = data['금년일강수량'].rolling(120).sum()
data['cum_150'] = data['금년일강수량'].rolling(150).sum()

list_tmp = ['cum_30','cum_60','cum_90','cum_120','cum_150']

data = data.loc[data['관측일'] >='2000-01-01',]
data['관측일'] = pd.to_datetime(data['관측일'])

#plt.hist(data['cum_90'])


#%% SPI FUCTION
def cal_spi(x):
    return norm.ppf(gamma.cdf(x, a = a_hat, scale=b_hat))


#%% SPI CALCULATE
for i in range(len(list_tmp)):
    a_hat = 0.5/ (np.log(data[list_tmp[i]].mean()) - np.mean(np.log(data[list_tmp[i]]+0.00001)))
    b_hat = data[list_tmp[i]].mean()/a_hat
    newcol = 'SPI'+str(i+1)
    data[newcol] = data[list_tmp[i]].map(lambda x: cal_spi(x))


#%%
data = data.loc[data['관측일'] >= '2020-01-01',]

plt.plot(data['관측일'],data['SPI1'], color='#1f77b4', label='SPI1')
plt.plot(data['관측일'],data['SPI2'], color='#ff7f0e', label='SPI2')
plt.plot(data['관측일'],data['SPI3'], color='#2ca02c', label='SPI3')
plt.plot(data['관측일'],data['SPI4'], color='#d62728', label='SPI4')
plt.plot(data['관측일'],data['SPI5'], color='#9467bd', label='SPI5')

temp = pd.DataFrame()
temp['관측일'] = data['관측일']
temp['EW'] = 2
temp['VW'] = 1.5
temp['MW'] = 1
temp['MD'] = -1
temp['SD'] = -1.5
temp['ED'] = -2

plt.plot(temp['관측일'],temp['EW'], alpha=0.2, color = 'gray', linestyle='--')
plt.plot(temp['관측일'],temp['VW'], alpha=0.2, color = 'gray', linestyle='--')
plt.plot(temp['관측일'],temp['MW'], alpha=0.2, color = 'gray', linestyle='--')
plt.plot(temp['관측일'],temp['MD'], alpha=0.2, color = 'gray', linestyle='--')
plt.plot(temp['관측일'],temp['SD'], alpha=0.2, color = 'gray', linestyle='--')
plt.plot(temp['관측일'],temp['ED'], alpha=0.2, color = 'gray', linestyle='--')

plt.vlines(x=dt.datetime(2020,10,1), ymin=min(min(data.iloc[:,7:].min().to_list()),-2.5),
            ymax=max(max(data.iloc[:,7:].max().to_list()),2.5), colors='black', ls=':', lw=.5)

plt.title('2020 SPI')
plt.xlabel('month')
plt.ylabel('index')

plt.yticks(np.arange(-3,3.5,0.5), labels=['','-2.5','-2.0','-1.5','-1.0','-0.5','0.0','0.5','1.0','1.5','2.0','2.5',''])
plt.xticks(['2020-01','2020-02','2020-03','2020-04','2020-05','2020-06','2020-07','2020-08','2020-09','2020-10','2020-11','2020-12'],labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.legend()
plt.show()



# %%
