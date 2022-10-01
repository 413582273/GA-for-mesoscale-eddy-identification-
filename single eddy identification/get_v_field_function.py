
# coding: utf-8

# In[ ]:


"""
函数说明

eddyinfo(track_number)
从中尺度涡数据库中获取需要跟踪的中尺度涡的坐标等信息
输入涡的辨识号  输出涡信息数组

lon_trans(input)
经度转换  输入中尺度涡数据库的经度 
参考http://wombat.coas.oregonstate.edu/eddies/data.html的注释

L_to_location(track_num)
半径和对应的度数范围转换  按照1度 112千米计算（粗略估计）
输入涡的识别号  输出ecco2中的对应坐标数组

get_eddy_time_index(track_number)
输入涡的识别号  获得流场数据库对应时刻的数组index

Jdate_trans(y,d,m)
儒略历转换 输入年月日
算法见https://baike.baidu.com/item/%E5%84%92%E7%95%A5%E6%97%A5/693474?fr=aladdin

get_vel_field(track_num,index)
从ecco2数据库中获取速度场数据  输入涡的识别号 

gen_pic(track_num)
输入涡识别号 生成提取的速度场图像

"""


# In[ ]:


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import csv
from datetime import datetime
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
import pprint
import seawater as sw
import sys
import time as tm

import glovar as glo


# In[ ]:


#读取中尺度涡数据库
dataset =Dataset('tracks_AVISO_DT2014_daily_web.nc')  # open the dataset
L=dataset.variables['L']
U=dataset.variables['U']
A=dataset.variables['A']
lat=dataset.variables['lat']
lon=dataset.variables['lon']
cyc=dataset.variables['cyc']
track=dataset.variables['track']
n=dataset.variables['n']
j1=dataset.variables['j1']


# In[ ]:


#读取流场数据库   
dataset_uvel =Dataset('http://apdrc.soest.hawaii.edu:80/dods/public_data/ECCO/ECCO2/cube92/uvel')
dataset_vvel =Dataset('http://apdrc.soest.hawaii.edu:80/dods/public_data/ECCO/ECCO2/cube92/vvel')    #打开数据文件
u=dataset_uvel.variables['uvel']
v=dataset_vvel.variables['vvel']
time=dataset_uvel.variables['time']
lat_f=np.array(dataset_uvel.variables['lat'])
lon_f=np.array(dataset_uvel.variables['lon'])


# In[ ]:


def eddyinfo(track_number):
#定义函数 从中尺度涡数据库中获取需要跟踪的中尺度涡的坐标等信息    
#筛选气旋反气旋涡   -1气旋 1反气旋
#筛选经度纬度
    output=np.zeros(9)
    index_func=np.where((n[:]==1)&(track[:]==track_number))  #选择了涡刚探测到时候的状态
    output[0]=lat[index_func[0]]
    output[1]=lon[index_func[0]]
    output[2]=j1[index_func[0]]
    output[3]=L[index_func[0]]
    output[4]=U[index_func[0]]
    output[5]=A[index_func[0]]
    output[6]=cyc[index_func[0]]
    output[7]=track[index_func[0]]
    output[8]=n[index_func[0]]
    return output


# In[ ]:


def lon_trans(input):
    #   经度转换  输入中尺度涡数据库的经度 参考http://wombat.coas.oregonstate.edu/eddies/data.html的注释
    
    #   lon, lat are the longitude and latitude of the centroid of the eddy at each of 
    #   the n points along the eddy track. In order to avoid jumps of ~360° in eddy tracks 
    #   when the trajectory wraps around a longitude branch point that might lie in a region of interest, 
    #   the longitude domain is set to 260°E-650°E. This range was selected so that the only eddy trajectories 
    #   that might still be affected will be those passing through the Drake Passage. In latitude, 
    #   the domain extends from 80°S-80°N
    #
    if(input<=360)&(input>=0):
        output=input
    elif(input>360):
        output=input-360
    elif(input<0):
        output=input+360
    return output


# In[ ]:


