"""В этом файлике собраны функции, которые могут понадобиться для обработки данных"""

import numpy as np
import datetime
import random
import matplotlib.pyplot as plt
import ta
import logging
import pandas as pd
import os

kline_id = 0


def get_id(x):
    global kline_id
    if x:
        kline_id += 1
    return x * kline_id


def get_kline_info(data):
    """Возвращает датафрейм, в котором добавлены фичи свечей из ta. Но вообще, оно inplace (аккуратно)"""
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
                                  'kline_high_price', 'kline_low_price', 'kline_close_price',
                                  'kline_base_volume')

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
    """Питоновская имплементация получения label-ов для данных"""
    if 'mid_price' in data.columns:
        target = data['mid_price']
    else:
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
    """Отрисовка label-а"""
    target = (data['depth_bid_price_1'] + data['depth_ask_price_1']) / 2.
    data['normal_time'] = data['time'].apply(datetime.datetime.fromtimestamp)
    target.index = data['normal_time']
    res.index = data['normal_time']
    target.plot()
    plt.scatter(target[res == 1].index, target[res == 1], color='g')
    plt.scatter(target[res == 0].index, target[res == 0], color='r')


def make_x_y(df, mod=0.003, need_kline=True):
    """По сути, пайплайн обработки"""
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


def plot_target(data):
    """Отрисовка таргета"""
    target = (data['depth_bid_price_1'] + data['depth_ask_price_1']) / 2.
    normal_time = data['time'].apply(datetime.datetime.fromtimestamp)
    plt.figure(figsize=(15, 5))
    plt.plot(normal_time, target)
    plt.show(block=False)


def basic_clean(data: pd.DataFrame):
    """Индекс по времени + отбрасывание некоторых столбцов"""
    data['normal_time'] = data['time'].apply(datetime.datetime.fromtimestamp)
    data.set_index('normal_time', inplace=True)
    data.drop(['id', 'time', 'currency_pair'], axis=1, inplace=True)
    return data


def get_state_cpp(prices, mod=0.001, input_name='input.txt', output_name='output.txt'):
    """Получение таргета через C++"""
    with open(input_name, 'w') as file:
        file.write(output_name + '\n')
        file.write(str(len(prices)) + ' ')
        file.write(str(mod) + '\n')
        for price in prices:
            file.write(str(price) + ' ')
    file_name = "executable"
    os.system(f'g++ -o {file_name} precount_extremums.cpp && ./executable')
    file = open("./" + output_name, 'r')
    target = eval(file.readline())
    file.close()
    os.system(f'rm {input_name} {output_name} {file_name}')
    return target


def count_some(orders, depth):
    """Подсчет некоторых признаков на основе одной строки"""
    orders['mid_price'] = (orders['depth_bid_price_1'] + orders['depth_ask_price_1']) / 2.

    # Distance to midpoint
    for col in orders.columns:
        if ('quantity' in col) or (col == 'mid_price'):
            continue
        name = col.split('_')
        orders['mid_distance_' + name[1] + '_' + name[3]] = orders[col] / orders['mid_price'] - 1.

    # Cumulative notional value
    orders['cumulative_ask_1'] = orders['depth_ask_price_1'] * orders['depth_ask_quantity_1']
    orders['cumulative_bid_1'] = orders['depth_bid_price_1'] * orders['depth_bid_quantity_1']
    for i in range(2, depth + 1):
        orders['cumulative_ask_' + str(i)] = orders['depth_ask_price_' + str(i)] * \
                                             orders['depth_ask_quantity_' + str(i)] + orders[
                                                 'cumulative_ask_' + str(i - 1)]
        orders['cumulative_bid_' + str(i)] = \
            orders['depth_bid_price_' + str(i)] * orders['depth_bid_quantity_' + str(i)] + orders[
                                                 'cumulative_bid_' + str(i - 1)]

    # Notional imbalances
    for i in range(1, depth + 1):
        orders['imbalance_' + str(i)] = \
            (orders['cumulative_ask_' + str(i)] - orders['cumulative_bid_' + str(i)]) / \
            (orders['cumulative_ask_' + str(i)] + orders['cumulative_bid_' + str(i)])

    # Spread
    orders['spread'] = orders['depth_ask_price_1'] - orders['depth_bid_price_1']
    return orders


def construct_order_names(depth):
    """Возвращает имена столбцов с ордерами"""
    to_leave = [['depth_ask_price_' + str(i), 'depth_ask_quantity_' + str(i),
                 'depth_bid_price_' + str(i), 'depth_bid_quantity_' + str(i)]
                for i in range(1, depth + 1)]
    lea = []
    for el in to_leave:
        lea += el
    return lea
