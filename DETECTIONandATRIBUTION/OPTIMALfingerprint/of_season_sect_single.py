# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 22:53:03 2023

@author: DELL
"""

import netCDF4 as nc
import numpy as np
import os
from get_cesm2 import get_SIE,get_section_SIE,get_season_mean,get_seasonal_SIE,output_sectional_seasonal_SIE
from labeltools import get_obsdata,juping,printbeta,recons_name
from ROF_main import da
path_CTL = 'H:/search2/pre-indus-contro/'

Files =sorted(os.listdir(path_CTL))
            
def SIE(path,Files,years):
    sie1,sie2,sie3,sie4,sie5=[],[],[],[],[]
    for file in Files:
        nf = nc.Dataset(path+file,'r')
        sic = nf.variables['aice'][:].data
        tarea = nf.variables['tarea'][:].data
        for i in range(0,len(sic)):
            s1,s2,s3,s4,s5 = get_section_SIE(tarea, sic[i])
            sie1.append(s1)
            sie2.append(s2)
            sie3.append(s3)
            sie4.append(s4)
            sie5.append(s5)
    a1,a2,a3,a4,a5 = get_seasonal_SIE(sie1, sie2, sie3, sie4, sie5,years)    
    amun1,amun2,amun3,amun4 = output_sectional_seasonal_SIE(a1, years)
    wed1,wed2,wed3,wed4 = output_sectional_seasonal_SIE(a2, years)
    king1,king2,king3,king4=output_sectional_seasonal_SIE(a3, years)
    ea1,ea2,ea3,ea4 = output_sectional_seasonal_SIE(a4, years)
    ross1,ross2,ross3,ross4=output_sectional_seasonal_SIE(a5, years)
    return amun1,amun2,amun3,amun4,wed1,wed2,wed3,wed4,king1,king2,king3,king4,ea1,ea2,ea3,ea4,ross1,ross2,ross3,ross4 

amun1,amun2,amun3,amun4,wed1,wed2,wed3,wed4,king1,king2,king3,king4,ea1,ea2,ea3,ea4,ross1,ross2,ross3,ross4 =SIE(path_CTL,Files,1999)

#%%
def printBETA(x,k,CTL,NUM,file1,file2,file3,file4):
#x = x_aaer / x_ghg / .....
#K=0/4/8/12/16 对应AMUN_BELL之外的 wed king ea ross
# CTL = [amun1,amun2,amun3,amun4]/......
# NUM = NUMS OF MEMBERS,FOR GHG NUM=15,FOR AAER NUM=20
# file1~4 重构数据文件名（不需要路径，但需要格式.nc）
    obs1 = get_obsdata(file1) 
    obs2 = get_obsdata(file2) 
    obs3 = get_obsdata(file3) 
    obs4 = get_obsdata(file4) 
    OBS=[obs1,obs2,obs3,obs4]
    beta = []
    for i in range(0,4):    
        x_x = x[i+k][54:]
        obs_0 = juping(OBS[i][:55])
        x_x_0 = juping(x_x[:55])
        obs_1 = juping(OBS[i][55:])
        x_x_1 = juping(x_x[55:])
        
        OBS[i] = juping(OBS[i])
        x_x    = juping(x_x)
        CTL[i] = juping(CTL[i])
        
        print("------1905-2014-------")
        BETA = da(OBS[i],x_x,NUM,CTL[i],
                  reg='OLS',cons_test='OLS_AT99',formule_ic_tls='',
                  sample_extr='segment')
        printbeta(BETA)
        beta.append(BETA)   
        
        print("------1905-1960-------")
        BETA = da(obs_0,x_x_0,NUM,CTL[i],
                  reg='OLS',cons_test='OLS_AT99',formule_ic_tls='',
                  sample_extr='segment')
        printbeta(BETA)
        beta.append(BETA) 
        print("------1960-2014-------")
        BETA = da(obs_1,x_x_1,NUM,CTL[i],
                  reg='OLS',cons_test='OLS_AT99',formule_ic_tls='',
                  sample_extr='segment')
        printbeta(BETA)  
        beta.append(BETA) 
    return beta
#%% 
##试验
from get_cesm2 import x_ghg
#%%      
obslist = recons_name(16,20)
file1,file2,file3,file4=obslist[0],obslist[1],obslist[2],obslist[3]
beta = printBETA(x_ghg,16,[ross1,ross2,ross3,ross4],15,
          file1,file2,file3,file4)
#%%

import matplotlib.pyplot as plt
from labeltools import beta_from_ofsss
from labeltools import colorscheme
B = beta_from_ofsss(beta)
Y_LIST = [yi for yi in B]
y = [1,2,3,6,7,8,11,12,13,16,17,18]
XMIN = [X[0] for X in Y_LIST]
XMAX = [X[2] for X in Y_LIST]
XDOT = [X[1] for X in Y_LIST]
plt.xlim(-3,2)
plt.hlines(y, XMIN, XMAX,colors=colorscheme)
plt.scatter(XDOT,y,c='black',s=17)
plt.axvline(0,linestyle='dashed',color='lightgrey')
plt.axvline(1,linestyle='dashed',color='lightgrey')
plt.xlabel('Scaling factors',fontsize=12)
plt.yticks(range(2,20,5), labels=['D J F','MAM','J J A','SON'])
plt.text(-2.8,18,'Ross–Amundsen',fontsize=10,color='grey')
plt.text(-2.8,17,'CESM2-GHG',fontsize=10,color='grey')
plt.savefig('H:/search2/Notes/photo/GHGross.jpg',dpi=300) 

