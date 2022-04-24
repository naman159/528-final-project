import pandas as pd
data_dir = "data/session-1/"
# %% visualize setup
df = pd.read_pickle(data_dir + 'exercise_2')
import matplotlib.pyplot as plt
def plot_scatter_distances(df):
    plt.plot(df.index, df['dist_left'], 'r')
    plt.plot(df.index, df['dist_right'], 'b')
    return plt

# %% visualize processed data
plot_scatter_distances(df).show()

# %% visualize velocity - smoothed rolling mean displacement
df_smooth = df.rolling('250ms').mean()
df_smooth = df_smooth.diff()
plot_scatter_distances(df_smooth)
