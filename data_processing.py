import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from scipy.signal import find_peaks
from collections import deque
import json
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

def get_set_reps_df(df):
    df['dist'] = df[['dist_left', 'dist_right']].mean(axis=1)

    # velocity
    df_veloc = df.diff().rolling('100ms').median()
    df_veloc = df_veloc.rename({'dist_left': 'velocity_left', 'dist_right':'velocity_right'}, axis=1)
    df['velocity'] = df_veloc[['velocity_left', 'velocity_right']].mean(axis=1)

    # velocity correlation
    df['corr'] = df_veloc['velocity_left'].rolling('4000ms').corr(df_veloc['velocity_right'])#.rolling('400ms').mean()

    df = df.replace([np.inf, -np.inf], np.nan) # boo infinity corr
    df = df.dropna()

    df['corr^3_x_speed'] = df['corr'].pow(3) * df['velocity'].abs()

    # if any any window_size we exceed the function theshold, the window contains set data
    threshold = 10
    df_start_ts, df_end_ts = df.index[0], df.index[-1]
    window_size = datetime.timedelta(seconds=4)
    curr_ts = df_start_ts - window_size/2
    in_set = False
    n_sets = 0
    df['set_num'] = np.nan

    while curr_ts <= df_end_ts:
        window_df = df.loc[curr_ts:curr_ts+window_size]
        curr_function_value = window_df['corr^3_x_speed'].max()
        if(curr_function_value < threshold):
            if in_set:
                in_set = False
            df.drop(index=window_df.index, inplace=True)
        else:
            if not in_set:
                n_sets += 1
                in_set = True
            df.loc[curr_ts:curr_ts+window_size, 'set_num'] = n_sets
        curr_ts += window_size


    # for each set identify the peaks/valleys and therfore reps
    df['rep_num'] = np.nan
    df['rep_state'] = np.nan
    for curr_set_num in df['set_num'].unique():
        set_df = df[df['set_num'] == curr_set_num]
        data = set_df['dist']
        peaks, _ = find_peaks(data, distance=10, height=np.quantile(data, 0.75)) # distance 10 because it would take at least 1/2 second to a repitation (sample freq is 50ms * 10 distance = 500ms)
        inv_data = data * -1
        valleys, _ = find_peaks(inv_data, distance=10, height=np.quantile(inv_data, 0.75))


        curr_ts = set_df.index[0]
        n_reps = 0
        in_rep = False

        if len(valleys)==0 or len(peaks)==0: break

        # only proces peaks/valleys that have an alternate state before them
        events = [] # rep start & peak indexes so even list length
        peaks_q, valleys_q = deque(peaks), deque(valleys)
        while(len(peaks_q) and len(valleys_q)):
            p_idx, v_idx = peaks_q[0], valleys_q[0]
            if(p_idx < v_idx):
                p_idx = peaks_q.popleft() # start of rep, or junk
                if not len(peaks_q):
                    pass
                elif not peaks_q[0] < v_idx:
                    v_idx = valleys_q.popleft()
                    events += [p_idx, v_idx]
            else:
                v_idx = valleys_q.popleft() # start of rep or junk
                if not len(valleys_q):
                    pass
                elif not valleys_q[0] < p_idx:
                    p_idx = peaks_q.popleft()
                    events += [v_idx, p_idx]

        events_ts = set_df.iloc[events].index

        events_ts = events_ts.append(set_df.index[-1:]) # add the end of the set to the events timestamps

        rep_num = 0
        df.drop(index=set_df[set_df.index[0]:events_ts[0]].index, inplace=True) # drop beginning of set that's not a rep
        for i in range(0, len(events_ts)-1, 2):
            rep_num += 1
            df.loc[events_ts[i]:events_ts[i+2], 'rep_num'] = rep_num
            df.loc[events_ts[i]:events_ts[i+1], 'rep_state'] = 0
            df.loc[events_ts[i+1]:events_ts[i+2], 'rep_state'] = 1
    return df
# %% pickle the data
get_set_reps_df(processdf(2))
