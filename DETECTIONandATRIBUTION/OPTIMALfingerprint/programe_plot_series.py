# -*- coding: utf-8 -*-
"""
Created on Sat May 20 13:31:08 2023

@author: DELL
"""

'''本程序   用于
   区域季节性SIE的时间序列图1905-2014绘制
'''
'导入包，整理CTL,ALL文件夹'
import os
import numpy as np
import scipy.stats as stats
from labeltools import get_obsdata,juping,ctlaverage,moving_average
import netCDF4 as nc
import matplotlib.pyplot as plt
import statsmodels.api as sm
path_CTL = 'H:/search2/pre-indus-contro/'
FilesCTL =sorted(os.listdir(path_CTL))
path_ALL = 'H:/search2/pre_all/'
FilesALL =sorted(os.listdir(path_ALL))
'函数工具:获取区域SIE值'
def SIE(path,filename,direction):
    nf = nc.Dataset(path+filename,'r')
    aice = nf.variables['aice'][:].data
    tarea = nf.variables['tarea'][:].data
    aice[np.where(aice == 10.**30)]=np.nan
    aice[np.where(aice<=0.15)]=np.nan
    tarea[np.where(tarea==10.**30)]=np.nan
    seaice_area=np.empty([len(aice)],dtype=float)
    for time in range(0,len(aice)):
        if direction == 'Amundsen_Bellingshausen':
            seaice_area[time] = np.nansum(aice[time][0:37,257:294]*tarea[0:37,257:294]/10**12)
        elif direction == 'Ross_Amundsen':
            seaice_area[time] = np.nansum(aice[time][0:37,180:257]*tarea[0:37,180:257]/10**12)            
        elif direction == 'East_Antarctica':
            seaice_area[time] = np.nansum(aice[time][0:37,99:180]*tarea[0:37,99:180]/10**12)
        elif direction == 'King_Hakon':
            seaice_area[time] = np.nansum(aice[time][0:37,23:99]*tarea[0:37,23:99]/10**12)
        elif direction == 'Weddell':
            Weddell_sic    = np.hstack((aice[time][0:37,0:23],aice[time][0:37,294:]))
            Weddell_tarea  = np.hstack((tarea[0:37,0:23],tarea[0:37,294:]))
            Weddell_sic[np.where(Weddell_sic>1)] = 0
            seaice_area[time] = np.nansum(Weddell_sic*Weddell_tarea/10**12)
    return seaice_area
'函数工具:获取季节SIE值'
def seasondata(monthlydata,YEAR,season):
    '对于2000年的CTL而言，YEAR=1999，在FOR循环中又只取到了1998'
    sie = []
    for k in range(0,YEAR):
        if season=='DJF':
            ini_12 = k*12+11 
        elif season=='JJA':
            ini_12 = k*12+17
        sie.append(np.mean(monthlydata[ini_12:ini_12+3]))
    return sie
'数据处理主程序'
print('请依次输入地区,季节')
direction = input()
season    = input()
monthSIEctl=[]
for ctl_file in FilesCTL:
    sie_monthly = SIE(path_CTL,ctl_file,direction)
    monthSIEctl.extend(sie_monthly)
ctl = seasondata(monthSIEctl,1999,season)  
print('CTL finished')
ALL = np.zeros((164))
for mem in range(0,50):
    ALL_tmp =[]
    ini = int(17*mem)
    end = int(17*mem+17)
    for all_file in FilesALL[ini:end]:
        all_anu = SIE(path_ALL,all_file,direction) 
        ALL_tmp.extend(all_anu)
    ALLtmp = seasondata(ALL_tmp,164,season)
    plt.plot(ALLtmp,'grey')
    ALL = np.array(ALLtmp)+ALL
    
ALL = ALL / 50.      
ALL = ALL[54:] 
print('ALL finished')
reconfile = direction+'_best_fit_recons_'+season+'.nc'
obs = get_obsdata(reconfile) 
'画图处理主程序'
t = np.arange(1905,2015)

