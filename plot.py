import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.dates as dates

from csv_list import data

sums = dict()

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

    # Just for double checking later
    sums[fname.split(".")[0][len("data/"):]] = df[datetime.date(2015, 7, 1):].Total.sum()

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

def get_stats(data, period_lengths=[1, 3, 6, 12]):
    '''
    Take a dict data which has tag names as keys and a list of file paths to
    CSVs as values. The order of the dataframes in the list is given in
    csv_list.py.

    Return a tuple (d, d2). Here d is a dict whose keys are tag names (the same
    ones present in data) and values are the mobile:desktop pageviews ratio
    since July 2015 of the respective tags. d2 is a dict whose keys are tuples
    (platform, tag, window), where platform is "combined" or "desktop", tag is
    the tag name, and window is the window length. The value is the month of
    peak pageviews for that tuple.
    '''
    d = dict()
    d2 = dict()

    # Get the overall mobile:desktop ratio since July 2015
    for key in data:
        df = get_df(data[key][0], 1)[datetime.date(2015, 7, 1):]
        df_mobapp = get_df(data[key][2], 1)
        df_mob = get_df(data[key][3], 1)
        # df, df_mobapp, and df_mob are normalized by the number of days in the
        # month, but we want the raw counts, so reproduce the raw totals. We
        # could have just re-read the CSVs and gotten the totals that way, but
        # since we already have the dataframes through get_df() we might as
        # well use them.
        desktop_total = df.Total.multiply(df.index.days_in_month).sum()
        mobile_total = (df_mobapp + df_mob).Total.multiply(
                df_mob.index.days_in_month).sum()
        d[key] = mobile_total/desktop_total

    # Find the month of peak pageviews for each tag and for each window length.
    for key in data:
        for n in period_lengths:
            df = get_df(data[key][0], n)
            df_mobapp = get_df(data[key][2], n)
            df_mob = get_df(data[key][3], n)
            combined = df + df_mobapp + df_mob
            d2[("combined", key, n)] = combined.Total.argmax()
            d2[("desktop", key, n)] = df.Total.argmax()

    return (d, d2)

# plot scatter plot
# a = pd.DataFrame([d2, d]).T ; plt.scatter(a[0].map(dates.date2num), a[1]) ; plt.show()

def do_top_quantile_plot(dfs, tag_list):
    c = 0
    d = dict()
    for df in dfs:
        dft = df.Total
        quantile = np.log10(dft[dft.notnull() & (dft.map(lambda x: x != 0))]
                ).quantile(0.95)
        ts = [t for t in dft[np.log10(dft) > quantile].index]
        plt.scatter(ts, [c]*len(ts))
        c += 1
    plt.title("test")
    plt.savefig("plots/test" + ".png")
    plt.clf()
    plt.close()

def do_a_plot(df, fname_base, n, show_wm_api_switch=False,
        show_mobile_onset=False, top=None):
    save_fname = "plots/" + fname_base
    if top is not None:
        np.log10(df[top]).plot(legend=None)
    else:
        np.log10(df).plot(legend=None)
    # plt.legend(prop={'size': 7})
    if show_wm_api_switch:
        plt.axvline(pd.to_datetime('2016-01-01'), color='r', lw=2)
        plt.axvline(pd.to_datetime('2016-01-01')+relativedelta(months=n-1),
                color='y', lw=2)
    if show_mobile_onset:
        plt.axvline(pd.to_datetime('2015-07-01'), color='b', lw=2)
        plt.axvline(pd.to_datetime('2015-07-01')+relativedelta(months=n-1),
                color='g', lw=2)
    dft = df.Total
    quantile = np.log10(dft[dft.notnull() & (dft.map(lambda x: x != 0))]
            ).quantile(0.75)
    plt.axhline(quantile)
    print(fname_base, quantile)
    plt.title("{} log10: moving avg of {} months".format(fname_base, n))
    plt.savefig("plots/" + fname_base + "_{}.png".format(n))
    plt.clf()
    plt.close()

if __name__ == "__main__":
    # TODO fix this
    # keyorder = get_stats(data, [6])
    d, d2 = get_stats(data)

    # Print mobile:desktop ratios
    # for tup in sorted(d.items(), key=lambda x: x[1]):
    #     print(tup)

    # Print peak months
    # for tup in sorted(d2.items()):
    #     print(tup)

    big_list = []
    tag_list = []
    # Take a slice of this list to restrict output; this is good for testing
    # since producing all plots takes a while.
    # data_list = sorted(list(data.keys()))[:]
    # print("data_list", data_list)
    # data_list = [x[0] for x in keyorder]
    data_list = []
    for key in data_list[:]:
        for n in [1, 3, 6, 12]:
            df = get_df(data[key][0], n)
            # stats.grok.se has a different way of dealing with spiders, so
            # only use the bot data starting in 2016 (when the API switch was
            # made)
            df_desktop_spider = get_df(data[key][1],
                    n)[datetime.date(2016, 1, 1):]
            df_mobapp = get_df(data[key][2], n)
            df_mob = get_df(data[key][3], n)
            df_mob_spider = get_df(data[key][4], n)[datetime.date(2016, 1, 1):]
            combined = df + df_mobapp + df_mob
            top = combined.sum().sort_values(ascending=False).index[:11]

            do_a_plot(combined, fname_base=key+"_total", n=n,
                    show_wm_api_switch=True, show_mobile_onset=True)
            do_a_plot(combined, fname_base=key+"_total_top", n=n,
                    show_wm_api_switch=True, show_mobile_onset=True, top=top)

            do_a_plot(df, fname_base=key+"_desktop", show_wm_api_switch=True,
                    n=n, show_mobile_onset=False)
            do_a_plot(df, fname_base=key+"_desktop_top",
                    show_wm_api_switch=True, n=n, show_mobile_onset=False,
                    top=top)

            do_a_plot(df_mobapp + df_mob, fname_base=key+"_mobile",
                    show_wm_api_switch=True, n=n, show_mobile_onset=True)
            do_a_plot(df_mobapp + df_mob, fname_base=key+"_mobile_top",
                    show_wm_api_switch=True, n=n, show_mobile_onset=True,
                    top=top)

            combined_with_spider = combined.add(df_desktop_spider +
                    df_mob_spider, fill_value=0)

            do_a_plot(combined_with_spider, fname_base=key+"_total_spider",
                    show_wm_api_switch=True, n=n, show_mobile_onset=True)
            do_a_plot(combined_with_spider, fname_base=key+"_total_spider_top",
                    show_wm_api_switch=True, n=n, show_mobile_onset=True,
                    top=top)

            # if n == 6:
            #     big_list.append(df)
            #     tag_list.append(key)
    # do_top_quantile_plot(big_list, tag_list)

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

