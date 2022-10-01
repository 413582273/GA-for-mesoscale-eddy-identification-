
# coding: utf-8

# In[ ]:


"""
This module is designed for global variables, therefore every 
other .py files can get the basic configuration data such as 
search range, search accuracy, etc.
"""
import numpy


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

