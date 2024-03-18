import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import pandas as pd

SLA=Dataset('../copernicus/cmems_1999-01-01~2018-12-31.nc')
SLA_test=Dataset('../copernicus/cmems_2019-01-01~2019-12-31.nc')

maplat=SLA.variables['latitude'][:]
maplon=SLA.variables['longitude'][:]

'''--------------------Test Grid Data--------------------'''
grid_acs_test=np.load('./Data/grid_acs_test.npy',allow_pickle=True).item()
grid_acl_test=np.load('./Data/grid_acl_test.npy',allow_pickle=True).item()
grid_cs_test=np.load('./Data/grid_cs_test.npy',allow_pickle=True).item()
grid_cl_test=np.load('./Data/grid_cl_test.npy',allow_pickle=True).item()

grid_all_test={}
for key in grid_acs_test.keys():
    grid_all_test[key]=grid_acs_test[key]+grid_acl_test[key]+grid_cs_test[key]+grid_cl_test[key]

np.save('./Data/grid_all_test.npy',grid_all_test._getvalue())

'''--------------------Train Grid Data--------------------'''
grid_acs=np.load('./Data/grid_acs.npy',allow_pickle=True).item()
grid_acl=np.load('./Data/grid_acl.npy',allow_pickle=True).item()
grid_cs=np.load('./Data/grid_cs.npy',allow_pickle=True).item()
grid_cl=np.load('./Data/grid_cl.npy',allow_pickle=True).item()

grid_all_train={}
for key in grid_acs.keys():
    grid_all_train[key]=grid_acs[key]+grid_acl[key]+grid_cs[key]+grid_cl[key]

np.save('./Data/grid_all_train.npy',grid_all_train._getvalue())

'''--------------------Test ADT Data--------------------'''
