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

'''--------------------Part for CS--------------------'''
contour_coordinate_cs=np.load('./Data/contour_coordinate_cs.npy',allow_pickle=True).item()
contour_time_cs=np.load('./Data/contour_time_cs.npy',allow_pickle=True).item()
center_cs=np.load('./Data/center_cs.npy',allow_pickle=True).item()

def trans_cs(time,grid_total):
    grid_data = np.zeros((len(maplat), len(maplon)))
    for k in contour_time_cs:
        if contour_time_cs[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_cs[k][0], contour_coordinate_cs[k][1]):
                        grid_data[i, j] = 3

            cj=find_nearest(maplon,center_cs[k][0])
            ci=find_nearest(maplat,center_cs[k][1])
            grid_data[ci, cj] = 4

    grid_total[time]=grid_data
    
'''--------------------Part for CL--------------------'''
contour_coordinate_cl=np.load('./Data/contour_coordinate_cl.npy',allow_pickle=True).item()
contour_time_cl=np.load('./Data/contour_time_cl.npy',allow_pickle=True).item()
center_cl=np.load('./Data/center_cl.npy',allow_pickle=True).item()

def trans_cl(time,grid_total):
    grid_data = np.zeros((len(maplat), len(maplon)))
    for k in contour_time_cl:
        if contour_time_cl[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_cl[k][0], contour_coordinate_cl[k][1]):
                        grid_data[i, j] = 3

            cj=find_nearest(maplon,center_cl[k][0])
            ci=find_nearest(maplat,center_cl[k][1])
            grid_data[ci, cj] = 4

    grid_total[time]=grid_data

'''--------------------Part for CU--------------------'''
contour_coordinate_cu=np.load('./Data/contour_coordinate_cu.npy',allow_pickle=True).item()
contour_time_cu=np.load('./Data/contour_time_cu.npy',allow_pickle=True).item()
center_cu=np.load('./Data/center_cu.npy',allow_pickle=True).item()

def trans_cu(time,grid_total):
    grid_data = np.zeros((len(maplat), len(maplon)))
    for k in contour_time_cu:
        if contour_time_cu[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_cu[k][0], contour_coordinate_cu[k][1]):
                        grid_data[i, j] = 3

            cj=find_nearest(maplon,center_cu[k][0])
            ci=find_nearest(maplat,center_cu[k][1])
            grid_data[ci, cj] = 4

    grid_total[time]=grid_data
    
'''--------------------Multiprocessing--------------------'''
if __name__ == '__main__':
    __spec__ = None
    manager=mp.Manager()
    grid_total_cs=manager.dict()
    grid_total_cl=manager.dict()
    grid_total_cu=manager.dict()

    start_time = tm.time()

    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    pool.map(partial(trans_cs, grid_total=grid_total_cs), times)
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(trans_cl, grid_total=grid_total_cl), times)
    pool.close()
    pool.join()

    pool = mp.Pool(processes=num_processes)
    pool.map(partial(trans_cu, grid_total=grid_total_cu), times)
    pool.close()
    pool.join()

    end_time=tm.time()
    elapsed_time=end_time-start_time
    print(f"花费时间：{elapsed_time:.2f}s")

    np.save('./Data/grid_cs_simple',grid_total_cs._getvalue())
    np.save('./Data/grid_cl_simple',grid_total_cl._getvalue())
    np.save('./Data/grid_cu_simple',grid_total_cu._getvalue())
    '''
    保存为一个字典：索引为相对1950-01-01偏移的日期，值为该时间下的格点坐标
    '''
