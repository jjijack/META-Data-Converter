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
#计算起止时间
#print(datetime.datetime.strptime('1999-01-01','%Y-%m-%d')-datetime.datetime.strptime('1950-01-01','%Y-%m-%d'))
times=range(17897,25202) #1999-1-1 to 2018-12-31

SLA=Dataset('../copernicus/cmems_1999-01-01~2018-12-31.nc')
#print(SLA.variables.keys())

adt=SLA.variables['adt'][:]
maplat=SLA.variables['latitude'][:]
maplat=np.asarray(maplat)
maplon=SLA.variables['longitude'][:]
maplon=np.asarray(maplon)

def point_in_polygon(x, y, poly_x, poly_y):    #判断grid坐标是否位于涡旋边界内部，输入grid lon, grid lat, contour lon, contour lat
    num_vertices = len(poly_x)
    inside = False
    j = num_vertices - 1
    for i in range(num_vertices):
        if ((poly_y[i] > y) != (poly_y[j] > y)) and (x < (poly_x[j] - poly_x[i]) * (y - poly_y[i]) / (poly_y[j] - poly_y[i]) + poly_x[i]):
            inside = not inside
        j = i
    return inside

def find_nearest(array,value):      #寻找与涡旋中心点经纬度坐标距离最近的地图网格
    idx=np.abs(array-value).argmin()
    return idx

'''--------------------Part for ACS--------------------'''
contour_coordinate_acs=np.load('./Data/contour_coordinate_acs.npy',allow_pickle=True).item()
contour_time_acs=np.load('./Data/contour_time_acs.npy',allow_pickle=True).item()
center_acs=np.load('./Data/center_acs.npy',allow_pickle=True).item()

def trans_acs(time,grid_total):
    grid_data = np.zeros((len(maplat), len(maplon)))
    for k in contour_time_acs:
        if contour_time_acs[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_acs[k][0], contour_coordinate_acs[k][1]):
                        grid_data[i, j] = 1

            cj=find_nearest(maplon,center_acs[k][0])
            ci=find_nearest(maplat,center_acs[k][1])
            grid_data[ci, cj] = 2

    grid_total[time]=grid_data
    
'''--------------------Part for ACL--------------------'''
contour_coordinate_acl=np.load('./Data/contour_coordinate_acl.npy',allow_pickle=True).item()
contour_time_acl=np.load('./Data/contour_time_acl.npy',allow_pickle=True).item()
center_acl=np.load('./Data/center_acl.npy',allow_pickle=True).item()

def trans_acl(time,grid_total):
    grid_data = np.zeros((len(maplat), len(maplon)))
    for k in contour_time_acl:
        if contour_time_acl[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_acl[k][0], contour_coordinate_acl[k][1]):
                        grid_data[i, j] = 1

            cj=find_nearest(maplon,center_acl[k][0])
            ci=find_nearest(maplat,center_acl[k][1])
            grid_data[ci, cj] = 2

    grid_total[time]=grid_data

'''--------------------Part for ACU--------------------'''
contour_coordinate_acu=np.load('./Data/contour_coordinate_acu.npy',allow_pickle=True).item()
contour_time_acu=np.load('./Data/contour_time_acu.npy',allow_pickle=True).item()
center_acu=np.load('./Data/center_acu.npy',allow_pickle=True).item()

def trans_acu(time,grid_total):
    grid_data = np.zeros((len(maplat), len(maplon)))
    for k in contour_time_acu:
        if contour_time_acu[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_acu[k][0], contour_coordinate_acu[k][1]):
                        grid_data[i, j] = 1

            cj=find_nearest(maplon,center_acu[k][0])
            ci=find_nearest(maplat,center_acu[k][1])
            grid_data[ci, cj] = 2

    grid_total[time]=grid_data
    
'''--------------------Multiprocessing--------------------'''
if __name__ == '__main__':
    __spec__ = None
    manager=mp.Manager()
    grid_total_acs=manager.dict()
    grid_total_acl=manager.dict()
    grid_total_acu=manager.dict()

    start_time = tm.time()

    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    pool.map(partial(trans_acs, grid_total=grid_total_acs), times)
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(trans_acl, grid_total=grid_total_acl), times)
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(trans_acu, grid_total=grid_total_acu), times)
    pool.close()
    pool.join()

    end_time=tm.time()
    elapsed_time=end_time-start_time
    print(f"花费时间：{elapsed_time:.2f}s")

    np.save('./Data/grid_acs',grid_total_acs._getvalue())
    np.save('./Data/grid_acl',grid_total_acl._getvalue())
    np.save('./Data/grid_acu',grid_total_acu._getvalue())
    '''
    保存为一个字典：索引为相对1950-01-01偏移的日期，值为该时间下的格点坐标
    '''
