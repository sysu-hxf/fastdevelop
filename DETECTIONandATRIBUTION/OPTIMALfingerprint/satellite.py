# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 17:37:56 2022

@author: DELL
"""

import os 
import pandas as pd
import numpy as np

#构建1979年至今按照逐月遍历年份方式排列的合并数据集
path = 'H:/search2/sic_sie/data_SIE/'
files = os.listdir(path)
files.sort(key = lambda x:int(x[2:4]))
data_csv = list(files)
data_list = []
for fileitem in data_csv:
    tmp = pd.read_csv(path + fileitem,header=0)
    data_list.append(tmp)
    
dataset = pd.concat(data_list,ignore_index = True)
#提取出SIE和年份的obs数据集，-9999用nan代替
obs = np.array(dataset[[dataset.columns[0],dataset.columns[4]]])
obs[np.where(obs[:,1]==-9999),1]=np.nan
del path,files,data_csv,data_list,tmp,fileitem
#1-9月SIE切片
obs_d=[]
for i in range(0,396,44):
    #print(i) 
    obs_tmp = obs[i:i+44,1]
    #ave_tmp = np.nansum(obs_tmp)/float(len(obs_tmp[~np.isnan(obs_tmp)]))
    #obs_d.append(obs_tmp-ave_tmp)
    obs_d.append(obs_tmp)

#10-12月的切片
obs_tmp10 = obs[396:439,1]
obs_tmp11 = obs[439:483,1]
obs_tmp12 = obs[483:527,1]
#ave_tmp = np.nansum(obs_tmp10)/float(len(obs_tmp10[~np.isnan(obs_tmp10)]))
#obs_d.append(obs_tmp10-ave_tmp)
obs_d.append(obs_tmp10)
#ave_tmp = np.nansum(obs_tmp11)/float(len(obs_tmp11[~np.isnan(obs_tmp11)]))
#obs_d.append(obs_tmp11-ave_tmp)
obs_d.append(obs_tmp11)
#ave_tmp = np.nansum(obs_tmp12)/float(len(obs_tmp12[~np.isnan(obs_tmp12)]))
#obs_d.append(obs_tmp12-ave_tmp)
obs_d.append(obs_tmp12)

'1978年11月 ———— 2022年9月'
sie_timeseries = np.array([])
sie_timeseries = np.append(sie_timeseries,obs_d[10][0]) #添加1978年11月
sie_timeseries = np.append(sie_timeseries,obs_d[11][0]) #添加1978年12月
#   for循环添加1979年1月-2021年12月
for i in range(0,43):
    sie_timeseries = np.append(sie_timeseries,[obs_d[j][i] for j in range(0,10)])
    sie_timeseries = np.append(sie_timeseries,[obs_d[j][i+1] for j in range(10,12)])
#最后再添加2022年1月-9月
sie_timeseries = np.append(sie_timeseries,[obs_d[j][43] for j in range(0,9)])

del i
sateDJF = []
for k in  range(0,44):
    tmp1 = sie_timeseries[2+12*k]
    tmp2 = sie_timeseries[3+12*k]
    tmp12 = sie_timeseries[1+12*k]
    sateDJF.append((tmp1+tmp2+tmp12)/3)


# 2022年夏季（即2021年12月、2022年1月、2月的卫星观测平均SIE是5.08667）
