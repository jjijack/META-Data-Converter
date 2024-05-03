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

CS=Dataset('META3.1exp_DT_allsat_Cyclonic_short_19930101_20200307.nc')
#print(CS.variables.keys())
CL=Dataset('META3.1exp_DT_allsat_Cyclonic_long_19930101_20200307.nc')
#print(CL.variables.keys())
CU=Dataset('META3.1exp_DT_allsat_Cyclonic_untracked_19930101_20200307.nc')

if not os.path.exists('Data'):
    os.mkdir('Data')

# SLA=Dataset('../copernicus/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-ducs-0.25deg_P1D_1704119807053.nc')
# #print(SLA.variables.keys())

# adt=SLA.variables['adt'][:]
# maplat=SLA.variables['latitude'][:]
# maplon=SLA.variables['longitude'][:]

'''--------------------Part for CS--------------------'''
time_cs=CS.variables['time'][:]
center_lon_cs=CS.variables['longitude'][:]
center_lat_cs=CS.variables['latitude'][:]

def area_limit_cs(i,contour_coordinate_cs,contour_time_cs,center_cs):
    if (center_lat_cs[i] >= latmin) and (center_lat_cs[i] <= latmax) and (center_lon_cs[i] >= lonmin) and (center_lon_cs[i] <= lonmax):  #提取研究范围内数据
        contour_coordinate_cs[i]=[CS.variables['effective_contour_longitude'][i], CS.variables['effective_contour_latitude'][i]]
        contour_time_cs[i]=time_cs[i]
        center_cs[i]=[center_lon_cs[i],center_lat_cs[i]]

'''--------------------Part for CL--------------------'''
time_cl=CL.variables['time'][:]
center_lon_cl=CL.variables['longitude'][:]
center_lat_cl=CL.variables['latitude'][:]

def area_limit_cl(i,contour_coordinate_cl,contour_time_cl,center_cl):
    if (center_lat_cl[i] >= latmin) and (center_lat_cl[i] <= latmax) and (center_lon_cl[i] >= lonmin) and (center_lon_cl[i] <= lonmax):  #提取研究范围内数据
        contour_coordinate_cl[i]=[CL.variables['effective_contour_longitude'][i], CL.variables['effective_contour_latitude'][i]]
        contour_time_cl[i]=time_cl[i]
        center_cl[i]=[center_lon_cl[i],center_lat_cl[i]]

'''--------------------Part for CU--------------------'''
time_cu=CU.variables['time'][:]
center_lon_cu=CU.variables['longitude'][:]
center_lat_cu=CU.variables['latitude'][:]

def area_limit_cu(i,contour_coordinate_cu,contour_time_cu,center_cu):
    if (center_lat_cu[i] >= latmin) and (center_lat_cu[i] <= latmax) and (center_lon_cu[i] >= lonmin) and (center_lon_cu[i] <= lonmax):  #提取研究范围内数据
        contour_coordinate_cu[i]=[CU.variables['effective_contour_longitude'][i], CU.variables['effective_contour_latitude'][i]]
        contour_time_cu[i]=time_cu[i]
        center_cu[i]=[center_lon_cu[i],center_lat_cu[i]]
    
'''--------------------Multiprocessing--------------------'''
if __name__ == '__main__':
    __spec__ = None
    manager=mp.Manager()
    contour_coordinate_cs = manager.dict()
    contour_time_cs = manager.dict()
    center_cs = manager.dict()

    contour_coordinate_cl = manager.dict()
    contour_time_cl = manager.dict()
    center_cl = manager.dict()

    contour_coordinate_cu = manager.dict()
    contour_time_cu = manager.dict()
    center_cu = manager.dict()

    start_time = tm.time()

    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_cs, contour_coordinate_cs=contour_coordinate_cs,contour_time_cs=contour_time_cs,center_cs=center_cs), range(len(time_cs)))
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_cl, contour_coordinate_cl=contour_coordinate_cl,contour_time_cl=contour_time_cl,center_cl=center_cl), range(len(time_cl)))
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_cu, contour_coordinate_cu=contour_coordinate_cu,contour_time_cu=contour_time_cu,center_cu=center_cu), range(len(time_cu)))
    pool.close()
    pool.join()

    #print(contour_coordinate_cs[114])
    #print(contour_time_cs[0:114])
    #print(contour_index_cs[0:114])
    end_time=tm.time()
    elapsed_time=end_time-start_time
    print(f"花费时间：{elapsed_time:.2f}s")
    
    np.save('./Data/contour_coordinate_cs',contour_coordinate_cs._getvalue())
    np.save('./Data/contour_time_cs',contour_time_cs._getvalue())
    np.save('./Data/center_cs',center_cs._getvalue())

    np.save('./Data/contour_coordinate_cl',contour_coordinate_cl._getvalue())
    np.save('./Data/contour_time_cl',contour_time_cl._getvalue())
    np.save('./Data/center_cl',center_cl._getvalue())

    np.save('./Data/contour_coordinate_cu',contour_coordinate_cu._getvalue())
    np.save('./Data/contour_time_cu',contour_time_cu._getvalue())
    np.save('./Data/center_cu',center_cu._getvalue())

    '''
    保存为三个字典：
    contour_coordinate:顶点的坐标，格式为[[50个lon],[50个lat]],即list中每个元素shape均为(2,50)
    contour_time:顶点坐标获取的时间
    center_acu:中心的坐标，格式为[lon,lat]
    索引为顶点坐标在原始数据中对应的序号
    '''