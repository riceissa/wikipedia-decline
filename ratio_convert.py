import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.dates as dates

from csv_list import data
from plot import get_df

dfs = []
for i in range(1, 30):
    df = pd.read_csv('google_trends_mj/{0:02}.csv'.format(i))
    dfs.append(df)

# pd.concat([df.iloc[:, 1:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs], axis=1).set_index(dfs[0]['Week'])

def plot_musicians_log_minus():
    '''
    This plots log(w(t)) - log(k(t)), where
        WV(p, t) = P(p, t) * w(t)
        GT(p, t) = P(p, t) * k(t)
    where p is the page, t is time, WV is the number of Wikipedia pageviews, GT
    is the Google Trends value, w is the usefulness of Wikipedia, and k is the
    inverse of the popularity of Google.
    '''
    wv_df = get_df('data/musicians_desktop.csv', 1)
    gt_df = pd.concat(
            # select non-MJ column and normalize by MJ max
            [df.iloc[:, 2:].divide(df['Michael Jackson: (Worldwide)'].max())
                for df in dfs] +
            # include one MJ trend too
            [dfs[0].iloc[:, 1:2].divide(dfs[0]['Michael Jackson: (Worldwide)'
                ].max())], axis=1)
    gt_df = gt_df.set_index(pd.to_datetime(dfs[0]['Week']))
    gt_df_sum = gt_df.sum(axis=1)
    combined_df = pd.DataFrame([gt_df_sum, wv_df.Total]).T
    combined_df.columns = ['google_trends', 'wikipedia_pageviews']
    combined_df = combined_df.resample('Q', fill_method='ffill')
    (np.log10(combined_df.wikipedia_pageviews) -
            np.log10(combined_df.google_trends)).plot(legend=None)
    plt.show()
    # wv_df.append(gt_df).sort_index().resample('Q-APR', loffset='-1m')

    # This is a bit fragile; it depends on the artists showing up in the same
    # order for the Google trends and Wikipedia Views data.  Also I'm not sure
    # why we need to use pd.concat here even though for the above code, we
    # could use pd.DataFrame to make a DataFrame out of two Series. I also
    # tried converting to pd.Series here but that made the Series turn into
    # this weird thing where the label names were split by character 'l', 'i',
    # 'k', 'e', ' ', 't', 'h', 'i', 's'.
    for i in range(30):
        cm = pd.concat([gt_df.iloc[:, i:i+1], wv_df.iloc[:, i:i+1]]).sort_index()
        cm = cm.resample('Q', fill_method='ffill')
        cm.columns = ['gt', 'wp']
        (np.log10(cm)['wp'] - np.log10(cm)['gt']).plot(legend=None)

plot_musicians_log_minus()

# sum of musicians
# np.log10(gt_df.sum(axis=1))

# plot with
# pd.concat([df.iloc[:, 2:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs], axis=1).plot(legend=None)
# np.log10(pd.rolling_mean(pd.concat([df.iloc[:, 1:].divide(df['Michael Jackson: (Worldwide)'].max()) for df in dfs], axis=1), window=1)).plot(legend=None) ; plt.show()
