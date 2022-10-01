
# coding: utf-8

# In[ ]:


import glovar as glo
import numpy as np


# In[ ]:


#Modify the search area
#input the eddy parameter, output regional coordinates
def locmod(R,lon,lat):
    lon_start=lon-R
    lon_end=lon+R
    lat_start=lat-R
    lat_end=lat+R
    return lon_start,lon_end,lat_start,lat_end


# In[ ]:


#Generlize search step
#input search accuracy(global var),search area ,output search grid data
def search_step():
    lon_mod=(glo.lon_end-glo.lon_start)%glo.acc #取模
    lat_mod=(glo.lat_end-glo.lat_start)%glo.acc
    lon_step=np.arange(glo.lon_start,glo.lon_end-lon_mod+glo.acc,glo.acc)
    lat_step=np.arange(glo.lat_start,glo.lat_end-lat_mod+glo.acc,glo.acc)
    #in order to ensure a detailed search result ，we use cross Staggered grid method
    lon_half_step=np.arange(glo.lon_start+glo.acc/2,glo.lon_end-lon_mod-glo.acc/2,glo.acc)
    lat_half_step=np.arange(glo.lat_start+glo.acc/2,glo.lat_end-lat_mod-glo.acc/2,glo.acc)
    return lon_step,lat_step,lon_half_step,lat_half_step


# In[ ]:


#set the local coordinates&velocity
#input original single calculating grid range,output the local calculating grid
def local_data_set(orilon_start,orilon_end,orilat_start,orilat_end):
    #get the index
    index_lon_start=np.max(np.where(glo.global_lon<=orilon_start))
    index_lon_end=np.min(np.where(glo.global_lon>=orilon_end))
    
    index_lat_start=np.max(np.where(glo.global_lat<=orilat_start))
    index_lat_end=np.min(np.where(glo.global_lat>=orilat_end))
    
    glo.local_lon=glo.global_lon[index_lon_start:index_lon_end+1]
    glo.local_lat=glo.global_lat[index_lat_start:index_lat_end+1]
    
    glo.local_u=glo.global_u[index_lat_start:index_lat_end+1,index_lon_start:index_lon_end+1]
    glo.local_v=glo.global_v[index_lat_start:index_lat_end+1,index_lon_start:index_lon_end+1]
    
    
    #print('实际计算经度：',glo.global_lon[index_lon_start],'-',glo.global_lon[index_lon_end],
     #     '纬度',glo.global_lat[index_lat_start],'-',glo.global_lat[index_lat_end])
    return 

