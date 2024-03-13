import numpy as np
from netCDF4 import Dataset
#import matplotlib.pyplot as plt
#import pandas as pd
import time as tm
import multiprocessing as mp
from functools import partial

latmin=24.875
latmax=44.875
lonmin=134.875
lonmax=179.875

CS=Dataset('META3.1exp_DT_allsat_Cyclonic_short_19930101_20200307.nc')
#print(CS.variables.keys())
CL=Dataset('META3.1exp_DT_allsat_Cyclonic_long_19930101_20200307.nc')
#print(CL.variables.keys())

# SLA=Dataset('../copernicus/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-ducs-0.25deg_P1D_1704119807053.nc')
# #print(SLA.variables.keys())

# adt=SLA.variables['adt'][:]
# maplat=SLA.variables['latitude'][:]
# maplon=SLA.variables['longitude'][:]

'''--------------------Part for CS--------------------'''
time_cs=CS.variables['time'][:]
center_lon_cs=CS.variables['longitude'][:]
center_lat_cs=CS.variables['latitude'][:]

def area_limit_cs(i,contour_coordinate_cs,contour_time_cs):
    if (center_lat_cs[i] >= latmin) and (center_lat_cs[i] <= latmax) and (center_lon_cs[i] >= lonmin) and (center_lon_cs[i] <= lonmax):
        contour_coordinate_cs[i]=[CS.variables['effective_contour_longitude'][i], CS.variables['effective_contour_latitude'][i]]
        contour_time_cs[i]=time_cs[i]

'''--------------------Part for CL--------------------'''
time_cl=CL.variables['time'][:]
center_lon_cl=CL.variables['longitude'][:]
center_lat_cl=CL.variables['latitude'][:]

def area_limit_cl(i,contour_coordinate_cl,contour_time_cl):
    if (center_lat_cl[i] >= latmin) and (center_lat_cl[i] <= latmax) and (center_lon_cl[i] >= lonmin) and (center_lon_cl[i] <= lonmax):
        contour_coordinate_cl[i]=[CL.variables['effective_contour_longitude'][i], CL.variables['effective_contour_latitude'][i]]
        contour_time_cl[i]=time_cl[i]
    
'''--------------------Multiprocessing--------------------'''
if __name__ == '__main__':
    __spec__ = None
    manager=mp.Manager()
    contour_coordinate_cs = manager.dict()
    contour_time_cs = manager.dict()

    contour_coordinate_cl = manager.dict()
    contour_time_cl = manager.dict()

    start_time = tm.time()

    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_cs, contour_coordinate_cs=contour_coordinate_cs,contour_time_cs=contour_time_cs), range(len(time_cs)))
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(area_limit_cl, contour_coordinate_cl=contour_coordinate_cl,contour_time_cl=contour_time_cl), range(len(time_cl)))
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

    np.save('./Data/contour_coordinate_cl',contour_coordinate_cl._getvalue())
    np.save('./Data/contour_time_cl',contour_time_cl._getvalue())

    '''
    保存为两个字典：
    contour_coordinate:顶点的坐标，格式为[[50个lon],[50个lat]],即list中每个元素shape均为(2,50)
    contour_time:顶点坐标获取的时间
    索引为顶点坐标在原始数据中对应的序号
    '''