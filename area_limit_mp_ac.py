import numpy as np
from netCDF4 import Dataset
#import matplotlib.pyplot as plt
#import pandas as pd
import time as tm
import multiprocessing as mp
from functools import partial
import os

latmin=24.875
latmax=44.875
lonmin=134.875
lonmax=179.875

ACS=Dataset('META3.1exp_DT_allsat_Anticyclonic_short_19930101_20200307.nc')
#print(ACS.variables.keys())
ACL=Dataset('META3.1exp_DT_allsat_Anticyclonic_long_19930101_20200307.nc')
#print(ACL.variables.keys())
ACU=Dataset('META3.1exp_DT_allsat_Anticyclonic_untracked_19930101_20200307.nc')

if not os.path.exists('Data'):
    os.mkdir('Data')

# SLA=Dataset('../copernicus/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.25deg_P1D_1704119807053.nc')
# #print(SLA.variables.keys())

# adt=SLA.variables['adt'][:]
# maplat=SLA.variables['latitude'][:]
# maplon=SLA.variables['longitude'][:]

'''--------------------Part for ACS--------------------'''
time_acs=ACS.variables['time'][:]
center_lon_acs=ACS.variables['longitude'][:]
center_lat_acs=ACS.variables['latitude'][:]

def area_limit_acs(i,contour_coordinate_acs,contour_time_acs,center_acs):
    if (center_lat_acs[i] >= latmin) and (center_lat_acs[i] <= latmax) and (center_lon_acs[i] >= lonmin) and (center_lon_acs[i] <= lonmax): #提取研究范围内数据
        contour_coordinate_acs[i]=[ACS.variables['effective_contour_longitude'][i], ACS.variables['effective_contour_latitude'][i]]
        contour_time_acs[i]=time_acs[i]
        center_acs[i]=[center_lon_acs[i],center_lat_acs[i]]

'''--------------------Part for ACL--------------------'''
time_acl=ACL.variables['time'][:]
center_lon_acl=ACL.variables['longitude'][:]
center_lat_acl=ACL.variables['latitude'][:]

def area_limit_acl(i,contour_coordinate_acl,contour_time_acl,center_acl):
    if (center_lat_acl[i] >= latmin) and (center_lat_acl[i] <= latmax) and (center_lon_acl[i] >= lonmin) and (center_lon_acl[i] <= lonmax):  #提取研究范围内数据
        contour_coordinate_acl[i]=[ACL.variables['effective_contour_longitude'][i], ACL.variables['effective_contour_latitude'][i]]
        contour_time_acl[i]=time_acl[i]
        center_acl[i]=[center_lon_acl[i],center_lat_acl[i]]

'''--------------------Part for ACU--------------------'''
time_acu=ACU.variables['time'][:]
center_lon_acu=ACU.variables['longitude'][:]
center_lat_acu=ACU.variables['latitude'][:]

def area_limit_acu(i,contour_coordinate_acu,contour_time_acu,center_acu):
    if (center_lat_acu[i] >= latmin) and (center_lat_acu[i] <= latmax) and (center_lon_acu[i] >= lonmin) and (center_lon_acu[i] <= lonmax):  #提取研究范围内数据
        contour_coordinate_acu[i]=[ACU.variables['effective_contour_longitude'][i], ACU.variables['effective_contour_latitude'][i]]
        contour_time_acu[i]=time_acu[i]
        center_acu[i]=[center_lon_acu[i],center_lat_acu[i]]
    
'''--------------------Multiprocessing--------------------'''
if __name__ == '__main__':
    __spec__ = None
    manager=mp.Manager()
    contour_coordinate_acs = manager.dict()
    contour_time_acs = manager.dict()
    center_acs = manager.dict()

    contour_coordinate_acl = manager.dict()
    contour_time_acl = manager.dict()
    center_acl = manager.dict()

    contour_coordinate_acu = manager.dict()
    contour_time_acu = manager.dict()
    center_acu = manager.dict()

    start_time = tm.time()

    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_acs, contour_coordinate_acs=contour_coordinate_acs,contour_time_acs=contour_time_acs,center_acs=center_acs), range(len(time_acs)))
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_acl, contour_coordinate_acl=contour_coordinate_acl,contour_time_acl=contour_time_acl,center_acl=center_acl), range(len(time_acl)))
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_acu, contour_coordinate_acu=contour_coordinate_acu,contour_time_acu=contour_time_acu,center_acu=center_acu), range(len(time_acu)))
    pool.close()
    pool.join()

    #print(contour_coordinate_acs[114])
    #print(contour_time_acs[0:114])
    #print(contour_index_acs[0:114])
    end_time=tm.time()
    elapsed_time=end_time-start_time
    print(f"花费时间：{elapsed_time:.2f}s")
    
    np.save('./Data/contour_coordinate_acs',contour_coordinate_acs._getvalue())
    np.save('./Data/contour_time_acs',contour_time_acs._getvalue())
    np.save('./Data/center_acs',center_acs._getvalue())

    np.save('./Data/contour_coordinate_acl',contour_coordinate_acl._getvalue())
    np.save('./Data/contour_time_acl',contour_time_acl._getvalue())
    np.save('./Data/center_acl',center_acl._getvalue())

    np.save('./Data/contour_coordinate_acu',contour_coordinate_acu._getvalue())
    np.save('./Data/contour_time_acu',contour_time_acu._getvalue())
    np.save('./Data/center_acu',center_acu._getvalue())

    '''
    保存为三个字典：
    contour_coordinate:顶点的坐标，格式为[[50个lon],[50个lat]],即list中每个元素shape均为(2,50)
    contour_time:顶点坐标获取的时间
    center_acu:中心的坐标，格式为[lon,lat]
    索引为顶点坐标在原始数据中对应的序号
    '''