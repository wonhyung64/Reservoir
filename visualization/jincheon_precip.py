#%% MODULE IMPORT
from re import I
import numpy as np
import pandas as pd
import os
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

plt.rcParams['figure.figsize'] = [10,6]


# %%
os.chdir("E:\Data\무수저수지")
print("Current Working Directory ", os.getcwd())


#%%
data = pd.read_excel("강수량_일자료_진천군(진천여중)_20210603145204.xls")
data = data.iloc[:2661,:2]
precip = pd.DataFrame()
precip['date'] = pd.to_datetime(data['관측일'])
precip['precipitation'] = data['금년일강수량'].astype(int)
#precip.info()


#%%
precip13 = precip.loc[precip['date'].dt.year==2013,]
precip14 = precip.loc[precip['date'].dt.year==2014,]
precip15 = precip.loc[precip['date'].dt.year==2015,]
precip16 = precip.loc[precip['date'].dt.year==2016,]
precip17 = precip.loc[precip['date'].dt.year==2017,]
precip18 = precip.loc[precip['date'].dt.year==2018,]
precip19 = precip.loc[precip['date'].dt.year==2019,]
precip20 = precip.loc[precip['date'].dt.year==2020,]
precip_list = [precip13,precip14,precip15,precip16,precip17,precip18,precip19,precip20]


#%%
def precip_grouped(data,precip='precipitation',date='date'):
    df = pd.DataFrame({'precip':data[precip],
                    'month':data[date].dt.month,
                    'day':data[date].dt.day})
    df = df.set_index(['month','day'])
    grouped = df.groupby(by ='month')
    return grouped
    #grouped.boxplot(subplots=False, vert=False,)


# %%
group13 = precip_grouped(precip13)
group14 = precip_grouped(precip14)
group15 = precip_grouped(precip15)
group16 = precip_grouped(precip16)
group17 = precip_grouped(precip17)
group18 = precip_grouped(precip18)
group19 = precip_grouped(precip19)
group20 = precip_grouped(precip20)

group_list = [group13,group14,group15,group16,group17,group18,group19,group20]


# %% PRECIPITATION BOXPLOT
year = [2013,2014,2015,2016,2017,2018,2019,2019,2020]
n = 1
for i in precip_list:
    jan = i.loc[i['date'].dt.month == 1,'precipitation']
    feb = i.loc[i['date'].dt.month == 2,'precipitation']
    mar = i.loc[i['date'].dt.month == 3,'precipitation']
    apr = i.loc[i['date'].dt.month == 4,'precipitation']
    may = i.loc[i['date'].dt.month == 5,'precipitation']
    jun = i.loc[i['date'].dt.month == 6,'precipitation']
    jul = i.loc[i['date'].dt.month == 7,'precipitation']
    aug = i.loc[i['date'].dt.month == 8,'precipitation']
    sep = i.loc[i['date'].dt.month == 9,'precipitation']
    oct = i.loc[i['date'].dt.month == 10,'precipitation']
    nov = i.loc[i['date'].dt.month == 11,'precipitation']
    dec = i.loc[i['date'].dt.month == 12,'precipitation']
    month = [jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec]

    fig1, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,4))
    ax.boxplot(month)
    ax.set_xticklabels(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])
   
    plt.xlabel(str(year[n-1]))
    n += 1


# %% MAX_PRECIPITATION LINE GRAPH
year = 2013
for i in group_list:
    label_tmp = 'line' + str(year)
    plt.plot(i.max().index, i.max()['precip'], label = label_tmp)
    plt.legend()
    year += 1
plt.title("MAX")
plt.xlabel("month")
plt.ylabel("precipitation")
plt.show()


# %% TOTAL_PRECIPITATION LINE GRAPH
year = 2013
for i in group_list:
    label_tmp = 'line' + str(year)
    plt.plot(i.sum().index, i.sum()['precip'], label = label_tmp)
    plt.legend()
    year += 1
plt.title("TOTAL")
plt.xlabel("month")
plt.ylabel("precipitation")
plt.show()


# %% AVERAGE_PRECIPITATION LINE GRAPH
year = 2013
for i in group_list:
    label_tmp = 'line' + str(year)
    plt.plot(i.mean().index, i.mean()['precip'], label = label_tmp)
    plt.legend()
    year += 1
plt.title("AVERAGE")
plt.show()


#%% MEDIAN_PRECIPITATION LINE GRAPH 쓸모없음..
year = 2013
for i in group_list:
    label_tmp = 'line' + str(year)
    plt.plot(i.median().index, i.median()['precip'], label = label_tmp)
    plt.legend()
    year += 1
plt.title("MEDIAN")
plt.xlabel("month")
plt.ylabel("precipitation")
plt.show()


# %%
year = [2013,2014,2015,2016,2017,2018,2019,2019,2020]
n = 1
for i in precip_list:
    plt.subplot(2,4,n)
    plt.bar(i.index, i['precipitation'], width=1.5)
    plt.xlabel(str(year[n-1]))
    plt.yticks(np.arange(0,160,20))
    n += 1
plt.show()


# %%
