import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import pandas as pd
#from datetime import datetime

SLA=Dataset('../copernicus/cmems_1999-01-01~2018-12-31.nc')
SLA_test=Dataset('../copernicus/cmems_2019-01-01~2019-12-31.nc')

maplat=SLA.variables['latitude'][:]
maplon=SLA.variables['longitude'][:]

'''--------------------Test Grid Data--------------------'''
grid_acs_test=np.load('./Data/grid_acs_test_simple.npy',allow_pickle=True).item()
grid_acl_test=np.load('./Data/grid_acl_test_simple.npy',allow_pickle=True).item()
grid_cs_test=np.load('./Data/grid_cs_test_simple.npy',allow_pickle=True).item()
grid_cl_test=np.load('./Data/grid_cl_test_simple.npy',allow_pickle=True).item()

grid_all_test_dict={}
for key in grid_acs_test.keys():
    grid_all_test_dict[key]=np.maximum(np.maximum(np.maximum(grid_acs_test[key],grid_acl_test[key]),grid_cs_test[key]),grid_cl_test[key])

grid_all_test=[]
for key in sorted(grid_all_test_dict.keys()):
    grid_all_test.append(grid_all_test_dict[key])
    
grid_all_test=np.array(grid_all_test)

np.save('./Data/grid_all_test_simple.npy',grid_all_test)

'''--------------------Train Grid Data--------------------'''
grid_acs=np.load('./Data/grid_acs_simple.npy',allow_pickle=True).item()
grid_acl=np.load('./Data/grid_acl_simple.npy',allow_pickle=True).item()
grid_cs=np.load('./Data/grid_cs_simple.npy',allow_pickle=True).item()
grid_cl=np.load('./Data/grid_cl_simple.npy',allow_pickle=True).item()

grid_all_train_dict={}
for key in grid_acs.keys():
    grid_all_train_dict[key]=np.maximum(np.maximum(np.maximum(grid_acs[key],grid_acl[key]),grid_cs[key]),grid_cl[key])

grid_all_train=[]
for key in sorted(grid_all_train_dict.keys()):
    grid_all_train.append(grid_all_train_dict[key])

grid_all_train=np.array(grid_all_train)

np.save('./Data/grid_all_train_simple.npy',grid_all_train)

'''--------------------Test ADT Data--------------------'''
adt_test=SLA_test['adt'][:]
adt_test=np.array(adt_test)

np.save('./Data/adt_test.npy',adt_test)

'''--------------------Train ADT Data--------------------'''
adt=SLA['adt'][:]
adt=np.array(adt)

np.save('./Data/adt_train.npy',adt)