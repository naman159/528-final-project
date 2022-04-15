import pandas as pd
import json
import numpy as np

data_dir = "data/session-1/"
left_datafile="R2 2022-04-14 21_45_31.txt"
path = data_dir + left_datafile

log_data=open(path,'r')

# parse the log file into a pandas df
headers = ["level", "timestamp", "message"]
def log_to_json(_log_data, _headers):
    result={}
    i=0
    for line in _log_data:
        columns = line.split('\t') #or w/e you're delimiter/separator is
        data = {}
        for idx, c in enumerate(columns):
            # print(i, _headers[min(idx, len(_headers)- 1)], c)
            key = _headers[idx]
            value = c
            data[key] = value
        result[i] = data
        i += 1
    return json.dumps(result)

df=pd.read_json(log_to_json(log_data, headers), orient='index')

# %% select the 'A' application rows & parse the hex value
df = df.loc[df['level'] == 'A']
df['message'] = df.apply(lambda x: int(x['message'][9:11] + x['message'][6:8],16) if x['message'][1:5]=='(0x)' else np.NaN, axis = 1)   # magic one liner to parse the hexademical reperesnting the height (and time which I'm ignoring) sent by the sensor
df = df.dropna()
df = df.drop('level', axis=1)
df = df.set_index('timestamp')

# %%


# %% visualize
import matplotlib.pyplot as plt
y = df['message']
x = np.arange(len(y))

plt.plot(x, y)
plt.show()
