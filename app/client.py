from copyreg import pickle
from io import StringIO
import io
import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import os
import json
import data_processing

#---------------------------------------------------------------------------------------------------------#
# Data Processing on Upload
data_dir = "data/txt/"

def processFile(log_data):

    headers = ["level", "timestamp", "message"]
    def log_to_json(_log_data, _headers):
        result={}
        i=0
        for line in _log_data:
            columns = line.split('\t') #or w/e you're delimiter/separator is
            data = {}
            for idx, c in enumerate(columns):
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

def processdf(files):
    l_df, r_df = processFile(files[0]), processFile(files[1])

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

    df = data_processing.get_set_reps_df(df)
    return df

def get_pickle(id, files):
    df = processdf(files)
    df.to_pickle("data/pickle/" + 'exercise'+id)
    #print(df)
#---------------------------------------------------------------------------------------------------------#

# App
if 'options' not in st.session_state:
    st.session_state['options'] = os.listdir("data/pickle/")


st.title('Exercise')

bc = st.empty()
lc = st.empty()



with st.sidebar:
    dropdown = st.empty()
    st.session_state['choice'] = dropdown.selectbox('Choose the exercise/day', st.session_state['options'], 0)

    st.session_state['df'] = pd.read_pickle("data/pickle/" + st.session_state['choice'])

    # Upload files
    uploaded_files = st.file_uploader("Upload L & R text files", accept_multiple_files=True)

    # 2 files
    if uploaded_files:
        def convert_to_wrapper(file):
            reader = io.BufferedReader(file)
            return io.TextIOWrapper(reader)

        uploaded_files = list(map(convert_to_wrapper, uploaded_files))
        get_pickle('8', uploaded_files) # Todo: Unique id creation/date


        st.session_state['options'] = os.listdir("data/pickle/")
        st.session_state['choice'] = dropdown.selectbox('Choose the exercise/day', st.session_state['options'])
        st.session_state['df'] = pd.read_pickle("data/pickle/" + st.session_state['choice'])

bc.bar_chart(st.session_state['df'].groupby('set_num')['rep_num'].max())
lc.line_chart(st.session_state['df']['dist'])
