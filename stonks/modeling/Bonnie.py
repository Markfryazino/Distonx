import pandas as pd
from ..auxiliary.fitting import fit_supervised
from ..auxiliary.data_preprocessing import basic_clean
from ..auxiliary import split_to_pairs
import joblib
from absl import logging
import datetime
import time
from ..auxiliary.data_preprocessing import basic_clean, make_x
from ..DataCatcher.database_saver import DB
import tensorflow as tf
from random import shuffle


# Модель 2 - эвристики + обучение с учителем (Бонни)
class BonnieModel:
    with open('settings/pairs.txt') as file:
        pairs_implemented = [a[:-1] for a in file.readlines()]

    # Инициализация и загрузка модели
    def __init__(self, time_=-1, indent=3600):
        self.indent = indent
        self.time_ = time_
        self.models = {}
        self.columns = {}
        self.scalers = {}
        for pair in BonnieModel.pairs_implemented:
            self.models[pair] = tf.keras.models.load_model('settings/Bonnie_settings/' +
                                                           pair + '_model.h5')
            self.columns[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_columns.joblib')
            self.scalers[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_scaler.joblib')

    def __call__(self, data, balance):  # Теперь data - список словарей, текущий момент - data.iloc[-1]
        query = []
        logs = []
        memory = {}
        shuffle(BonnieModel.pairs_implemented)
        for pair in BonnieModel.pairs_implemented:
            memory[pair] = basic_clean(data[pair].iloc[:-1])
            ok_cols = self.columns[pair]
            scaler = self.scalers[pair]

            try:
                copy = memory[pair].copy()
                some = make_x(copy)
            except IndexError:
                logging.info('that weird ta error happened')
                joblib.dump(memory[pair], 'trash/ta_error.joblib')
                continue
            some = some[ok_cols]
            df = pd.DataFrame(scaler.transform(some), index=some.index, columns=some.columns)

            prob_down, prob_up = self.models[pair].predict(df)[0]
            if prob_up > 0.5:
                query.append((pair, 'sell quote', balance[pair[3:]]))
            elif prob_down > 0.5:
                query.append((pair, 'sell base', balance[pair[:3]]))
            logs.append((pair, prob_down, prob_up))
        return query, logs

    # Эта функция возвращает класс модели (просто для гибкости)
    @staticmethod
    def current_model():
        model = tf.keras.Sequential(name='btcusdt model')
        model.add(tf.keras.layers.Dense(128, input_shape=(109,)))
        model.add(tf.keras.layers.Dropout(0.5))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(2, activation='softmax'))

        model.compile('adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    # Обучение. Вызывается перед использованием один раз.
    @staticmethod
    def fit(data: pd.DataFrame):
        for pair in BonnieModel.pairs_implemented:
            logging.debug('fitting ' + pair)
            semi_data = data[data['currency_pair'] == pair]
            model, cols, scaler = fit_supervised(semi_data, BonnieModel.current_model())
            model.save('settings/Bonnie_settings/' + pair + '_model.h5')
            joblib.dump(cols, 'settings/Bonnie_settings/' + pair + '_columns.joblib')
            joblib.dump(scaler, 'settings/Bonnie_settings/' + pair + '_scaler.joblib')
