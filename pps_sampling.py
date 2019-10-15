# this code is used to perform pps sampling in python
# visit https://medium.com/@chaayushmalik/pps-sampling-in-python-b5d5d4a8bdf7 for detailed information

import pandas as pd
import numpy as np

df = pd.read_csv('filename.csv')

total = df['Total'].sum()
sample_size = 81 #number of samples to be selected
interval_width = int(total/sample_size)

df['cum_sum'] = df['Total'].cumsum()
num = interval_width #can be a random number also as in the example
sampled_series = np.arange(num, total, interval_width)

cum_array = np.asarray(df['cum_sum'])
selected_samples = np.zeros(sample_size, dtype='int32')
idx = np.searchsorted(cum_array,sampled_series) #the heart of code
result = cum_array[idx-1] 

ndf = df[df.cum_sum.isin(result)]
del ndf['cum_sum'] #so that new file doesn't have cum_sum column

ndf.to_csv('sampled_file.csv', index=None)