def L_to_location(track_num):#(R_input,eddycore_lat,eddycore_lon):
    #   半径和对应的度数范围转换  按照1度 112千米计算（粗略估计）
    #   输入涡的识别号  输出ecco2中的对应坐标数组
    e_info=eddyinfo(track_num)
    eddycore_lat=e_info[0]
    eddycore_lon=e_info[1]
    R_input=1.1*e_info[3]
    output1=np.zeros(4)  #lon start end 01     lat start end 23
    output=np.arange(8)
    R=R_input/112
    output1[0]=lon_trans(eddycore_lon-R)
    output1[1]=lon_trans(eddycore_lon+R)
    output1[2]=eddycore_lat-R
    output1[3]=eddycore_lat+R
    print('涡心坐标    lat：',eddycore_lat,'lon：',eddycore_lon)
    print('半径L=',R_input,'转换为度数：',R)
    print('涡的坐标范围lat: ',output1[2],output1[3],' lon:',output1[0],output1[1])
    #寻找匹配ecco2中的坐标
    output[0]=np.max(np.where((lon_f<=output1[0])))
    output[1]=np.min(np.where((lon_f>=output1[1])))
    if(output1[2]>0):
        output[2]=np.max(np.where((lat_f<=output1[2])))
        output[3]=np.min(np.where((lat_f>=output1[3])))
    else:
        output[2]=np.min(np.where((lat_f>=output1[2])))
        output[3]=np.max(np.where((lat_f<=output1[3])))
    
    output[4]=output1[0]
    output[5]=output1[1]
    output[6]=output1[2]
    output[7]=output1[3]
        
    print('对应坐标起止lat:',lat_f[output[2]],lat_f[output[3]],' lon:',lon_f[output[0]],lon_f[output[1]])
    print('对应数组起止lat: ',output[2],output[3],' lon:',output[0],output[1])
    return output


# In[ ]:


def get_eddy_time_index(track_number):
    #输入涡的识别号  获得流场数据库对应的时刻
    date=eddyinfo(track_number)[2]  #获得中尺度涡数据库的时间
    #时间转换 http://apdrc.soest.hawaii.edu/dods/public_data/ECCO2/cube92/uvel
    
    #流场数据库,起始时间为00z01jan1992,对应数组的值为727200 
    #与中尺度涡数据库起始时间2448623
    #两者相差2448623-727200=1721423
    #则流场数据库的时间有如下转换
    date1=date-1721423-366
    
    date_index=np.max(np.where(time<=date1)) #在流场数据库中筛选出对应时间点
    print('\n选择了中尺度涡数据库的Julian时间为',date,'转换后为',date1,
          '\n对应流场观测的时间点为',time[date_index],'数组索引为',date_index)
    return date_index


# In[ ]:


def Jdate_trans(y,d,m):  #儒略历转换 输入年月日
    #算法见https://baike.baidu.com/item/%E5%84%92%E7%95%A5%E6%97%A5/693474?fr=aladdin
    JDN=d+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-32083
    return JDN


# In[ ]:


def get_vel_field(track_num,index):
    #从ecco2数据库中获取速度场数据  输入涡的识别号  index=1为u
    print('————————————————获取速度场————————————————')
    location=L_to_location(track_num)
    range_lon=np.arange(location[0],location[1],1)
    range_lat=np.arange(location[2],location[3],1)
    range_lon=range_lon.tolist()
    range_lat=range_lat.tolist()
    date=get_eddy_time_index(track_num)
    if (index==1):
        output=u[date,1,range_lat,range_lon]
        print('———————————————获取速度U完毕————————————————\n\n')
    else:
        output=v[date,1,range_lat,range_lon]
        print('———————————————获取速度V完毕————————————————\n\n')
    return output


# In[ ]:


def gen_pic(track_num):  #生成提取的速度场图像
    #获取速度场
    vx=get_vel_field(track_num,1)
    vy=get_vel_field(track_num,0)
    #获取坐标的数组范围
    loc_range=L_to_location(track_num)
    #生成网格
    X,Y=np.meshgrid(lon_f[loc_range[0]:loc_range[1]],lat_f[loc_range[2]:loc_range[3]])  #参见函数L_to_location
    
    print('\n————————网格生成成功，大小为：',X.shape,'————————')
    
    fig, ax = plt.subplots()
    q = ax.quiver(X, Y, vx, vy)
    ax.quiverkey(q, X=0.3, Y=1.1, U=10,label='Quiver key, length = 10', labelpos='E')
    print('\n————————绘图完毕————————')
    plt.show()
    return

