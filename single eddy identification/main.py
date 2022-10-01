
# coding: utf-8

# In[ ]:


import geatpy as ga
import numpy as np
# 获取函数接口地址
AIM_M = __import__('aimfuc')
PUN_M = __import__('punishing')
"""============================变量设置============================"""
ox = [284,286]  # 自变量1的范围  lon的范围
oy = [31,34]  # 自变量2的范围    lat的范围
C = [1, 10]  # 自变量3的范围
R = [0.1, 4]  # 自变量3的范围
b1 = [1, 1]  # 自变量1是否包含下界
b2 = [1, 1]  # 自变量2是否包含上界
b3 = [1, 1]  # 自变量3是否包含下界
b4 = [1, 1]  # 自变量4是否包含上界
precisions = [1, 1]  # 在二进制/格雷码编码中代表自变量的编码精度，当控制变量是二进制/格雷编码时，该参数可控制编码的精度
ranges = np.vstack([ox,oy,C,R]).T  # 生成自变量的范围矩阵
borders = np.vstack([b1, b2,b3,b4]).T  # 生成自变量的边界矩阵
# 生成区域描述器
FieldD = ga.crtfld(ranges, borders, precisions)
"""========================遗传算法参数设置========================="""
NIND = 100  # 种群规模
MAXGEN = 500  # 最大遗传代数
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
[ObjV, NDSet, NDSetObjV, times] = ga.moea_nsga2_templet(AIM_M=AIM_M, AIM_F="aimfuc", PUN_M=None,PUN_F=None,
                                                        FieldDR=FieldD, problem="R", maxormin=1, MAXGEN=MAXGEN,
                                                        MAXSIZE=MAXSIZE, NIND=NIND, SUBPOP=SUBPOP, GGAP=GGAP,
                                                        selectStyle=selectStyle, recombinStyle=recombinStyle,
                                                       recopt=recopt, pm=pm, distribute=True, drawing=1)#PUN_M=PUN_M, PUN_F="punishing",



index_output=np.where((ObjV[:,0]/ObjV[:,1]<1.2)&(ObjV[:,0]/ObjV[:,1]>0.8))

print('涡心为：   lon:',np.mean(NDSet[:,0]),
                            'lat:',np.mean(NDSet[:,1]),
                            '\nC:',np.mean(NDSet[:,2]),
                            '\nR:',np.mean(NDSet[:,3]))
print('涡心为：   lon:',np.mean(NDSet[index_output,0]),
                            'lat:',np.mean(NDSet[index_output,1]),
                            '\nC:',np.mean(NDSet[index_output,2]),
                            '\nR:',np.mean(NDSet[index_output,3]))

