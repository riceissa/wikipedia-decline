import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.dates as dates

from csv_list import data

dfs = []
for i in range(1, 30):
    df = pd.read_csv('google_trends_mj/{0:02}.csv'.format(i))
    dfs.append(df)

pd.concat([df.iloc[:, 1:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs], axis=1).set_index(dfs[0]['Week'])

# pd.concat([df.iloc[:, 2:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs] + [dfs[0].iloc[:, 1:2].divide(dfs[0]['Michael Jackson: (Worldwide)'].max())], axis=1).set_index(dfs[0]['Week'])['Michael Jackson: (Worldwide)'].plot(legend=None); plt.show()
# gt_df = np.log10(pd.concat([df.iloc[:, 2:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs] + [dfs[0].iloc[:, 1:2].divide(dfs[0]['Michael Jackson: (Worldwide)'].max())], axis=1).set_index(dfs[0]['Week']))

# plot with
# pd.concat([df.iloc[:, 2:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs], axis=1).plot(legend=None)
# np.log10(pd.rolling_mean(pd.concat([df.iloc[:, 1:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs], axis=1), window=1)).plot(legend=None) ; plt.show()
