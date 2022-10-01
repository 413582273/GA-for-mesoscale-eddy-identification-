
# coding: utf-8

# In[ ]:


import numpy
import glovar as glo


# In[ ]:


def readvel(lon_start,lon_end,lat_start,lat_end):
    #get the array index 
    index_lon_start=np.max(np.where(glo.global_lon<=lon_start))
    index_lon_end=np.min(np.where(glo.global_lon>=lon_start))
    index_lat_start=np.max(np.where(glo.global_lat<=lat_start))
    index_lat_end=np.min(np.where(glo.global_lat>=lat_start))
    #get the range of the index
    range_lon=np.arange(index_lon_start,index_lon_end,1)
    range_lat=np.arange(index_lat_start,index_lat_end,1)
    #get the velocity data
    U=glo.global_u[range_lat,range_lon]
    V=glo.global_u[range_lat,range_lon]
    return U,V

