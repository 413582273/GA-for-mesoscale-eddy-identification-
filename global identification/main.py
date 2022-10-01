
# coding: utf-8

# In[ ]:


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import csv
from datetime import datetime
import function as fuc
import geatpy as ga
import glovar as glo
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
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
import time as tm


# In[ ]:


"""Set global constants"""
#set search range, the unit is degree
glo.time=900
glo.lon_start=108
glo.lon_end=120
glo.lat_start=12
glo.lat_end=23
#set search accuracy, the unit is degree
glo.acc=1
glo.iden_tol=5
glo.island_tol=0.001
glo.C_tol=6.0
#set constants in GA
glo.nind=100
glo.maxgen=200


# In[ ]:


"""Load the velocity field dataset """
#connect the data set
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


# In[ ]:


#draw pic
fuc.local_data_set(glo.lon_start,glo.lon_end,glo.lat_start,glo.lat_end)

glo.search_lon=glo.local_lon
glo.search_lat=glo.local_lat
glo.search_u=glo.local_u
glo.search_v=glo.local_v


# In[ ]:


#Check the search area
X,Y = np.meshgrid(glo.local_lon[:],glo.local_lat[:])
U=glo.search_u
V=glo.search_v


# In[ ]:


#generlize the search step
lon_step,lat_step,lon_half_step,lat_half_step=fuc.search_step()
#initial eddy recording array
eddy_record=np.array([0,0,0,0,0])


# In[ ]:


#search the eddy
GA=__import__('GA')
#entail step
for i in range(lon_step.shape[0]-1):
    for j in range(lat_step.shape[0]-1):
        #set the local coordinates&velocity
        print('计算经度：',lon_step[i],'-',lon_step[i+1],'纬度',lat_step[j],'-',lat_step[j+1])
        fuc.local_data_set(lon_step[i],lon_step[i+1],lat_step[j],lat_step[j+1])
        #Judge whether it is land or not
        if ((np.max(abs(glo.local_u[:,:])<glo.island_tol)and(np.max(abs(glo.local_v[:,:])<glo.island_tol)))):
            print('此区域为陆地')
        else:
            #search clockwise eddy
            glo.clockwise=1.0   
            eddy_lon,eddy_lat,eddy_C,eddy_R,eddyornot=GA.GA(glo.nind,glo.maxgen,lon_step[i],lon_step[i+1],lat_step[j],lat_step[j+1])
            if((eddyornot==1)and(eddy_C<glo.C_tol)):
                print(eddy_lon,eddy_lat,eddy_C,eddy_R)
                #record the search result
                eddy_record=np.append(eddy_record,[eddy_lon,eddy_lat,eddy_C,eddy_R,glo.clockwise])
            else:
                #search anti-clockwise eddy
                glo.clockwise=-1.0 
                eddy_lon,eddy_lat,eddy_C,eddy_R,eddyornot=GA.GA(glo.nind,glo.maxgen,lon_step[i],lon_step[i+1],lat_step[j],lat_step[j+1])
                if((eddyornot==1)and(eddy_C<glo.C_tol)):
                    print(eddy_lon,eddy_lat,eddy_C,eddy_R)
                    #record the search result
                    eddy_record=np.append(eddy_record,[eddy_lon,eddy_lat,eddy_C,eddy_R,glo.clockwise])


# #half_step
# for i in range(lon_half_step.shape[0]-1):
#     for j in range(lat_half_step.shape[0]-1):
#         #set the local coordinates&velocity
#         print('计算经度：',lon_half_step[i],'-',lon_half_step[i+1],'纬度',lat_half_step[j],'-',lat_half_step[j+1])
#         fuc.local_data_set(lon_half_step[i],lon_half_step[i+1],lat_half_step[j],lat_half_step[j+1])
#         #Judge whether it is land or not
#         if ((np.max(abs(glo.local_u[:,:])<glo.island_tol)and(np.max(abs(glo.local_v[:,:])<glo.island_tol)))):
#             print('此区域为陆地')
#         else:
#             eddy_lon,eddy_lat,eddy_C,eddy_R,eddyornot=GA.GA(nind,maxgen,lon_half_step[i],lon_half_step[i+1],lat_half_step[j],lat_half_step[j+1])
#             if(eddyornot==1):
#                 print(eddy_lon,eddy_lat,eddy_C,eddy_R)
#                 eddy_record=np.append(eddy_record,[eddy_lon,eddy_lat,eddy_C,eddy_R,glo.clockwise])

