import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
d = pd.read_csv('DTM.csv')
l = pd.read_csv('DTMlemma.csv')
d = d[d['Name']=='Donald Trump']
sums = d.sum()
sums = sums.drop(['Title','Date','Name'])
sums = sums.reset_index()
sums.sort_values(0,ascending = False,inplace = True)
temp = sums[:100]
plt.figure
plt.bar(temp['index'],temp[0])
plt.show()