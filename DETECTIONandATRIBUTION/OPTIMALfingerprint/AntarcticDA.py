# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 23:07:41 2023

@author: DELL
"""

import os
import numpy as np
from labeltools import get_recdata,ctlaverage,draw_series,get_obsdata
import netCDF4 as nc
import matplotlib.pyplot as plt
from satellite import sateDJF    # sateDJF为南极DJF观测SIE1905-2014
from ROF_main import da
path_CTL = 'H:/search2/pre-indus-contro/'
FilesCTL =sorted(os.listdir(path_CTL))

path_ALL = 'H:/search2/pre_all/'
FilesALL =sorted(os.listdir(path_ALL))


# 读取60°S以南海冰SIC数据，T-area;计算各月SIE 
#  return:  全南极或扇区的DJF序列（检测归因）或2月序列（事件归因）
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
        elif direction == 'Antarctic':
            seaice_area[time] = np.nansum(aice[time][0:37,:]*tarea[0:37,:]/10**12)
    return seaice_area
'函数工具:获取季节SIE值'
def seasondata(monthlydata,YEAR,season):
    '对于2000年的CTL而言，YEAR=1999，在FOR循环中又只取到了1998'
    sie = []
    for k in range(0,YEAR):
        if season=='DJF':
            ini_12 = k*12+11 
            sie.append(np.mean(monthlydata[ini_12:ini_12+3]))
        elif season=='Feb':
            ini_12 = k*12+13
            sie.append(monthlydata[ini_12])
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
    ALL = np.array(ALLtmp)+ALL              
ALL = ALL[54:]/50                          # 1905-2014 
#%%
print("***choose y/n to D&A(y) or Extent(n)***")
CONDITION =str( input())
if CONDITION == 'y':
    if direction == 'Antarctic':
        zone = 'Total'
    else:
        zone = direction
    fileRecon = zone+'_best_fit_recons_DJF.nc'
    RECON = get_recdata(fileRecon)             # get_obsdata 得到重构数据1905-2014
    OBS   = get_obsdata(fileRecon)             # 得到对应的真实观测  size = 116
    OBS[np.where(OBS<=0)]=np.nan
    print("*****INPUT time scale(such as 1950,2005)****")
    stt,ter = int(input())-1905,int(input())-1905
    xall,xrecon = ALL[stt:ter],RECON[stt:ter]
    climatebaseALL = np.mean(ALL[76:106])
    climatebaseREC = np.mean(RECON[76:106])
    error = climatebaseALL - climatebaseREC
    print('CESM2-ALL气候态与重构气候态之差 ： '+str(error))
    print('请考虑是否需要校准')
    ANOMALall = [x-climatebaseALL for x in xall]
    ANOMALrec = [x-climatebaseREC for x in xrecon]
    CTL = ctl  - np.mean(ctl)
    beta = da(ANOMALrec,ANOMALall,50,CTL,reg='TLS',cons_test='AS03',
              formule_ic_tls='AS03',sample_extr='regular')

ctl_110 = ctlaverage(ctl, 110)
plt.figure(figsize=(4,4))
draw_series(np.arange(1905,2015), ALL, 
RECON,ctl_110,OBS,'ALL','Reconstuction','PIC','OBS',10,'CESM2 '+direction+'-'+season)
#plt.savefig('H:/search2/Notes/'+direction+season,dpi=300)

import scipy.stats as stats
plt.figure(figsize=(6,4))
'图例位置设定'
ytxt1 = max(ANOMALrec)-0.02
ytxt2 = 0.85*ytxt1
R, P = stats.pearsonr(ANOMALrec[:55],ANOMALall[:55])
R = round(R,3)
P = round(P,5)
plt.text(1905,ytxt1,'r='+str(R),color='crimson',fontsize=16)
plt.text(1905,ytxt2,'p='+str(P),color='r',fontsize=16)
R, P = stats.pearsonr(ANOMALrec[55:],ANOMALall[55:])
R = round(R,3)
P = round(P,5)
plt.text(1985,ytxt1,'r='+str(R),color='crimson',fontsize=16)
plt.text(1985,ytxt2,'p='+str(P),color='r',fontsize=16)

plt.plot(np.arange(1905,2015),ANOMALrec,'seagreen',label='Reconstruction')
plt.plot(np.arange(1905,2015),ANOMALall,'steelblue',label='ALL')
plt.axvline(1960,linestyle='dashed',color='grey')
plt.xticks([i for i in range(1905,2015,10)],rotation = 45)
plt.legend(loc='lower left')
plt.ylabel('SIE anomaly'+'$(10^6km^2)$',labelpad=-72,y=1.02,rotation=0,fontsize=12)
#plt.savefig('H:/search2/Notes/时间序列图/'+direction+'-'+season+'.jpg',dpi=300)

#%%
plt.figure(figsize = (4,4))
betamin,betamax = 0.568393,1.63344
betabest = 1.09485
plt.scatter(0.3,betabest,s=15,c='royalblue',marker='o')
plt.scatter(0.3,betamin,s=30,c='royalblue',marker='_')
plt.scatter(0.3,betamax,s=30,c='royalblue',marker='_')
plt.vlines(0.3,betamin,betamax,colors='royalblue')

betamin,betamax = 0.863642,3.26435
betabest = 2.0105
plt.scatter(0.6,betabest,s=15,c='royalblue',marker='o')
plt.scatter(0.6,betamin,s=30,c='royalblue',marker='_')
plt.scatter(0.6,betamax,s=30,c='royalblue',marker='_')
plt.vlines(0.6,betamin,betamax,colors='royalblue')

plt.xlim(0,0.9)
plt.ylim(-1,4)
plt.xticks([0.3,0.6],['1905-2014','1960-2014'])
plt.axhline(0,linestyle='dashed',color='grey')
plt.axhline(1,linestyle='dashed',color='grey')
plt.ylabel('Scaling factors',fontsize=12,labelpad=-72,y=1.02,rotation=0)
plt.text(0.1,3.5,'ALL',color='royalblue',fontsize=16)
#plt.savefig('H:/search2/Notes/Amunda.jpg',dpi=300) 
#%%
from get_cesm2 import x_ghg
#%%
'AmundsenBellingshausen DJF GHG'
xghg = x_ghg[0][54:]
print("*****INPUT time scale(such as 1950,2005)****")
stt,ter = int(input())-1905,int(input())-1905

xi,xrecon = xghg[stt:ter],RECON[stt:ter]
climatebaseGHG = np.mean(xghg[76:106])
error = climatebaseGHG - climatebaseREC
print('CESM2-GHG单因子强迫与重构气候态之差： '+str(error))
ANOMALghg = [x-climatebaseGHG for x in xi]
ANOMALrec = [x-climatebaseREC for x in xrecon]
beta = da(ANOMALrec,ANOMALghg,15,CTL,reg='TLS',cons_test='AS03',
          formule_ic_tls='AS03',sample_extr='regular')

#%%
plt.figure(figsize = (4,4))
betamin,betamax = 0.568393,1.63344
betabest = 1.09485
plt.scatter(0.25,betabest,s=15,c='royalblue',marker='o')
plt.scatter(0.25,betamin,s=30,c='royalblue',marker='_')
plt.scatter(0.25,betamax,s=30,c='royalblue',marker='_')
plt.vlines(0.25,betamin,betamax,colors='royalblue')

betamin,betamax = 0.255957,1.00628
betabest = 0.6254
plt.scatter(0.35,betabest,s=15,c='seagreen',marker='o')
plt.scatter(0.35,betamin,s=30,c='seagreen',marker='_')
plt.scatter(0.35,betamax,s=30,c='seagreen',marker='_')
plt.vlines(0.35,betamin,betamax,colors='seagreen')

betamin,betamax = 0.863642,3.26435
betabest = 2.0105
plt.scatter(0.65,betabest,s=15,c='royalblue',marker='o')
plt.scatter(0.65,betamin,s=30,c='royalblue',marker='_')
plt.scatter(0.65,betamax,s=30,c='royalblue',marker='_')
plt.vlines(0.65,betamin,betamax,colors='royalblue')

betamin,betamax = 0.830056,2.03936
betabest = 1.40453
plt.scatter(0.75,betabest,s=15,c='seagreen',marker='o')
plt.scatter(0.75,betamin,s=30,c='seagreen',marker='_')
plt.scatter(0.75,betamax,s=30,c='seagreen',marker='_')
plt.vlines(0.75,betamin,betamax,colors='seagreen')

plt.xlim(0,0.9)
plt.ylim(-1,4)
plt.xticks([0.3,0.7],['1905-2014','1960-2014'])
plt.axhline(0,linestyle='dashed',color='grey')
plt.axhline(1,linestyle='dashed',color='grey')
plt.ylabel('Scaling factors',fontsize=12,labelpad=-72,y=1.02,rotation=0)
plt.text(0.05,3.5,'ALL',color='royalblue',fontsize=13)
plt.text(0.05,3,'GHG',color='seagreen',fontsize=13)
#plt.savefig('H:/search2/Notes/Amundaplus.jpg',dpi=300) 