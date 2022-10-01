
# coding: utf-8

# In[ ]:


"""
This module is designed for global variables, therefore every 
other .py files can get the basic configuration data such as 
search range, search accuracy, etc.
"""
import numpy
import get_v_field_function as gvf


# In[ ]:


"""Global Constants"""


# In[ ]:


#set search range, the unit is degree
time="time"
lon_start="lon_start"
lon_end="lon_end"
lat_start="lat_start"
lat_end="lat_end"
#set search accuracy, the unit is degree
acc="acc"
#identification tolerance
iden_tol="inden_tol"
#clockwise=1 anti clockwise=-1
clockwise="clockwise"
#tolerance level of the island
island_tol="island_tol"
C_tol="C_tol"

#GA
nind="nind"
maxgen="maxgen"

track_n="track_n"


# In[ ]:


"""Global Variables"""


# In[ ]:


#set local&global velocity variables
#for convenience，u v should depend only on lon&lat，without time
local_u="local_u"
local_v="local_v"
local_lon="local_lon"
local_lat="local_lat"
global_u="global_u"
global_v="global_v"
global_lon="global_lon"
global_lat="global_lat"
search_lon="search_lon"
search_lat="search_lat"


# In[ ]:


class Data:
    '海洋数据的基类'
    track=0
    def __init__(self,track):
        #涡的标号
        self.track_num=track
        #速度场属性
        self.u=gvf.get_vel_field(track,1)
        self.v=gvf.get_vel_field(track,0)
        #区域大小
        self.Xdata_size=self.u.shape[1]
        self.Ydata_size=self.u.shape[0]
        #区域网格
        #self.X=self.u
        #self.Y=self.u
        self.X=gvf.lon_f[gvf.L_to_location(track)[0]:gvf.L_to_location(track)[1]]
                                   #参见函数L_to_location
        self.Y=gvf.lat_f[gvf.L_to_location(track)[2]:gvf.L_to_location(track)[3]]
        self.lat=gvf.eddyinfo(track)[0]
        self.lon=gvf.eddyinfo(track)[1]
        self.j1=gvf.eddyinfo(track)[2]
        self.L=gvf.eddyinfo(track)[3]
        self.U=gvf.eddyinfo(track)[4]
        self.A=gvf.eddyinfo(track)[5]
        self.cyc=gvf.eddyinfo(track)[6]
        self.track=gvf.eddyinfo(track)[7]
        self.n=gvf.eddyinfo(track)[8]
        print('数据对象创建成功')

