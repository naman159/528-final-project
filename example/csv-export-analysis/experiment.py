import pandas as pd

# %% read most recent
from get_data import get_most_recent_session
df = get_most_recent_session() # TODO replace with flask ORM
df

# %%
import get_charts
get_charts.session_plot(df)
