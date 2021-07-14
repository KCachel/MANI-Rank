import numpy as np
import pandas as pd

baseR = pd.read_excel('allyr_baserankings.xlsx')
baseR = baseR.replace(u'\xa0', u' ', regex=True) #get rid of weird encoding
print(baseR)

deptdf = pd.read_excel('/Users/KathleenCachel/OneDrive - Worcester Polytechnic Institute (wpi.edu)/ResearchWork2021/csrankings_dictionary.xlsx')
print(deptdf)

school_int_id_dict = {}

for i in range(len(deptdf['School'])):
    school_int_id_dict[deptdf['School'][i]] = i

cs_baseranks = np.full((21,65), np.inf)

for yr in range(21):
    yr_series = baseR[baseR.columns[yr]]
    recode_yr_series = yr_series.map(school_int_id_dict)
    np_array_yr = recode_yr_series.to_numpy()
    cs_baseranks[yr,:] = np_array_yr

print(cs_baseranks)
np.save('cs_baseranks.npy', cs_baseranks)