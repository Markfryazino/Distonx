from ..DataCatcher.database_saver import DB
import pandas as pd
import logging
from .data_preprocessing import make_x_y
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def fit_model(model, start_time, end_time, pair_name=''):
    """Пайплайн обучения (все инкапсулировано в model.fit"""
    dbase = DB()
    names = dbase.get_columns_names()
    data = dbase.get_data_from_db(start_time, end_time, pair_name)
    logging.debug('fetched data')
    data = pd.DataFrame(data=data, columns=names)
    model.fit(data)


def fit_supervised(data, model):
    """Пайплайн обучения с учителем для Бонни"""
    plt.subplot(311)
    target = (data['depth_bid_price_1'] + data['depth_ask_price_1']) / 2.
    x, y, scaler = make_x_y(data, need_kline=False)
    x_train, x_test, y_train, \
                    y_test, tar_train, tar_test = train_test_split(x, y,
                                                   target[x.index], shuffle=False, test_size=0.2)
    logging.debug('data processed')
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    logging.debug('model trained\nREPORT:\n' + classification_report(y_test, pred))
    logging.debug('VALUE COUNTS:\n' + str(pd.Series(pred).value_counts()))

    proba = model.predict_proba(x_test)
    probas = pd.DataFrame(proba, columns=['maximum', 'minimum'], index=x_test.index)

    ups = probas['maximum'] > 0.65
    downs = probas['minimum'] > 0.65

    plt.subplot(312)
    plt.plot(x_test.index, tar_test)
    plt.scatter(x_test[y_test == 1].index, tar_test[y_test == 1], color='g')
    plt.scatter(x_test[y_test == 0].index, tar_test[y_test == 0], color='r')
    plt.subplot(313)
    plt.plot(x_test.index, tar_test)
    plt.scatter(x_test[ups].index, tar_test[ups], color='r')
    plt.scatter(x_test[downs].index, tar_test[downs], color='g')
    return model, list(x.columns), scaler
