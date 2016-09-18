import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

def get_dfs(fname, win_len):
    '''
    Return (raw, rolling), where raw is the raw pageviews dataframe and rolling
    is the rolling mean pageview dataframe, normalized by the number of dats in
    the time period.
    '''
    df = pd.read_csv(fname, sep='|')
    df = df[:-2] # remove "Total" and "Percentage" rows from the bottom
    # 200610 -> "2006-10"
    df['Month'] = pd.to_datetime(df['Month'].map(lambda x:
        str(x)[:4] + "-" + str(x)[4:]))
    df = df.set_index('Month')
    df = df.sort_index()
    del df['Percentage']

    rolling = pd.rolling_sum(df, window=win_len)
    tmp = rolling.copy()
    for i in range(win_len-1, len(rolling)):
        # TODO use the month ends to calculate the period
        # TODO win_len=1 should return raw df
        d0 = tmp.iloc[i-win_len+1].name
        d1 = tmp.iloc[i].name
        d1_eom = pd.to_datetime(datetime.date(d1.year, d1.month,
            d1.days_in_month))
        # [number of days in period] = [end of current month] -
        #   [beginning of previous month] + 1, to include the final day
        num_days = (d1_eom - d0).days + 1
        rolling.iloc[i] = tmp.iloc[i].divide(num_days)

    rolling = rolling.divide(rolling.index.days_in_month, axis='index')
    return (df, rolling)

    return something

def raw_df(fname):
    df = pd.read_csv(fname, sep='|')
    df = df[:-2] # remove "Total" and "Percentage" rows from the bottom
    df['Month'] = pd.to_datetime(df['Month'].map(lambda x:
        str(x)[:4] + "-" + str(x)[4:]))
    df = df.set_index('Month')
    df = df.sort_index()
    del df['Percentage']
    return df

def get_df(fname, win_len):
    df = pd.read_csv(fname)
    df = df[:-2] # remove "Total" and "Percentage" rows from the bottom
    df['Month'] = pd.to_datetime(df['Month'].map(lambda x:
        str(x)[:4] + "-" + str(x)[4:]))
    df = df.set_index('Month')
    df = df.sort_index()
    del df['Percentage']
    df = pd.rolling_sum(df, window=win_len)
    tmp = df.copy()
    for i in range(win_len-1, len(df)):
        # TODO use the month ends to calculate the period
        num_days = (tmp.iloc[i].name - tmp.iloc[i-win_len+1].name).days
        df.iloc[i] = tmp.iloc[i].divide(num_days)
    # df = df.divide(df.index.days_in_month, axis='index')
    return df

df = raw_df('desktop_monthly_colors.csv')
df_mob = raw_df('mobile_monthly_colors.csv')
df_mobapp = raw_df('mobileapp_monthly_colors.csv')
# df = lambda n: get_df('french_colors_desktop.csv', n)
# df_mob = lambda n: get_df('french_colors_mobile.csv', n)
# df_mobapp = lambda n: get_df('french_colors_mobileapp.csv', n)

# To plot, use something like this
# np.log10(df(n)+df_mob(n)+df_mobapp(n)).plot(color=colors, legend=None) ; plt.title("log10 plot, moving avg of {} months".format(n)) ; plt.show()
# n=2 ; np.log10(df(n)).plot(color=colors, legend=None) ; plt.axvspan(datetime.date(2015, 7, 1), datetime.date(2016, 9, 1), color='yellow', alpha=0.4) ; plt.axvspan(datetime.date(2007, 12, 1), datetime.date(2016, 1, 1), color='green', alpha=0.4) ; plt.title("log10 plot, moving avg of {} months, no mobile".format(n)) ; plt.show()
# top 10 countries plot
# n=3 ; np.log10(df(n)[df(n).sum().sort_values(ascending=False).index[:11]]).plot() ; plt.title("log10 plot, moving avg of {} months".format(n)) ; plt.show()
# cities
# n=6 ; top = df(n).sum().sort_values(ascending=False).index[:11] ; np.log10(df(n)[top] + df_mob(n)[top]).plot() ; plt.legend(loc='lower left', prop={'size': 7}); plt.title("citites, moving avg of %d months, desktop+mobileweb" % n) ; plt.show()

colors = ('k', 'b', 'brown', 'g', 'grey', 'orange', 'purple', 'r', 'violet', 'lightgrey', 'y', 'cyan')

# df = pd.read_csv('desktop_colors.csv')
# df['Year'] = pd.to_datetime(df['Year'].map(lambda x: str(x)+"-01-01"))
# df = df.set_index('Year')
# df = df.sort_index()
# del df['Percentage']
# df = df[1:] # remove 2007
# df.loc['2016-01-01'] = df.loc['2016-01-01'] * (365 / 260)

# df2 = pd.read_csv('mobile_colors.csv')
# df2['Year'] = pd.to_datetime(df2['Year'].map(lambda x: str(x)+"-01-01"))
# df2 = df2.set_index('Year')
# df2 = df2.sort_index()
# del df2['Percentage']
# df2 = df2[1:] # remove 2007
# df2.loc['2016-01-01'] = df2.loc['2016-01-01'] * (365 / 260)

