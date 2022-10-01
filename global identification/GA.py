
# coding: utf-8

# In[ ]:


import geatpy as ga
import numpy as np
import glovar as glo
from moea_nsga2_templet1 import moea_nsga2_templet1


# In[ ]:


def GA(nind,maxgen,lon_start,lon_end,lat_start,lat_end):
    # 获取函数接口地址
    AIM_M = __import__('aimfuc')
    PUN_M = __import__('punishing')
    """============================变量设置============================"""
    ox = [lon_start,lon_end]  # 自变量1的范围  lon的范围
    oy = [lat_start,lat_end]  # 自变量2的范围    lat的范围
    R = [0.1,4 ]  # 自变量3的范围
    alfa = [-3, 3]  # 自变量3的范围
    beta = [-3, 3]  # 自变量3的范围
    a = [0.1, 4]  # 自变量3的范围
    b = [0.1, 4]  # 自变量3的范围
    lamda = [0.1, 10]  # 自变量3的范围
    mu = [0.1, 10]  # 自变量3的范围
    b1 = [1, 1]  # 自变量1是否包含下界
    b2 = [1, 1]  # 自变量2是否包含上界
    b3 = [1, 1]  # 自变量3是否包含下界
    b4 = [1, 1]  # 自变量4是否包含上界
    b5 = [1, 1]  # 自变量4是否包含上界
    b6 = [1, 1]  # 自变量4是否包含上界
    b7 = [1, 1]  # 自变量4是否包含上界
    b8 = [1, 1]  # 自变量4是否包含上界
    b9 = [1, 1]  # 自变量4是否包含上界
    precisions = [1, 1]  # 在二进制/格雷码编码中代表自变量的编码精度，当控制变量是二进制/格雷编码时，该参数可控制编码的精度
    ranges = np.vstack([ox,oy,R,alfa,beta,a,b,lamda,mu]).T  # 生成自变量的范围矩阵
    borders = np.vstack([b1,b2,b3,b4,b5,b6,b7,b8,b9]).T  # 生成自变量的边界矩阵
    # 生成区域描述器
    FieldD = ga.crtfld(ranges, borders, precisions)
    """========================遗传算法参数设置========================="""
    NIND = glo.nind  # 种群规模
    MAXGEN = glo.maxgen  # 最大遗传代数
    MAXSIZE = 200  # 最大帕累托前沿数
    GGAP = 0.8  # 代沟：子代与父代的重复率为(1-GGAP)
    selectStyle = 'rws'  # 遗传算法的选择方式设为"rws"——轮盘赌选择
    recombinStyle = 'xovdp'  # 遗传算法的重组方式，设为两点交叉
    recopt = 0.9  # 交叉概率
    pm = 0.1  # 变异概率
    SUBPOP = 1  # 设置种群数为1
    maxormin = 1  # 设置标记表明这是最小化目标
    """=======================调用编程模板进行种群进化==================="""
    # 调用编程模板进行种群进化，得到种群进化和变量的追踪器以及运行时间
    [ObjV, NDSet, NDSetObjV, times] = moea_nsga2_templet1(AIM_M=AIM_M, AIM_F="aimfuc", PUN_M=PUN_M, PUN_F="punishing",
                                                            FieldDR=FieldD, problem="R", maxormin=1, MAXGEN=MAXGEN,
                                                            MAXSIZE=MAXSIZE, NIND=NIND, SUBPOP=SUBPOP, GGAP=GGAP,
                                                            selectStyle=selectStyle, recombinStyle=recombinStyle,
                                                            recopt=recopt, pm=pm, distribute=True, drawing=0)
    lon=np.mean(NDSet[:,0])
    lat=np.mean(NDSet[:,1])
    R1=np.mean(NDSet[:,2])
    alfa=np.mean(NDSet[:,3])
    beta=np.mean(NDSet[:,4])
    a=np.mean(NDSet[:,5])
    b=np.mean(NDSet[:,6])
    lamda=np.mean(NDSet[:,7])
    mu=np.mean(NDSet[:,8])
    return lon,lat,R1**0.5,alfa,beta,a,b,lamda,mu,np.mean(np.abs(NDSetObjV[:,0])+np.abs(NDSetObjV[:,1])),lon_start,lon_end,lat_start,lat_end

