
# coding: utf-8

# In[ ]:


"""
本程序利用数据库的数据对动力系统进行拟合
利用get_v_field文件进行数据获取
利用geatpy库进行遗传算法拟合参数

需要拟合的模型参见中尺度涡动力系统模型一文

算法教程见https://github.com/geatpy-dev/geatpy/blob/master/geatpy/doc/Geatpy-tutorials/2.quickstart.pdf

"""


# In[ ]:


import numpy as np
import geatpy as ga # 导入geatpy库
import matplotlib.pyplot as plt
import time
import get_v_field_function as gvf #自己的函数库

import glovar as glo


# In[ ]:


data1=glo.Data(glo.track_n)
U=data1.u
V=data1.v
X=data1.X
Y=data1.Y
cyc=data1.cyc


# In[ ]:


#完整模型
def aimfuc(Phen,LegV):
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
            fx=U[j][i]-(lamda*(Y[j]-oy)+alfa*(X[i]-ox)*(a*(X[i]-ox)**2+b*(Y[j]-oy)**2-R)**2)#
            fy=V[j][i]-(-mu*(X[i]-ox)+beta*(Y[j]-oy)*(a*(X[i]-ox)**2+b*(Y[j]-oy)**2-R)**2)#
            fucx=fx**2+fucx
            fucy=fy**2+fucy
    return[np.vstack([fucx, fucy]).T,LegV]

