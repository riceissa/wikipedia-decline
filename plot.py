import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        num_days = (tmp.iloc[i].name - tmp.iloc[i-win_len+1].name).days
        df.iloc[i] = tmp.iloc[i].divide(num_days)
    # df = df.divide(df.index.days_in_month, axis='index')
    return df

df = lambda n: get_df('desktop_monthly_colors.csv', n)
df_mob = lambda n: get_df('mobile_monthly_colors.csv', n)
df_mobapp = lambda n: get_df('mobileapp_monthly_colors.csv', n)

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

