from ..DataCatcher.database_saver import DB
import pandas as pd
import logging
from .data_preprocessing import make_x_y
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def fit_model(model, start_time, end_time, pair_names=None):
    """Пайплайн обучения (все инкапсулировано в model.fit)"""
    if pair_names is None:
        pair_names = set()
    dbase = DB()
    names = dbase.get_columns_names()
    data = dbase.get_data_from_db(start_time, end_time, pair_names=pair_names)
    logging.debug('fetched data')
    data = pd.DataFrame(data=data, columns=names)
    model.fit(data)


def fit_supervised(data, model):
    """Пайплайн обучения с учителем для Бонни"""
    x, y, scaler = make_x_y(data)
    x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=False, test_size=12 * 3600)
    logging.debug('data processed')
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    print('model trained\nREPORT:\n' + classification_report(y_test, pred))
    print('VALUE COUNTS:\n' + str(pd.Series(pred).value_counts()))
    print('REAL VALUE COUNTS:\n' + str(pd.Series(y_test).value_counts()))
    return model, list(x.columns), scaler
