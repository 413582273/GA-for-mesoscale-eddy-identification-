
# coding: utf-8

# In[ ]:


"""
This program is designed for parameter estimation of dynamic system ,
using the Geatpy to accomplish the GA algorithm.

The module describes the aim function of the parameter estimation problem.

Algorithm's details see also 
https://github.com/geatpy-dev/geatpy/blob/master/geatpy/doc/Geatpy-tutorials/2.quickstart.pdf

"""


# In[ ]:


import numpy as np
import geatpy as ga #Import GA algorithm
import glovar as glo #Import global variables


# In[ ]:


#新模型Defination of the aim function
def aimfuc(Phen,LegV):
    #Get the values of global variables
    U=glo.local_u
    V=glo.local_v
    X=glo.local_lon
    Y=glo.local_lat
    ox=Phen[:,0]
    oy=Phen[:,1]
    R=Phen[:,2]
    lamda=Phen[:,3]
    mu=Phen[:,4]
    alfa=Phen[:,5]
    beta=Phen[:,6]
    a=Phen[:,7]
    b=Phen[:,8]
    fucx=0
    fucy=0
    for i in range(X.shape[0]):
        for j in range(Y.shape[0]):
            fx=U[j][i]-(lamda*(Y[j]-oy)+alfa*(X[i]-ox)*(a*(X[i]-ox)**2+b*(Y[j]-oy)**2-R)**2)
            fy=V[j][i]-(-mu*(X[i]-ox)+beta*(Y[j]-oy)*(a*(X[i]-ox)**2+b*(Y[j]-oy)**2-R)**2)
            fucx=fx**2+fucx
            fucy=fy**2+fucy
    return[np.vstack([fucx, fucy]).T,LegV]


# #老模型Defination of the aim function
# def aimfuc(Phen,LegV):
#     #Get the values of global variables
#     U=glo.local_u
#     V=glo.local_v
#     X=glo.local_lon
#     Y=glo.local_lat
#     ox=Phen[:,0]
#     oy=Phen[:,1]
#     C=Phen[:,2]
#     R=Phen[:,3]
#     fucx=0
#     fucy=0
#     for i in range(X.shape[0]):
#         for j in range(Y.shape[0]):
#             fx=U[j][i]-glo.clockwise*((Y[j]-oy)-(X[i]-ox)*((X[i]-ox)**2+(Y[j]-oy)**2-R))/C
#             fy=V[j][i]-glo.clockwise*(-(X[i]-ox)-(Y[j]-oy)*((X[i]-ox)**2+(Y[j]-oy)**2-R))/C
#             fucx=fx**2+fucx
#             fucy=fy**2+fucy
#     return[np.vstack([fucx, fucy]).T,LegV]