yobs0 = juping(obs[:55])
yall0 = juping(ALL[:55])
yobs1 = juping(obs[55:])
yall1 = juping(ALL[55:])
yobs = np.append(yobs0,yobs1)
yall = np.append(yall0,yall1)
yctl = ctlaverage(ctl,110)
yctlano = juping(yctl)
print('请输入地区和季节对应的数字代号0-19')
DataFrameStructureNum = int(input())
from get_cesm2 import x_ghg
x  = x_ghg[DataFrameStructureNum][54:]
y0 = juping(x[:55])
y1 = juping(x[55:])
ysingle = np.append(y0,y1)
#%%
plt.figure(figsize=(9,4))
ytxt1 = max(yobs)-0.01
ytxt2 = ytxt1*0.8
R, P = stats.pearsonr(yobs0,yall0)
R = round(R,3)
P = round(P,5)
plt.text(1905,ytxt1,'r='+str(R),color='royalblue',fontsize=12)
plt.text(1920,ytxt1,'p='+str(P),color='royalblue',fontsize=12)
R, P = stats.pearsonr(yobs1,yall1)
R = round(R,3)
P = round(P,5)
plt.text(1905,ytxt2,'r='+str(R),color='steelblue',fontsize=12)
plt.text(1920,ytxt2,'p='+str(P),color='steelblue',fontsize=12)
plt.title(direction+'-'+season,loc='right',fontsize=12)
plt.plot(t,yobs,'crimson',label='Reconstruction')
plt.plot(t,yall,'steelblue',label='ALL')
#plt.plot(t,ysingle,'grey',label='GHG')
plt.plot(t,yctlano,'black',label='CTL',linestyle='dashed',linewidth = 0.8)
plt.axvline(1960,linestyle='dashed',color='lightgrey')
plt.xticks([i for i in range(1905,2015,10)],rotation = 45)
plt.legend(loc='upper right')
plt.ylabel('SIE anomaly'+'$(10^6km^2)$',labelpad=-72,y=1.02,rotation=0,fontsize=12)
plt.xlabel('Year',labelpad=-20,x=0.95,fontsize=12)
plt.savefig('H:/search2/Notes/时间序列图/'+direction+'-'+season+'.jpg',dpi=300)
#%%
from ROF_main import da
beta = da(yall1,yobs1,50,juping(ctl),
          reg='TLS',cons_test='AS03',formule_ic_tls='AS03',
          sample_extr='regular')
ball_low,ball,ball_high = beta[0],beta[1],beta[2]
beta = da(y1,yobs1,20,juping(ctl),
          reg='OLS',cons_test='OLS_AT99',formule_ic_tls='',
          sample_extr='segment')
bghg_low,bghg,bghg_high = beta[0],beta[1],beta[2]
#%%
'一元回归趋势及不确定性'
def trendplot(tlist,datalist,namelist,direction,season):
    i=0
    plt.figure(figsize=(10,5))
    for data in datalist:
        data = moving_average(data, 11)
        x = sm.add_constant(tlist[i])
        model  = sm.OLS(data,x)
        result = model.fit()
        k = result.conf_int()
        k_low = k[1][0]*10
        k_high= k[1][1]*10
        k0 = result.params
        k0 = k0[1]*10
        if k0>=0:
            col = 'pink'
        else:
            col = 'darkgrey'
        plt.bar(namelist[i],k0,color= col)
        plt.vlines(namelist[i],k_low,k_high,'darkgreen')
        i=i+1
    plt.xticks(namelist,fontsize=12)
    plt.title(direction+'-'+season,loc='right',fontsize=12)
    plt.ylabel('SIE anomaly trend'+'$(10^6km^2/10yr)$',labelpad=-100,y=1.02,rotation=0,fontsize=12)
    plt.savefig('H:/search2/Notes/趋势图/'+direction+'-'+season+'.jpg',dpi=300)
trendplot([t,t[:55],t[55:],t,t[:55],t[55:],t,t[:55],t[55:]], 
          [yobs,yobs0,yobs1,yall,yall0,yall1,ysingle,y0,y1], 
          ['Recon','R0560','R6014','ALL','A0560','A6014','GHG','G0560','G6014']
          , direction, season)