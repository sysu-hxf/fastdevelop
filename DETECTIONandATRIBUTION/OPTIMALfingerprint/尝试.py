# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 23:07:41 2023

@author: DELL
"""

import os
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from labeltools import get_recdata
from ROF_main import da
path_ALL = 'H:/search2/canada/hist/'
FilesALL =sorted(os.listdir(path_ALL))
path_NAT = 'H:/search2/canada/nat/'
FilesNAT =sorted(os.listdir(path_NAT))
path_pic = 'H:/search2/canada/pic/'
FilesPIC =sorted(os.listdir(path_pic))
#%%
'''网格面积数组例程-----节省算力'''
file = path_ALL+FilesALL[0][:]
nf = nc.Dataset(file,'r')
lat_bnd = nf.variables['lat_bnds'][:].data
lon_bnd = nf.variables['lon_bnds'][:].data
lon = nf.variables['lon'][:].data
from math import radians, sin
def get_gridarea(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    r = 6372
    return abs(r**2 * (lon2 - lon1) * (sin(lat2) - sin(lat1)))/10**6
area = np.zeros((11,128))
for i in range(0,11):
    for j in range(0,128):
           lat1,lat2 = lat_bnd[i,0],lat_bnd[i,1]
           lon1,lon2 = lon_bnd[j,0],lon_bnd[j,1]
           area[i][j] = get_gridarea(lon1, lat1, lon2, lat2)
#%%
def SIE(path,filename,direction):
    nf = nc.Dataset(path+filename,'r')
    sic = nf.variables['sic'][:].data
    sic = sic/100
    sic[np.where(sic == 0)]=np.nan
    sic[np.where(sic<0.15)]=np.nan
    seaice_area=np.empty([len(sic)],dtype=float)
    for time in range(0,len(sic)):
        if direction == 'antarctic':
            seaice_area[time] = np.nansum(sic[time][0:11,:]*area[:,:])
        elif direction == 'Amundsen_Bellingshausen':
            seaice_area[time] = np.nansum(sic[time][0:11,89:104]*area[:,89:104])
        elif direction == 'Weddell':
            seaice_area[time] = np.nansum(sic[time][0:11,103:124]*area[:,103:124])
        elif direction == 'Ross_Amundsen':
            seaice_area[time] = np.nansum(sic[time][0:11,58:90]*area[:,58:90])
        elif direction == 'East_Antarctica':
            seaice_area[time] = np.nansum(sic[time][0:11,25:58]*area[:,25:58])
        elif direction == 'King_Hakon':
            tmp_sic    = np.hstack((sic[time][0:11,0:26],sic[time][0:11,123:]))
            tmp_area  = np.hstack((area[:,0:26],area[:,123:]))
            seaice_area[time] = np.nansum(tmp_sic*tmp_area)
    return seaice_area

def seasondata(monthlydata,YEAR,season):
    sie = []
    for k in range(0,YEAR):
        if season=='year':
            ini_12 = k*12
            sie.append(np.mean(monthlydata[ini_12:ini_12+12]))
        elif season=='DJF':
            ini_12 = k*12+11 
            sie.append(np.mean(monthlydata[ini_12:ini_12+3]))
        elif season=='Feb':
            ini_12 = k*12+11 
            sie.append(monthlydata[ini_12+2])
    return sie
#%%
print('zone:')
zone = input()
print('season')
season = input()
sie_all = []
for file in FilesALL:
    sie_all.append(seasondata(SIE(path_ALL,file,zone),155, season)) 
sie_nat = []
for file in FilesNAT:
    sie_nat.append(seasondata(SIE(path_NAT,file,zone),155, season))  
ALL = np.average([sie_all[i] for i in range(0,5)], axis=0).tolist()
NAT = np.average([sie_nat[i] for i in range(0,5)], axis=0).tolist()   

sie_pic = []
sie_pic.extend(seasondata(SIE(path_pic,FilesPIC[0][:],zone), 295, season))
for file in FilesPIC[1:]:
    sie_pic.extend(seasondata(SIE(path_pic,file,zone),99, season))
#%%   
if zone == 'antarctic':
    zone = 'Total'
else:
    zone = zone
if season == 'DJF':
    fileRecon = zone+'_best_fit_recons_DJF.nc'
    RECON = get_recdata(fileRecon)             # get_obsdata 得到重构数据1905-2014
    RECON = RECON[55:101]                        
    ALL   = ALL[109:]
    NAT   = NAT[109:]
else:
    print("当前非DJF季度，无法调取RECON")
#%%
'1971-2000气候态'
climatebaseALL =np.mean( ALL[11:41])
climatebaseNAT =np.mean(NAT[11:41])
climatebaseREC =np.mean( RECON[11:41])

ERROR = climatebaseALL - climatebaseREC

ALLadjust = [I - ERROR for I in ALL]
NATadjust = [I - ERROR for I in NAT]

plt.figure(figsize=(4,4))
std_all = np.std(ALL)
std_rec = np.std(RECON)
std_nat = np.std(NAT)
t = np.arange(1960,2006)
plt.fill_between(t, ALL-1.64*std_all,  ALL+1.64*std_all, facecolor = 'lightblue',alpha=0.6)
plt.fill_between(t, NAT-1.64*std_nat,  NAT+1.64*std_nat, facecolor = 'lightgreen',alpha=0.7)
plt.fill_between(t, RECON-1.64*std_rec  ,  RECON+1.64*std_rec  , facecolor = 'lightgrey',alpha=0.4)
plt.plot(t,ALL,'steelblue',label='ALL')
plt.plot(t,NAT,'green' ,label='NAT')
plt.plot(t,RECON,'grey' ,label='Reconstruction')

plt.plot(t,ALLadjust,'blue',linestyle='dashed')
plt.plot(t,NATadjust,'lime',linestyle='dashed')
plt.legend()
plt.ylabel('SIE'+'$(10^6km^2)$',labelpad=-62,y=1.02,rotation=0,fontsize=12)
plt.xticks([i for i in range(t[0],t[-1]+1,5)],rotation = 45)
plt.savefig('H:/search2/Notes/canesm2'+zone+season+'.jpg',dpi=300)
#%%

