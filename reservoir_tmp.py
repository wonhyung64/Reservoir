#%%
import numpy as np
import pandas as pd
import openpyxl as xl
import os

#%%
os.chdir("E:\Data\무수저수지")
print("Current Working Directory: ", os.getcwd())


#%%

data_tmp = pd.read_excel("강수량_일자료_임실군(용암리)_20210712144100.xls")
data_tmp = data_tmp.iloc[:7763,:]

data1 = pd.DataFrame()
data1['관측일'] = pd.to_datetime(data_tmp['관측일'])
data1['금년일강수량'] = pd.to_numeric(data_tmp['금년일강수량'])
data1['지역'] = '임실군'
data1['관측소'] = '임실군(용암리)'
data1 = data1[['지역','관측소','관측일','금년일강수량']]



#%%
data2 = pd.DataFrame()
data2['관측일'] = pd.to_datetime(data_tmp['관측일'])
data2['저수율'] = np.tanh(np.random.normal(0,1,data1.shape[0])) * 0.25 + 0.6
data2['지역'] = '임실군'
data2['저수지'] = '두곡저수지'
data2 = data2[['지역','저수지','관측일','저수율']]


#%%
data_tmp = pd.read_excel("평창군_강수량_1999_2020.xls")
data_tmp = data_tmp.loc[data_tmp['관측일'] >= '1999-10-01',]
data_tmp = data_tmp.reset_index(drop=True)
data_tmp = data_tmp.iloc[:7747,:]

data3 = pd.DataFrame()
data3['관측일'] = pd.to_datetime(data_tmp['관측일'])
data3['금년일강수량'] = pd.to_numeric(data_tmp['금년일강수량'])
data3['지역'] = '평창군'
data3['관측소'] = '평창군(상진부리)'
data3 = data3[['지역','관측소','관측일','금년일강수량']]


#%%
data4 = pd.DataFrame()
data4['관측일'] = pd.to_datetime(data_tmp['관측일'])
data4['저수율'] = np.tanh(np.random.normal(0,1,data4.shape[0])) * 0.25 + 0.6
data4['지역'] = '평창군'
data4['저수지'] = '생곡저수지'
data4 = data4[['지역','저수지','관측일','저수율']]

# %%
data_tmp = pd.read_excel("진천_강수량_1999-2020.xls")
data_tmp = data_tmp.iloc[:7676,:]

data5 = pd.DataFrame()
data5['관측일'] = pd.to_datetime(data_tmp['관측일'])
data5['금년일강수량'] = pd.to_numeric(data_tmp['금년일강수량'])
data5['지역'] = '진천군'
data5['관측소'] = '진천군(진천여중))'
data5 = data5[['지역','관측소','관측일','금년일강수량']]

#%%
data_tmp = {'지역' : ['진천군','평창군','임실군'],
            '저수지': ['무수저수지','생곡저수지','두곡저수지'],
            '위도': [36.98154, 37.68076, 35.63822],
            '경도': [127.42919, 128.23646, 127.22687]}
data6 = pd.DataFrame(data_tmp)
#%%
data_tmp = {'지역' : ['진천군','평창군','임실군'],
            '관측소': ['진천군(진천여중)','평창군(상진부리)','임실군(용암리)'],
            '위도': [36.8692, 37.6589, 35.6406],
            '경도': [127.4561, 128.5781, 127.2072]}
data7 = pd.DataFrame(data_tmp)
# %%
os.chdir("E:\Data\무수저수지\shiny_data")
print("Current Working Directorty : ", os.getcwd())

data1.to_csv("임실_임실군(용암리)_강수량.csv", index=False, encoding='utf-8-sig')
data2.to_csv("임실군_두곡저수지_저수율.csv", index=False, encoding='utf_8-sig')
data3.to_csv("평창군_평창군(상진부리)_강수량.csv", index=False, encoding='utf-8-sig')
data4.to_csv("평창군_생곡저수지_저수율.csv", encoding='utf_8-sig')
data5.to_csv("진천군_진천군(진천여중)_강수량.csv", index=False, encoding='utf-8-sig')
data6.to_csv("저수지_위치.csv", index=False, encoding='utf-8-sig')
data7.to_csv("관측소_위치.csv", index=False, encoding='utf-8-sig')

#%%