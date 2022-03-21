import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def session_plot(df):
    s_max = df['s'].max()
    r_max = df['r'].max()
    fig, axes = plt.subplots(s_max, r_max, figsize=(30, 20), sharey=True)
    fig.suptitle('Session: ')

    for curr_s in range(s_max):
        for curr_r in range(r_max):
            selected_df = df.loc[(df['s'] == curr_s) & (df['r'] == curr_r)]
            sns.scatterplot(data=selected_df, ax=axes[curr_s, curr_r], x='filteredTime', y='filteredHeight', hue='device', palette=sns.color_palette(['red', 'blue']))
    return fig
