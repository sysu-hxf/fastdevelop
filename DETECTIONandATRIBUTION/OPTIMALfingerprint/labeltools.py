# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 17:45:08 2022

@author: DELL
"""
import numpy as np
import matplotlib.pyplot as plt
def label_tools(num):
    if num==0:
        label='DJF-Amundsen–Bellingshausen'
    if num==1:
        label='MAM-Amundsen–Bellingshausen'
    if num==2:
        label='JJA-Amundsen–Bellingshausen'
    if num==3:
        label='SON-Amundsen–Bellingshausen'
    if num==4:
        label='DJF-Weddell'
    if num==5:
        label='MAM-Weddell'
    if num==6:
        label='JJA-Weddell'    
    if num==7:
        label='SON-Weddell'
    if num==8:
        label='DJF-King Hakon VII'
    if num==9:
        label='MAM-King Hakon VII'
    if num==10:
        label='JJA-King Hakon VII'
    if num==11:
        label='SON-King Hakon VII'
    if num==12:
        label='DJF-East Antarctica'
    if num==13:
        label='MAM-East Antarctica'
    if num==14:
        label='JJA-East Antarctica'
    if num==15:
        label='SON-East Antarctica'
    if num==16:
        label='DJF-Ross–Amundsen Seas'
    if num==17:
        label='MAM-Ross–Amundsen Seas'
    if num==18:
        label='JJA-Ross–Amundsen Seas'
    if num==19:
        label='SON-Ross–Amundsen Seas'
    return label  

def get_recdata(filename):
    import netCDF4 as nc
    path ='H:/search2/reconstruction/best_fit/'+filename
    nf = nc.Dataset(path,'r')
    rec = nf.variables['best_fit'][:].data    
    rec=rec[:110]
    return rec
def get_obsdata(filename):
    import netCDF4 as nc
    path ='H:/search2/reconstruction/best_fit/'+filename
    nf = nc.Dataset(path,'r')
    obs = nf.variables['obs'][:].data    
    obs=obs[:110]
    return obs

def Average_nonoverlap(data,window):
    newdata_num = int(len(data)/(window+0.0))
    newdata=np.zeros(newdata_num)
    for i in range(0,newdata_num):
        left = window*i
        right = left+window
        newdata[i] = np.mean(data[left:right])
    return newdata

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w

def juping(data):
    data = data - np.mean(data)
    return data

def printbeta(beta):
    print(beta[0][0])
    print(beta[1][0])
    print(beta[2][0])
    
def recons_name(startnum,endnum):
    # 参数分别可选：0~4,4~8,8~12,12~16,16~20
    sector=['Amundsen_Bellingshausen','Weddell','King_Hakon',
            'East_Antarctica','Ross_Amundsen']
    season=['DJF','MAM','JJA','SON']
    trail = '_best_fit_recons_'
    obs_reconlist = [sector[i]+trail+season[j]+'.nc' for i in range(0,5) 
                for j in range(0,4)]
    return obs_reconlist[startnum:endnum]

'''
nx = np.array([15,20])
beta = da(obs1,[x_xx_ghg,x_xx_aaer],nx,ross1,
          reg='TLS',cons_test='AS03',formule_ic_tls='AS03',
          sample_extr='segment') 
'''

def draw_series(t,xall,xrecon,ctl,obs,labelx1,labelx2,labelx3,label4,interval,title):
    std_allano = np.std(xall)
    std_recano = np.std(xrecon)

    plt.fill_between(t, xall-1.64*std_allano,   xall+1.64*std_allano,  facecolor = 'lightblue',alpha=0.6)
    plt.fill_between(t, xrecon-1.64*std_recano, xrecon+1.64*std_recano,facecolor = 'lightgreen',alpha=0.6)

    plt.plot(t,xall,'steelblue',label=labelx1)
    plt.plot(t,xrecon,'seagreen',label=labelx2)
    plt.plot(t,ctl,'grey',label=labelx3,linestyle='dashed')
    plt.plot(t,obs,'black',label=label4)
    plt.legend()
    plt.ylabel('SIE'+'$(10^6km^2)$',labelpad=-62,y=1.02,rotation=0,fontsize=12)
    plt.xticks([i for i in range(t[0],t[-1],interval)],rotation = 45)
    #plt.title(title,fontstyle='italic',fontsize=12)
def ctlaverage(ctl,gap):
    '这个是用来画时间序列图里那个110组的CTL的！！！不是用来滑动平均的'
    num = int(len(ctl)/gap)
    ctl_new = np.zeros((gap))
    for k in range(0,num):
        tmp = []
        tmp.extend(ctl[k*gap:k*gap+gap])
        ctl_new = ctl_new + np.array(tmp)
    ctl_new = ctl_new/(num+0.0)
    return ctl_new

def beta_from_ofsss(beta):
    B_DJF_0514,B_DJF_0560,B_DJF_6014 = beta[0],beta[1],beta[2]
    B_MAM_0514,B_MAM_0560,B_MAM_6014 = beta[3],beta[4],beta[5]
    B_JJA_0514,B_JJA_0560,B_JJA_6014 = beta[6],beta[7],beta[8]
    B_SON_0514,B_SON_0560,B_SON_6014 = beta[9],beta[10],beta[11]
    B = B_DJF_0514,B_DJF_0560,B_DJF_6014,B_MAM_0514,B_MAM_0560,B_MAM_6014,B_JJA_0514,B_JJA_0560,B_JJA_6014,B_SON_0514,B_SON_0560,B_SON_6014
    return B


colorscheme = ['springgreen','steelblue','crimson',
                   'springgreen','steelblue','crimson',
                   'springgreen','steelblue','crimson',
                   'springgreen','steelblue','crimson']


 