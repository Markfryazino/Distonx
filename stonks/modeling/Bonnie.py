import pandas as pd
from ..auxiliary.fitting import fit_supervised
import joblib
from absl import logging
from ..auxiliary.data_preprocessing import basic_clean, make_x
import tensorflow as tf
from random import shuffle


# Модель 2 - эвристики + обучение с учителем (Бонни)
class BonnieModel:
    with open('settings/pairs.txt') as file:
        pairs_implemented = [a[:-1] for a in file.readlines()]

    # Инициализация и загрузка модели
    def __init__(self):
        self.models = {}
        self.columns = {}
        self.scalers = {}
        for pair in BonnieModel.pairs_implemented:
            self.models[pair] = tf.keras.models.load_model('settings/Bonnie_settings/' +
                                                           pair + '_model.h5')
            self.columns[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_columns.joblib')
            self.scalers[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_scaler.joblib')

    def __call__(self, data, balance):
        query = []
        logs = []
        shuffle(BonnieModel.pairs_implemented)
        for pair in BonnieModel.pairs_implemented:
            memory = basic_clean(data[pair])
            ok_cols = self.columns[pair]
            scaler = self.scalers[pair]

            try:
                copy = memory.copy()
                some = make_x(copy)
            except IndexError:
                logging.info('that weird ta error happened')
                joblib.dump(memory, 'trash/ta_error.joblib')
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
