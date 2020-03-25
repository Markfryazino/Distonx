from ..DataCatcher.database_saver import db
import pandas as pd
import logging
from .data_preprocessing import make_x_y
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def fit_model(model, start_time, end_time, pair_name=''):
    dbase = db()
    names = dbase.get_columns_names()
    data = dbase.get_data_from_DB(start_time, end_time, pair_name)
    logging.debug('fetched data')
    data = pd.DataFrame(data=data, columns=names)
    model.fit(data)


def fit_supervised(data, model):
    plt.subplot(311)
    x, y = make_x_y(data)
    x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=False, test_size=0.2)
    logging.debug('data processed')
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    logging.debug('model trained\nREPORT:\n' + classification_report(y_test, pred))
    logging.debug('VALUE COUNTS:\n' + str(pd.Series(pred).value_counts()))

    proba = model.predict_proba(x_test)
    probas = pd.DataFrame(proba, columns=['maximum', 'minimum'], index=x_test.index)

    x_test['target'] = (x_test['depth_bid_price_1'] + x_test['depth_ask_price_1']) / 2.

    ups = probas['maximum'] > 0.5
    downs = probas['minimum'] > 0.5

    plt.subplot(312)
    plt.plot(x_test.index, x_test['target'])
    plt.scatter(x_test[y_test == 1].index, x_test[y_test == 1]['target'], color='g')
    plt.scatter(x_test[y_test == 0].index, x_test[y_test == 0]['target'], color='r')
    #plt.show(block=False)
    plt.subplot(313)
    plt.plot(x_test.index, x_test['target'])
    plt.scatter(x_test[ups].index, x_test[ups]['target'], color='r')
    plt.scatter(x_test[downs].index, x_test[downs]['target'], color='g')
    #plt.show(block=False)
    return model
