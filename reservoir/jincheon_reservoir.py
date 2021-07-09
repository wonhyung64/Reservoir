#%%
import numpy as np
import pandas as pd
import openpyxl as xl
from matplotlib import pyplot as plt
import os

#%% 
os.chdir("E:\Data\무수저수지")
print("Current Working Directory ", os.getcwd())
# %%
data = pd.read_excel("무수저수지 데이터셋.xlsx", header=0)
data.head()
# %%
