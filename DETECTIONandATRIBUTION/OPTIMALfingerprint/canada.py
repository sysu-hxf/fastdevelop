# -*- coding: utf-8 -*-
"""
Created on Wed May 24 20:44:11 2023

@author: DELL
"""

import os
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

path_ALL = 'H:/search2/canada/hist/'
FilesALL =sorted(os.listdir(path_ALL))
path_NAT = 'H:/search2/canada/nat/'
FilesNAT =sorted(os.listdir(path_NAT))
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
sie_all = []
print('zone:')
zone = input()
season = 'Feb'
for file in FilesALL:
    sie_all.append(seasondata(SIE(path_ALL,file,zone),155, season))
sie_nat = []
for file in FilesNAT:
    sie_nat.append(seasondata(SIE(path_NAT,file,zone),155, season))   
#%%
ALL = np.average([sie_all[i] for i in range(0,5)], axis=0).tolist()
NAT = np.average([sie_nat[i] for i in range(0,5)], axis=0).tolist()

import scipy.stats as st

def getkde(data,datax):
    scipy_kde = st.gaussian_kde(data)  # 高斯核密度估计
    datax.sort()
    dens = scipy_kde.evaluate(datax)
    data_integrate = []  # 存放所有点的累积概率
    data_integrate.append(0)
    point = 0  # 存放单个累积概率
    for i in range(1, len(datax)):
        point =  point+scipy_kde.integrate_box_1d(datax[i-1], datax[i])  
        data_integrate.append(point)    
    return dens,data_integrate

def FAR(pnat,pall):
    tmp = 1-(pnat/(pall+0.0000000001))
    if tmp>0:
        FAR = tmp
    else:
        FAR = 0
    return FAR




ALL = ALL[55:] #1906-2005
NAT = NAT[55:]
ini = [i-1905 for i in [1955,1965,1975,1985,1995]]
end = [i-1905 for i in [1965,1975,1985,1995,2005]]

print('事件y0')
#y0 = 1.79    #2023年2月的卫星观测
y0 = float(input())
for k in range(0,len(ini)):
    yall = ALL[ini[k]:end[k]]
    ynat = NAT[ini[k]:end[k]]

    datax = np.arange(0.5*min(min(min(yall),min(ynat)),y0),1.5*max(max(yall),max(ynat)),0.001)
    ALLden,ALLcdf = getkde(yall,datax)
    NATden,NATcdf = getkde(ynat,datax)

    plt.figure(figsize=(3,3))
    plt.xlabel('Absolute SIE'+'$(10^6km^2)$',labelpad=15,x=0.85,fontsize=10)
    plt.ylabel('Kernel Density',labelpad=-72,y=1.02,rotation=0,fontsize=12)
    plt.axvline(y0,color='gray',linewidth=2)
    plt.plot(datax,ALLden,label='ALL',c='blue')
    plt.plot(datax,NATden,label='NAT',c='green')
    plt.legend(loc='upper left') 
    plt.title(str(ini[k]+1905)+'-'+str(end[k]+1904),loc='right',fontsize=10)
    plt.savefig('H:/search2/Notes/事件图/'+zone+'-'+season+'_kde_'+str(k)+'.jpg',dpi=300)

plt.figure(figsize=(3,3))
ax = plt.gca()
ax.invert_xaxis()  #x轴反向
plt.axvline(y0,color='gray',linewidth=2)
colorlist = ['seagreen','crimson','royalblue','gold','black']
for k in range(0,len(ini)):
    yall = ALL[ini[k]:end[k]]
    ynat = NAT[ini[k]:end[k]]
    datax = np.arange(0.5*min(min(min(yall),min(ynat)),y0),1.2*max(max(yall),max(ynat)),0.001)
    ALLden,ALLcdf = getkde(yall,datax)
    NATden,NATcdf = getkde(ynat,datax)
    FARvalue = []
    for i in range(len(datax)):
        FARvalue.append(FAR(NATcdf[i],ALLcdf[i]))  

    plt.plot(datax[1:],FARvalue[1:],label=str(ini[k]+1905)+'-'+str(end[k]+1904)
           ,c = colorlist[k] )


plt.title(' F A R',loc='left',fontsize=12)
plt.legend(loc='lower right')  
plt.savefig('H:/search2/Notes/事件图/'+zone+'-'+season+'_FAR'+'.jpg',dpi=300)
