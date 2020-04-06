from ..DataCatcher.database_saver import DB
import pandas as pd
from absl import logging
from .data_preprocessing import make_x_y
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import tensorflow as tf


def fit_model(model, start_time, end_time, pair_names=None, dbase=None):
    """Пайплайн обучения (все инкапсулировано в model.fit)"""
    if pair_names is None:
        pair_names = set()
    if dbase is None:
        dbase = DB()
    names = dbase.get_columns_names()
    data = dbase.get_data_from_db(start_time, end_time, pair_names=pair_names)
    logging.debug('fetched data')
    data = pd.DataFrame(data=data, columns=names)
    model.fit(data)


def fit_supervised(data, model):
    """Пайплайн обучения с учителем для Бонни"""
    x, y, scaler = make_x_y(data)
    y_cat = tf.keras.utils.to_categorical(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y_cat, shuffle=False, test_size=24 * 3600)
    x_train, y_train = shuffle(x_train, y_train)
    logging.debug('data processed')
    model.fit(x_train, y_train)
    pred = model.predict_classes(x_test)
    print('model trained\nREPORT:\n' + classification_report(y_test[:, 1], pred))
    print('VALUE COUNTS:\n' + str(pd.Series(pred).value_counts()))
    print('REAL VALUE COUNTS:\n' + str(pd.Series(y_test[:, 1]).value_counts()))
    return model, list(x.columns), scaler
