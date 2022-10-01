
# coding: utf-8

# In[ ]:


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import csv
from datetime import datetime
import function as fuc
import geatpy as ga
import GA as GA
import glovar as glo
from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpi4py import MPI
import math
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset, date2index
from netCDF4 import num2date
from netCDF4 import date2num
import os
from pydap.client import open_url
import seawater as sw
import sys
import time as t

from tqdm import tqdm


# In[ ]:


#initial mpi environment
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()


# In[ ]:


"""Set global constants"""
#set search range, the unit is degree
glo.time=900
glo.lon_start=100
glo.lon_end=126
glo.lat_start=2
glo.lat_end=23

#set search accuracy, the unit is degree
glo.acc=2
glo.iden_tol=10
glo.island_tol=0.001
glo.C_tol=10
#set constants in GA
glo.nind=100
glo.maxgen=1000


# In[ ]:


""" 0 process Load the velocity field dataset """
if comm_rank==0:
    #connect the data set
    print("进程创建完成，共",comm_size,"个进程，进程",comm_rank,"正在下载数据")
    dataset_uvel =Dataset('http://apdrc.soest.hawaii.edu:80/dods/public_data/ECCO2/cube92/uvel')
    dataset_vvel =Dataset('http://apdrc.soest.hawaii.edu:80/dods/public_data/ECCO2/cube92/vvel')    
    #get the data by use of the keys
    u=dataset_uvel.variables['uvel']
    v=dataset_vvel.variables['vvel']
    time=dataset_uvel.variables['time']
    #global variables assignment
    glo.global_lat=np.array(dataset_uvel.variables['lat'])
    glo.global_lon=np.array(dataset_uvel.variables['lon'])
    glo.global_u=u[glo.time,1,:,:]
    glo.global_v=v[glo.time,1,:,:]
"""broadcast the velocity field data"""
if comm_rank==0:
    print('数据下载完成，正在分发给其余',comm_size-1,'个进程')
glo.global_lat=comm.bcast(glo.global_lat, root=0)
glo.global_lon=comm.bcast(glo.global_lon, root=0)
glo.global_u=comm.bcast(glo.global_u, root=0)
glo.global_v=comm.bcast(glo.global_v, root=0)
if comm_rank==0:
    print('流场数据分发完毕')


# In[ ]:


#assign calculating block
lon_range=glo.lon_end-glo.lon_start
if comm_rank==0:
    print("开始分配任务")
else:
    block=(lon_range-lon_range%(comm_size-1))/(comm_size-1)+1
    my_lon_start=(comm_rank-1)*block+glo.lon_start
    if my_lon_start+block<=glo.lon_end:
        my_lon_end=my_lon_start+block
        my_lon_range=my_lon_end-my_lon_start
    else:
        my_lon_end=glo.lon_end
        my_lon_range=my_lon_end-my_lon_start
    glo.lon_start=my_lon_start
    glo.lon_end=my_lon_end
    
    print(comm_rank,"号进程处理经度",glo.lon_start,"到",glo.lon_end,"的数据")


# In[ ]:


#initial eddy recording array
eddy_record=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#eddy_record=np.array([comm_rank,comm_rank,comm_rank,comm_rank,comm_rank,comm_rank])


# In[ ]:


#search the eddy
if comm_rank>0:
    #generlize the search step
    lon_step,lat_step,lon_half_step,lat_half_step=fuc.search_step()
    #GA=__import__('GA')
    #entail step
    pbar=tqdm(range(lon_step.shape[0]-1))
    for i in pbar:
        pbar.set_description("进程 %s" % comm_rank)
        for j in range(lat_step.shape[0]-1):
            #set the local coordinates&velocity
            #print('计算经度：',lon_step[i],'-',lon_step[i+1],'纬度',lat_step[j],'-',lat_step[j+1])
            fuc.local_data_set(lon_step[i],lon_step[i+1],lat_step[j],lat_step[j+1])
            #Judge whether it is land or not
            if ((np.max(abs(glo.local_u[:,:])<glo.island_tol)and(np.max(abs(glo.local_v[:,:])<glo.island_tol)))):
                aaa=1
            #    print('此区域为陆地')
            else:
                eddy1,eddy2,eddy3,eddy4,eddy5,eddy6,eddy7,eddy8,eddy9,eddy0,eddy11,eddy12,eddy13,eddy14=GA.GA(glo.nind,glo.maxgen,lon_step[i],lon_step[i+1],lat_step[j],lat_step[j+1])
                
                eddy_record=np.append(eddy_record,[eddy1,eddy2,eddy3,eddy4,eddy5,eddy6,eddy7,eddy8,eddy9,eddy0,eddy11,eddy12,eddy13,eddy14])


# In[ ]:


eddy_record=comm.gather(eddy_record, root=0)
if comm_rank==0:
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('数据收集完毕，正在绘图。。。')
    #eddy_record=np.array(eddy_record)
    #print(eddy_record.shape)
    #print(eddy_record)
    eddy=list(chain(*eddy_record))
    print('数据转换完成')
    #print(eddy_record[0]+eddy_record[1])
    #print('数据转换完成11111')
    #print(eddy)
    #draw pic
    fuc.local_data_set(glo.lon_start,glo.lon_end,glo.lat_start,glo.lat_end)
    glo.search_lon=glo.local_lon
    glo.search_lat=glo.local_lat
    glo.search_u=glo.local_u
    glo.search_v=glo.local_v
    #Check the search area
    X,Y = np.meshgrid(glo.local_lon[:],glo.local_lat[:])
    U=glo.search_u
    V=glo.search_v
    
    #write the identification result into a csv file named data
    eddy=np.array(eddy)
    k=eddy.shape[0]/14
    eddy=eddy.reshape((int(k),14))
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('正在写入数据文件。。。')
    out = open('data.csv','a', newline='')
    #设定写入模式
    csv_write = csv.writer(out,dialect='excel')
    #写入具体内容
    csv_write.writerows(eddy)
    out.close()
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('写入数据完毕')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

