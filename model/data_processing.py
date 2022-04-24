import pandas as pd
import json
import numpy as np
import os

data_dir = "data/session-1/"
r_file="R2 2022-04-14 21_45_31.txt"
l_file="L2 2022-04-14 21_45_49.txt"
def processFile(filename):
    path = data_dir + filename
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
    # select the application rows & parse the hex value representing the height
    df = df.loc[df['level'] == 'A']
    df['message'] = df.apply(lambda x: int(x['message'][9:11] + x['message'][6:8],16) if x['message'][1:5]=='(0x)' else np.NaN, axis = 1)   # magic one liner to parse the hexademical reperesnting the height (and time which I'm ignoring) sent by the sensor

    df.rename(columns = {'message':'dist'}, inplace = True)
    df = df.dropna()
    df = df.drop('level', axis=1)
    df = df.set_index('timestamp')
    return df

def processdf(session_id):
    # find files matching L + session_id & R + session_id
    l_df, r_df = None, None
    for file in os.listdir(data_dir):
        if file.startswith('L' + str(session_id)):
            l_df = processFile(file)
        elif file.startswith('R' + str(session_id)):
            r_df = processFile(file)
    assert(l_df is not None and r_df is not None)

    # find earliest common slow-time scan & lastest common scan & then drop rows not common on time
    earliest_common_scan = max(l_df.index[0], r_df.index[0])
    latest_common_scan = min(l_df.index[-1], r_df.index[-1])

    x, y = latest_common_scan > l_df.index, l_df.index > earliest_common_scan
    keeps = [a and b for a, b in zip(x, y)]
    index_to_drop = l_df.index[np.invert(keeps)]
    l_df.drop(index=index_to_drop, inplace=True)

    x, y = latest_common_scan > r_df.index, r_df.index > earliest_common_scan
    keeps = [a and b for a, b in zip(x, y)]
    index_to_drop = r_df.index[np.invert(keeps)]
    r_df.drop(index=index_to_drop, inplace=True)

    # average over 250ms windows & join df's
    l_df = l_df.reset_index()
    l_df['timestamp']= l_df.timestamp.dt.ceil(freq='50L')
    l_df = l_df.groupby('timestamp').mean()
    l_df = l_df.rename(columns={'dist':'dist_left'})

    r_df = r_df.reset_index()
    r_df['timestamp']= r_df.timestamp.dt.ceil(freq='50L')
    r_df = r_df.groupby('timestamp').mean()
    r_df = r_df.rename(columns={'dist':'dist_right'})

    df = pd.merge(l_df, r_df, how='left', left_index=True, right_index=True)
    df.ffill(inplace=True) # just incase a window has no samples
    return df

# %% visualize setup
import matplotlib.pyplot as plt
def plot_scatter_distances(df):
    plt.plot(df.index, df['dist_left'], 'r')
    plt.plot(df.index, df['dist_right'], 'b')
    return plt

# %% visualize processed data
df = processdf(2)
plot_scatter_distances(df).show()

# %% visualize velocity - smoothed rolling mean displacement
df_smooth = df.rolling('250ms').mean()
df_smooth = df_smooth.diff()
plot_scatter_distances(df_smooth)
