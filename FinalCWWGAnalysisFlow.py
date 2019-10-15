#!/usr/bin/env python
# coding: utf-8

#importing the relevant libraries for analysis

import pandas as pd
import numpy as np
import datetime as dt


# In[2]:


#the location is dropbox in usage data, samyam updates it weekly
path = '/path/to/the/file'
df = pd.read_stata(path)


# In[3]:


#ensure that the block variable is there
#sometimes the mobile is written as number, make a consistency in that
df = df[['name','number', 'date', 'tag0', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'district', 'block']]


# In[4]:


df.date = pd.to_datetime(df.date) #to select the subset of dates


# In[5]:


#this should be run on only monday so that we have call records from previous friday to the gone friday, because data gets updated on friday and meeting is on monday
#if anything changes, plan to change the date accordingly

start_date = pd.to_datetime(dt.datetime.now() - dt.timedelta(days = 10)) #timedelta to get to the date we need
end_date = pd.to_datetime(dt.datetime.now() - dt.timedelta(days = 3)) 
df = df[(df['date'] > start_date) & (df['date'] < end_date)] #use & and not 'and'


# In[6]:


#it's better to run this command first to know any typos or mistyping or some facts about the data and then carry out the next cell which is for cleaning
for i in range(6):
    a = 'tag'+ str(i)
    print('='*10,a)
    print(df[a].value_counts())


# In[7]:


#data cleaning
#if the systems are following the necessary protocols, then eventually there will be no need to run the last three commands in this cell
df = df[pd.notnull(df['tag0'])]
df = df[~df.tag0.str.startswith('0')]
df = df[~df.tag0.str.startswith('.')]
df.replace('panicle intiation', '4.panicle initiation', inplace=True)
df.replace('leaf yellowing in paddy', '4.leaf yellowing in paddy', inplace=True)
df.replace('leaf roller', '4.leaf roller', inplace=True)


# In[8]:


#remember to join df because after the below written command name number district and date will get lost from the original dataset so make a new df and then join them to get a complete picture
#this was made so that it can be joined after performing the stacking operation described below
#important to do this before carrying the next step
ddf = df[['number','date','district','block', 'name']]


# In[9]:


df = df.stack().to_frame('a').reset_index(level=1, drop=True).reset_index()
df['b'] = df['a'].str.split('.').str[0]
d = {'1': 'season', '2': 'crop', '3': 'maintopic', '4':'subtopic','5':'issue'}

df = df.pivot_table(index='index',columns='b',values='a', aggfunc=','.join).rename(columns=d).rename_axis(None, axis=1).rename_axis(None)


# In[10]:


#removing all other irrelevant columns
df = df[['season', 'crop', 'maintopic', 'subtopic', 'issue']]


# In[11]:


merged = df.join(ddf) #to join the ddf and df so that the variables we isolated before can be used with this
merged = merged[merged.maintopic == '3.pest and disease management'] #we only need pest and disease information
merged.drop('maintopic', axis=1, inplace=True) #because then main topic will only be pest and disease so better to clear it


# In[12]:


final_df = pd.DataFrame(merged.groupby(['district','block','crop']).subtopic.value_counts())
final_df.rename(columns={'subtopic':'#'}, inplace=True) #changing name of the column
final_df.reset_index(inplace = True) #to convert multiindex to columns


# In[14]:


get_ipython().run_cell_magic('capture', 'cap', "for district in final_df.district.value_counts().head(5).index:\n    print('='*10,district,'='*10)\n    temp = final_df[final_df.district == district]\n    #this writes the block crop issue and count for the top districts\n    print(temp.groupby(['block', 'crop']).subtopic.value_counts())\n    #this shows the main issues from the above five districts\n    print(temp.groupby(['district']).subtopic.value_counts())\n    \nwith open('pest_n_disease.txt', 'w') as f:\n    f.write(cap.stdout)")





