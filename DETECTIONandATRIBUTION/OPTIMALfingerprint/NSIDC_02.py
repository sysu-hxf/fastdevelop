# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 23:07:41 2023

@author: DELL
"""

import os
import numpy as np
import netCDF4 as nc
#from pyproj import Proj
path_nsidc = 'H:/search2/SSMIS/'
Files_nsidc =sorted(os.listdir(path_nsidc))

def polar_stere_grid(grid_dir, hms, res):
    """
    Purpose: read polar stereographic grid
        south hemisphere: 664 x 632 (12.5 km), 332 x 316 (25 km)
        north hemisphere: 896 x 608 (12.5 km), 448 x 304 (25 km)

    :param
    :param res: resolution (12 or 25)
    :return: ps_grid = {'lon':lon, 'lat':lat, 'cellarea':cellarea}

    ref: (1) https://nsidc.org/data/user-resources/help-center/guide-nsidcs-polar-stereographic-projection
         (2) the scale of lon/lat is 1e5; the data type is 'long word integers (4 byte)', which can be
         found in the user manuals of the products that use this grid, e.g.,
         https://doi.org//10.5067/AMSR-E/AE_SI12.003
    """

    if hms == 'n':
        if res == 12:
            nx, ny = 896, 608
        elif res == 25:
            nx, ny = 448, 304
    elif hms == 's':
        if res == 12:
            nx, ny = 664, 632
        elif res == 25:
            nx, ny = 332, 316
    # <i4
    with open(grid_dir + 'ps' + hms + str(res) + 'area_v3.dat', 'rb') as raw_area:
        cellarea = np.fromfile(raw_area, dtype='int32').reshape(nx, ny) / 1e3  # unit: km^2, 32-bit integer
    with open(grid_dir + 'ps' + hms + str(res) + 'lons_v3.dat', 'rb') as raw_lon:
        lon = np.fromfile(raw_lon, dtype='int32').reshape(nx, ny) / 1e5
    with open(grid_dir + 'ps' + hms + str(res) + 'lats_v3.dat', 'rb') as raw_lat:
        lat = np.fromfile(raw_lat, dtype='int32').reshape(nx, ny) / 1e5

    print('Range of ps' + hms + str(res) + '\n\tcell area (unit: km2):', np.min(cellarea), np.max(cellarea),
          '\n\tlat:', np.min(lat), np.max(lat), '\n\tlon:', np.min(lon), np.max(lon))

    ps_grid = {'lon': lon, 'lat': lat, 'cellarea': cellarea}

    return ps_grid
ps_grid = polar_stere_grid('H:/search2/sic_sie/','s',25)
cell = ps_grid['cellarea'][:]/10**6
lon  = ps_grid['lon'][:]

#%%   
print("*************enter direction*****************")                     
direction = input()
SIE = []
for file in Files_nsidc:
    file = path_nsidc + file
    nf = nc.Dataset(file,'r')
    key_list = list(nf.variables.keys())
    sic = nf.variables[key_list[-1]][:].data
    sic = sic[0][:,:]
    sic[np.where(sic<0.15)] =   np.nan
    sic[np.where(sic>1)]     =  np.nan
    if direction == 'antarctic':
        SIE.append(np.nansum(sic[:,:]*cell[:,:]))
        
    elif direction == 'Amundsen_Bellingshausen':
        loc = np.where((lon<=-70) & (lon>=-110))
        SIE.append(np.nansum(sic[loc]*cell[loc]))   
        
    elif direction == 'Weddell':
        loc = np.where((lon<=-14) & (lon>=-70))
        SIE.append(np.nansum(sic[loc]*cell[loc]))
        
    elif direction == 'Ross_Amundsen':
        loc = np.where((lon>=162) | (lon<=-110))
        SIE.append(np.nansum(sic[loc]*cell[loc]))
        
    elif direction == 'East_Antarctica':
        loc = np.where((lon<=162) & (lon>=71))
        SIE.append(np.nansum(sic[loc]*cell[loc]))
        
    elif direction == 'King_Hakon':
        loc = np.where((lon<=71) & (lon>=-14))
        SIE.append(np.nansum(sic[loc]*cell[loc]))
Extreme_base = np.mean(SIE)


