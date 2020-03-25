import numpy as np
import datetime
import random
import matplotlib.pyplot as plt
import ta
import logging
import pandas as pd


kline_id = 0


def get_id(x):
    global kline_id
    if x:
        kline_id += 1
    return x * kline_id


def get_kline_info(data):
    global kline_id
    kline_id = 0

    shifted_update = data['kline_time_since_update'].shift(1)
    data['new_kline'] = data['kline_time_since_update'] < shifted_update

    data['kline_id'] = data['new_kline'].apply(get_id)

    data['kline_id'].replace({0: np.NaN}, inplace=True)
    data['kline_id'].ffill(inplace=True)

    data.dropna(inplace=True)

    data.drop('new_kline', axis=1, inplace=True)
    klines = data[['kline_id', 'kline_trade_number', 'kline_open_price', 'kline_close_price',
                   'kline_high_price', 'kline_low_price', 'kline_base_volume',
                   'kline_quote_volume', 'kline_taker_base_volume',
                   'kline_taker_quote_volume', 'kline_time_since_update', 'kline_update_time']].groupby(
        'kline_id').mean()

    klines['kline_update_time'] = klines['kline_update_time'].apply(
        lambda x: datetime.datetime.fromtimestamp(x / 1000))

    feat = ta.add_all_ta_features(klines, 'kline_open_price',
                                  'kline_high_price', 'kline_low_price', 'kline_close_price', 'kline_base_volume')

    data.drop(['kline_trade_number', 'kline_open_price', 'kline_open_price',
               'kline_close_price', 'kline_high_price', 'kline_low_price',
               'kline_base_volume', 'kline_quote_volume', 'kline_taker_base_volume',
               'kline_taker_quote_volume', 'kline_time_since_update',
               'kline_update_time'], axis=1, inplace=True)

    feat.drop('kline_update_time', axis=1, inplace=True)
    data = data.merge(feat, on='kline_id')
    data.fillna(0, inplace=True)
    return data


def get_state(data, mod=0.001):
    target = (data['depth_bid_price_1'] + data['depth_ask_price_1']) / 2.
    res = pd.Series(index=target.index, data=-1)

    for _ in range(5):
        logging.debug('state step: ' + str(_))
        period = random.randint(3000, 4000)
        start = 0
        while start < res.shape[0]:
            a = target[start:start + period].values

            diff_mat = a - a[:, None] * (1. + mod)
            upper = (np.triu(diff_mat) > 0).argmax(1)
            np.place(upper, upper == 0, 10 ** 9)

            diff_mat = a - a[:, None] * (1. - mod)
            lower = (np.triu(diff_mat) < 0).argmax(1)
            np.place(lower, lower == 0, 10 ** 9)

            res[target[start:start + period][upper < lower].index] = 1
            res[target[start:start + period][upper > lower].index] = 0
            start += period
    return res


def plot_state(data, res):
    target = (data['depth_bid_price_1'] + data['depth_ask_price_1']) / 2.
    data['normal_time'] = data['time'].apply(datetime.datetime.fromtimestamp)
    target.index = data['normal_time']
    res.index = data['normal_time']
    target.plot()
    plt.scatter(target[res == 1].index, target[res == 1], color='g')
    plt.scatter(target[res == 0].index, target[res == 0], color='r')
    #plt.show(block=False)


def make_x_y(df, mod=0.003, need_kline=True):
    if need_kline:
        logging.debug('counting klines')
        df = get_kline_info(df)
        df.drop('kline_id', axis=1, inplace=True)
    logging.debug('getting state')
    res = get_state(df, mod)
    plot_state(df, res)
    df.set_index('normal_time', inplace=True)
    df.drop(['id', 'time', 'currency_pair'], axis=1, inplace=True)
    df = df[res != -1]
    res = res[res != -1]
    return df, res
