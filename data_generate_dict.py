import numpy as np
from netCDF4 import Dataset
from datetime import datetime

SLA=Dataset('../copernicus/cmems_1999-01-01~2018-12-31.nc')
SLA_test=Dataset('../copernicus/cmems_2019-01-01~2019-12-31.nc')

maplat=SLA.variables['latitude'][:]
maplon=SLA.variables['longitude'][:]

'''--------------------Test Grid Data--------------------'''
grid_acs_test=np.load('./Data/grid_acs_test.npy',allow_pickle=True).item()
grid_acl_test=np.load('./Data/grid_acl_test.npy',allow_pickle=True).item()
grid_acu_test=np.load('./Data/grid_acu_test.npy',allow_pickle=True).item()
grid_cs_test=np.load('./Data/grid_cs_test.npy',allow_pickle=True).item()
grid_cl_test=np.load('./Data/grid_cl_test.npy',allow_pickle=True).item()
grid_cu_test=np.load('./Data/grid_cu_test.npy',allow_pickle=True).item()

grid_all_test_dict={}
for key in grid_acs_test.keys():
    grid_all_test_dict[key]=np.maximum(np.maximum(np.maximum(np.maximum(np.maximum(grid_acs_test[key],grid_acl_test[key]),grid_acu_test[key]),grid_cs_test[key]),grid_cl_test[key]),grid_cu_test[key])

np.save('./Data/grid_all_test_dict.npy',grid_all_test_dict)

'''--------------------Train Grid Data--------------------'''
grid_acs=np.load('./Data/grid_acs.npy',allow_pickle=True).item()
grid_acl=np.load('./Data/grid_acl.npy',allow_pickle=True).item()
grid_acu=np.load('./Data/grid_acu.npy',allow_pickle=True).item()
grid_cs=np.load('./Data/grid_cs.npy',allow_pickle=True).item()
grid_cl=np.load('./Data/grid_cl.npy',allow_pickle=True).item()
grid_cu=np.load('./Data/grid_cu.npy',allow_pickle=True).item()

grid_all_train_dict={}
for key in grid_acs.keys():
    grid_all_train_dict[key]=np.maximum(np.maximum(np.maximum(np.maximum(np.maximum(grid_acs[key],grid_acl[key]),grid_acu[key]),grid_cs[key]),grid_cl[key]),grid_cu[key])

np.save('./Data/grid_all_train_dict.npy',grid_all_train_dict)

'''--------------------Test ADT Data--------------------'''
adt_test=SLA_test['adt'][:]
time_test=SLA_test['time'][:]
adt_test_dict={}
for i in range(len(time_test)):
    delta = datetime.fromtimestamp(time_test[i]) - datetime.strptime('1950-01-01','%Y-%m-%d')
    delta = delta.days
    adt_test_dict[delta]=adt_test[i]

np.save('./Data/adt_test_dict.npy',adt_test_dict)

'''--------------------Train ADT Data--------------------'''
adt=SLA['adt'][:]
time=SLA['time'][:]
adt_dict={}
for i in range(len(time)):
    delta = datetime.fromtimestamp(time[i]) - datetime.strptime('1950-01-01','%Y-%m-%d')
    delta = delta.days
    adt_dict[delta]=adt[i]

np.save('./Data/adt_train_dict.npy',adt_dict)