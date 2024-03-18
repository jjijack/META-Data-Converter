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
times=range(25202,25567) #2019-1-1 to 2019-12-31

SLA=Dataset('../copernicus/cmems_2019-01-01~2019-12-31.nc')
#print(SLA.variables.keys())

adt=SLA.variables['adt'][:]
maplat=SLA.variables['latitude'][:]
maplon=SLA.variables['longitude'][:]

def point_in_polygon(x, y, poly_x, poly_y):    #判断grid坐标是否位于涡旋边界内部，输入grid lon, grid lat, contour lon, contour lat
    num_vertices = len(poly_x)
    inside = False
    j = num_vertices - 1
    for i in range(num_vertices):
        if ((poly_y[i] > y) != (poly_y[j] > y)) and (x < (poly_x[j] - poly_x[i]) * (y - poly_y[i]) / (poly_y[j] - poly_y[i]) + poly_x[i]):
            inside = not inside
        j = i
    return inside

'''--------------------Part for CS--------------------'''
contour_coordinate_cs=np.load('./Data/contour_coordinate_cs.npy',allow_pickle=True).item()
contour_time_cs=np.load('./Data/contour_time_cs.npy',allow_pickle=True).item()
contour_type_cs=np.load('./Data/contour_type_cs.npy',allow_pickle=True).item()

def trans_cs(time,grid_total):
    grid_data = -np.ones((len(maplat), len(maplon)))
    for k in contour_time_cs:
        if contour_time_cs[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_cs[k][0], contour_coordinate_cs[k][1]):
                        grid_data[i, j] = contour_type_cs[k]

    grid_total[time]=grid_data
    
'''--------------------Part for CL--------------------'''
contour_coordinate_cl=np.load('./Data/contour_coordinate_cl.npy',allow_pickle=True).item()
contour_time_cl=np.load('./Data/contour_time_cl.npy',allow_pickle=True).item()
contour_type_cl=np.load('./Data/contour_type_cl.npy',allow_pickle=True).item()

def trans_cl(time,grid_total):
    grid_data = np.zeros((len(maplat), len(maplon)))
    for k in contour_time_cl:
        if contour_time_cl[k]==time:
            for i in range(len(maplat)):
                for j in range(len(maplon)):
                    if point_in_polygon(maplon[j], maplat[i], contour_coordinate_cl[k][0], contour_coordinate_cl[k][1]):
                        grid_data[i, j] = contour_type_cl[k]

    grid_total[time]=grid_data
    
'''--------------------Multiprocessing--------------------'''
if __name__ == '__main__':
    __spec__ = None
    manager=mp.Manager()
    grid_total_cs=manager.dict()
    grid_total_cl=manager.dict()

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

    end_time=tm.time()
    elapsed_time=end_time-start_time
    print(f"花费时间：{elapsed_time:.2f}s")

    np.save('./Data/grid_cs_test',grid_total_cs._getvalue())
    np.save('./Data/grid_cl_test',grid_total_cl._getvalue())
    '''
    保存为一个字典：索引为相对1950-01-01偏移的日期，值为该时间下的格点坐标
    '''
