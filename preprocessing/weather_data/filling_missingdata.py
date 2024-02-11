#!/usr/bin/env python
# coding: utf-8

# In[7]:


#importing useful libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

pd.options.mode.chained_assignment = None  # default='warn'


# In[8]:


#read weather data 
data = pd.read_csv('1yearData.csv',usecols=[0,1,2,7,9,12])
data.rename(columns={'District Name':'District','Current Date':'Date'}, inplace = True)
data.head(10)


# In[9]:


#distance between two districts
distance= pd.read_csv('Distance.csv')
distance.head(10)
distance.drop(distance.index[distance['Distance'] == 0], inplace=True)


# In[10]:


dist = distance.groupby(['Origin'])['Distance'].apply(lambda x: x.nsmallest(3))
distance = distance.merge(dist,on='Origin',suffixes=('','_mindist'))
distance = distance[distance.Distance==distance.Distance_mindist].drop('Distance_mindist', axis=1)


# In[11]:


def calc_hum(i,dict,idx):
    fetch_val = dest_dict[idx][1]
    time = data['timestamp'][i]
    rel_hum = data[(data["timestamp"]==time) & (data["District"] == fetch_val)]["relative_humidity"]
    rel_list = []
    rel_list = rel_hum.values.tolist()
    return rel_list


# In[ ]:


data['relative_humidity'].fillna(0,inplace=True)

indices = list(np.where(data["relative_humidity"]==0)[0])

for i in indices:
    distr = data['District'][i]
    dest_dict = list(zip(distance['Distance'][distance['Origin'] == distr], distance['Destination'][distance['Origin'] == distr]))
    dest_dict = sorted(dest_dict,key=lambda l:l[1])
    rel1_hum = calc_hum(i,dest_dict,0)

    if(rel1_hum == 0):
        rel1_hum = []
        rel1_hum = calc_hum(i,dest_dict,1)
 
        if(rel1_hum == 0):
            rel1_hum = []
            rel1_hum = calc_hum(i,dest_dict,2)
   
            if(rel1_hum == 0):
                rel1_hum = []
                rel1_hum = 0.0
    
    if len(rel1_hum)> 0:
        data["relative_humidity"][i] = rel1_hum[0]


# In[ ]:


data.to_csv("out.csv", encoding='utf-8')


# In[ ]:




