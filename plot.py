import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

from csv_list import data

def get_df(fname, win_len):
    '''
    Return the rolling mean pageview dataframe, normalized by the number of
    dates in the time period. When win_len is 1, this is of course just the raw
    monthly pageviews that was passed in.
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
        d0 = tmp.iloc[i-win_len+1].name
        d1 = tmp.iloc[i].name
        d1_eom = pd.to_datetime(datetime.date(d1.year, d1.month,
            d1.days_in_month))
        # [number of days in period] = [end of current month] -
        #   [beginning of previous month] + 1, to include the final day
        num_days = (d1_eom - d0).days + 1
        rolling.iloc[i] = tmp.iloc[i].divide(num_days)
    return rolling

for key in data:
    for n in [1, 3, 6, 12]:
        df = get_df(data[key][0], n)
        df_mobapp = get_df(data[key][1], n)
        df_mob = get_df(data[key][2], n)
        np.log10(df).plot()
        plt.legend(prop={'size': 7})
        plt.title("{}: moving avg of {} months".format(key, n))
        plt.savefig("plots/{}_{}_{}.png".format(key, "total", n))
        plt.clf()

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

