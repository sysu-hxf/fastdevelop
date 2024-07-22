# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 22:41:03 2022

@author: DELL
"""
'''本程序  用于
   读取CESM2-single强迫实验数据,并计算整理为x_ghg等数据集
'''
'调包，整理文件夹'
import netCDF4 as nc
import numpy as np
import os
path = 'H:/search2/cesm2/'
files =sorted(os.listdir(path))
AAER_SSP370 = files[0:15]
AAER        = files[15:95]
BMB_SSP370  = files[95:110]
BMB         = files[110:170]
EE_SSP370   = files[170:185]
EE          = files[185:245]
GHG_SSP370  = files[245:260]
GHG         = files[260:320]
xAER        = files[320:338]
xAER_SSP370 = files[338:348]
#%%
'函数写在这里'
def get_var(nc_filename):
    var = []
    nf = nc.Dataset(nc_filename,'r')
    key_list = list(nf.variables.keys())

    for i in range(0,len(key_list)):
        var.append(nf.variables[key_list[i]][:])
    return var,key_list

def get_SIE(sic,tarea):
    '计算给定的像元面积'
    s = np.nansum(sic*tarea)/(10**12)  #10^6平方千米
    return s

def get_section_SIE(tarea,sic):
    '分海区，计算各海区的海冰面积'
    sic = sic[0:37][:]
    tarea = tarea[0:37][:]
    
    sic[np.where(sic==10.**30)]=np.nan
    sic[np.where(sic<=0.15)]=np.nan
    tarea[np.where(tarea==10.**30)]=np.nan
    
    amundsen_sic   = sic[:,257:294]
    amundsen_tarea = tarea[:,257:294] 
    
    Weddell_sic    = np.hstack((sic[:,0:23],sic[:,294:]))
    Weddell_tarea  = np.hstack((tarea[:,0:23],tarea[:,294:]))
    Weddell_sic[np.where(Weddell_sic>1)] = 0
    
    KingHakon_sic   = sic[:][23:99]
    KingHakon_tarea = tarea[:][23:99]
    
    EastAntarctica_sic   = sic[:,99:180]
    EastAntarctica_tarea = tarea[:,99:180]
    
    RossAmundsen_sic   = sic[:,180:257]
    RossAmundsen_tarea = tarea[:,180:257]
    
    s1 = get_SIE(amundsen_sic, amundsen_tarea)
    s2 = get_SIE(Weddell_sic, Weddell_tarea)
    s3 = get_SIE(KingHakon_sic, KingHakon_tarea)
    s4 = get_SIE(EastAntarctica_sic, EastAntarctica_tarea)
    s5 = get_SIE(RossAmundsen_sic,RossAmundsen_tarea)
    return s1,s2,s3,s4,s5

def get_season_mean(s,season,k):
    '计算指定季节的海冰面积'
    if season=='DJF':
        index1,index2,index3=11+12*k,12*k+12,13+12*k
    elif season=='MAM':
        index1,index2,index3=14+12*k,15+12*k,16+12*k
    elif season=='JJA':
        index1,index2,index3=17+12*k,18+12*k,19+12*k
    elif season=='SON':
        index1,index2,index3=20+12*k,21+12*k,22+12*k
    mean = (s[index1]+s[index2]+s[index3])/3
    return mean

def get_seasonal_SIE(sie1,sie2,sie3,sie4,sie5,years):

    '''
    因为1850——2014共165年，但是第一个DJF应该是由1850年的12月，1851年的1月、2月构成，故years
    这个参数（其实也是get_season_mean方法中的参数k）取值范围是0-164
    '''

    area1,area2,area3,area4,area5=[],[],[],[],[]
    for season in ['DJF','MAM','JJA','SON']:
        for k in range(0,years): 
            tmp1 = get_season_mean(sie1, season, k)
            tmp2 = get_season_mean(sie2, season, k)
            tmp3 = get_season_mean(sie3, season, k)
            tmp4 = get_season_mean(sie4, season, k)
            tmp5 = get_season_mean(sie5, season, k)
            area1.append(tmp1)
            area2.append(tmp2)
            area3.append(tmp3)
            area4.append(tmp4)
            area5.append(tmp5)
    return area1,area2,area3,area4,area5

def output_sectional_seasonal_SIE(a,years):  
    a_SIE_DJF = a[0:years]
    a_SIE_MAM = a[years:years*2]
    a_SIE_JJA = a[years*2:years*3]
    a_SIE_SON = a[years*3:]
    return a_SIE_DJF,a_SIE_MAM,a_SIE_JJA,a_SIE_SON

def main(force,filefirst,filelast,years):
    '''
    force : 
        强迫代号，见最上方.
    filefirst : 
        该强迫文件夹下访问起点
    filelast : 
        该强迫文件夹下访问终点
    years : 
        每种强迫对应的总年数是确定的.
        比如AAER对应1850-2014共165年
    '''
    sie1,sie2,sie3,sie4,sie5=[],[],[],[],[]
    for j in range(filefirst,filelast):   
        var,key_list= get_var(path+force[j])
        tarea = var[9]
        sic   = var[25]
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
#%%

def get_dataframe_totalave(j,dataframe):
    temp = dataframe[0][j]
    for k in range(1,len(dataframe)):
        temp = np.sum([temp,dataframe[k][j]],axis=0).tolist()
    temp = np.divide(temp,(len(dataframe)+0.0)) 
    return temp


def mainloop_to_xi(force,years):
    dataframe = [main(force,4*k,4*(k+1),years) for k in range(0,int(len(force)/4))]
    dataframe_total = [get_dataframe_totalave(j,dataframe) for j in range(0,20)]
    return dataframe_total


x_ghg  =  mainloop_to_xi(GHG,164)