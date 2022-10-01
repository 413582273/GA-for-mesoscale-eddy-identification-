
# coding: utf-8

# In[1]:


import numpy as np


def punishing(LegV, FitnV):
    FitnV[np.where(LegV == 0)[0]] = np.min(FitnV) * 0.1  # 对非可行解严厉惩罚
    return FitnV

