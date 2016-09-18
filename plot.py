import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

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

df = lambda n: get_df('desktop_countries_monthly.csv', n)
df_mob = lambda n: get_df('mobile_countries_monthly.csv', n)
df_mobapp = lambda n: get_df('mobileapp_countries_monthly.csv', n)

# To plot, use something like this
# np.log10(df(n)+df_mob(n)+df_mobapp(n)).plot(color=colors, legend=None) ; plt.title("log10 plot, moving avg of {} months".format(n)) ; plt.show()
# n=2 ; np.log10(df(n)).plot(color=colors, legend=None) ; plt.axvspan(datetime.date(2015, 7, 1), datetime.date(2016, 9, 1), color='yellow', alpha=0.4) ; plt.axvspan(datetime.date(2007, 12, 1), datetime.date(2016, 1, 1), color='green', alpha=0.4) ; plt.title("log10 plot, moving avg of {} months, no mobile".format(n)) ; plt.show()
# top 10 countries plot
# n=3 ; np.log10(df(n)[df(n).sum().sort_values(ascending=False).index[:11]]).plot() ; plt.title("log10 plot, moving avg of {} months".format(n)) ; plt.show()

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