# #search the clockwise eddy
# glo.clockwise=-1.0   
# GA=__import__('GA')
# #entail step
# for i in range(lon_step.shape[0]-1):
#     for j in range(lat_step.shape[0]-1):
#         #set the local coordinates&velocity
#         print('计算经度：',lon_step[i],'-',lon_step[i+1],'纬度',lat_step[j],'-',lat_step[j+1])
#         fuc.local_data_set(lon_step[i],lon_step[i+1],lat_step[j],lat_step[j+1])
#         #Judge whether it is land or not
#         if ((np.max(abs(glo.local_u[:,:])<glo.island_tol)and(np.max(abs(glo.local_v[:,:])<glo.island_tol)))):
#             print('此区域为陆地')
#         else:
#             eddy_lon,eddy_lat,eddy_C,eddy_R,eddyornot=GA.GA(nind,maxgen,lon_step[i],lon_step[i+1],lat_step[j],lat_step[j+1])
#             if((eddyornot==1)and(eddy_C<C_tol)):
#                 print(eddy_lon,eddy_lat,eddy_C,eddy_R)
#                 eddy_record=np.append(eddy_record,[eddy_lon,eddy_lat,eddy_C,eddy_R,glo.clockwise])

# #half_step
# for i in range(lon_half_step.shape[0]-1):
#     for j in range(lat_half_step.shape[0]-1):
#         #set the local coordinates&velocity
#         print('计算经度：',lon_half_step[i],'-',lon_half_step[i+1],'纬度',lat_half_step[j],'-',lat_half_step[j+1])
#         fuc.local_data_set(lon_half_step[i],lon_half_step[i+1],lat_half_step[j],lat_half_step[j+1])
#         #Judge whether it is land or not
#         if ((np.max(abs(glo.local_u[:,:])<0.0001)and(np.max(abs(glo.local_v[:,:])<0.0001)))):
#             print('此区域为陆地')
#         else:
#             eddy_lon,eddy_lat,eddy_C,eddy_R,eddyornot=GA.GA(nind,maxgen,lon_half_step[i],lon_half_step[i+1],lat_half_step[j],lat_half_step[j+1])
#             if(eddyornot==1):
#                 print(eddy_lon,eddy_lat,eddy_C,eddy_R)
#                 eddy_record=np.append(eddy_record,[eddy_lon,eddy_lat,eddy_C,eddy_R,glo.clockwise])

# In[ ]:


#write the identification result into a csv file named data
eddy=eddy_record
k=eddy.shape[0]/5
eddy=eddy.reshape((int(k),5))
out = open('data.csv','a', newline='')
#设定写入模式
csv_write = csv.writer(out,dialect='excel')
#写入具体内容
csv_write.writerows(eddy)
out.close()


# In[ ]:


fig=plt.figure(figsize=(50,50))
ax=plt.subplot(projection=ccrs.PlateCarree())
ax.coastlines('50m',linewidth=20)
ax.add_feature(cfeature.LAND,alpha=1, color='')
ax.set_extent([glo.search_lon[0], glo.search_lon[glo.search_lon.shape[0]-1]
                , glo.search_lat[0], glo.search_lat[glo.search_lat.shape[0]-1]]
               , ccrs.PlateCarree())
ax.grid(True, linestyle='-.')
#ax0.streamplot(X, Y, U, V, density=5, color='k', linewidth=1)

for i in range(eddy[1:,0].shape[0]):
    if(eddy[1+i,4]==1):
        cir1 = plt.Circle(xy = (eddy[1+i,0], eddy[1+i,1]), radius=eddy[1+i,3]**0.5, alpha=0.7,color='g')
        ax.add_patch(cir1)
    else:
        cir1 = plt.Circle(xy = (eddy[1+i,0], eddy[1+i,1]), radius=eddy[1+i,3]**0.5, alpha=0.7,color='y')
        ax.add_patch(cir1)
        
ax.quiver(X, Y, U, V)#,width=0.0005)
foo_fig = plt.gcf() # 'get current figure'
foo_fig.savefig('result.eps', format='eps', dpi=1000)
plt.show()

