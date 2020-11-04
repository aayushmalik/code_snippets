#!/usr/bin/env python
# coding: utf-8

# In[108]:


import pandas as pd
import numpy as np


# In[109]:


df = pd.read_excel('2015riversdatacleaned.xlsx', sheet_name = 'Sheet2')


# In[110]:


df['temp_avg'] = (df['min_temp'] + df['max_temp'])/2
df['do_avg'] = (df['dissolved_oxygen_min'] + df['dissolved_oxygen_max'])/2
df['ph_avg'] = (df['ph_min'] + df['ph_max'])/2
df['conductivity_avg'] = (df['conductivity_min'] + df['conductivity_max'])/2
df['bod_avg'] = (df['bod_min'] + df['bod_max'])/2
df['fc_avg'] = (df['fc_min'] + df['fc_max'])/2


# In[111]:


def calculate_do_index(temp, do):
    '''this function returns the DO index for the input value of average temperature, and average do'''
    docp = ((np.exp(7.7117-1.31403*np.log10(temp+45.93))) * 1 * (1-np.exp(11.8571-(3840.7/(temp+273.15))-(216961/((temp+273.15)**2)))/1)* (1-(0.000975-(0.00001426*temp)+(0.00000006436*(temp**2)))*1))/ (1-np.exp(11.8571-(3840.7/(temp+273.15))-(216961/((temp+273.15)**2))))/ (1-(0.000975-(0.00001426*temp)+(0.00000006436*(temp**2))))
    dosp = 100*do/docp
    if dosp < 40:
        return dosp * 0.66 + 0.18
    elif (dosp > 40) & (dosp < 100):
        return -13.55+1.17 * dosp
    else:
        return 163.34-0.62*dosp


# In[112]:


def calculate_bod_index(value):
    '''this function returns the value of BOD index for the input value of average BOD'''
    if value <= 10:
        return 96.67 - 7 * value
    elif (value > 10) & (value < 30):
        return 38.9 - 1.23 * value
    else:
        return 2


# In[113]:


def calculate_ph_index(value):
    '''this function returns the value of pH index for the input value of average pH'''
    if value < 2:
        return 0
    elif (value > 2) & (value < 5):
        return 16.1 + 7.35*value
    elif (value > 5) & (value < 7.3):
        return -142.67 + 33.5*value
    elif (value > 7.3) & (value < 10):
        return 316.96 - 29.85*value
    elif (value < 12) & (value > 10):
        return 96.17 - 8*value
    else:
        return 0


# In[114]:


def calculate_fc_index(value):
    '''this function returns the value of FC index for the input value of average faecal coliform'''
    if (value > 1) & (value < 172):
        return 97.2 - 26.6*np.log10(value)
    elif (value > 1000) & (value < 100000):
        return 42.33-7.75*np.log10(value)
    else:
        return 2


# In[115]:


def calculate_wqi(do, bod, ph, fc):
    '''this function returns wqi for the input values of do, bod, ph, and fc'''
    return do*0.31 + bod*0.19 + ph*0.22 + fc*0.28


# In[116]:


def check_drinking_safe(do, bod, ph, fc):
    '''this function takes the value of ph, do, bod, and tc and returns 1 if the water is safe'''
    if (do >= 3) & (bod >= 2) & (fc <= 50) & (ph >= 6.5) & (ph <= 8.5):
        return 1
    else:
        return 0


# In[117]:


def check_bathing_safe(do, bod, ph, fc):
    '''this function takes the value of ph, do, bod, and tc and returns 1 if the water is safe'''
    if (do <= 5) & (bod >= 3) & (fc >= 5000) & (ph <=8.5) & (ph >= 6.5):
        return 1
    else:
        return 0


# In[118]:


def check_industrial_safe(ph, ec):
    '''this function takes the value of ph, and ec returns 1 if the water is safe'''
    if (ph >= 6) & (ph <= 8.5) & (ec <= 2250):
        return 1
    else:
        return 0


# In[119]:


df['ph_index'] = df.ph_avg.apply(calculate_ph_index)
df['fc_index'] = df.fc_avg.apply(calculate_fc_index)
df['bod_index'] = df.bod_avg.apply(calculate_bod_index)
df['do_index'] = df.apply(lambda x: calculate_do_index(x.temp_avg, x.do_avg), axis=1)


# In[120]:


df['drinking_safe'] = df.apply(lambda x: check_drinking_safe(x.do_avg, x.bod_avg, x.ph_avg, x.fc_avg), axis = 1)
df['bathing_safe'] = df.apply(lambda x: check_bathing_safe(x.do_avg, x.bod_avg, x.ph_avg, x.fc_avg), axis = 1)
df['industrial_safe'] = df.apply(lambda x: check_industrial_safe(x.ph_avg, x.conductivity_avg), axis = 1)


# In[121]:


df['wqi'] = df.apply(lambda x: calculate_wqi(x.do_index, x.bod_index, x.ph_index, x.fc_index), axis = 1)


# In[122]:


df.to_csv('2015_indices.csv', index=None)


# In[ ]:




