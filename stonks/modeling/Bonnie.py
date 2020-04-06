from sklearn.linear_model import LogisticRegression
import pandas as pd
from ..auxiliary.fitting import fit_supervised
from ..auxiliary.data_preprocessing import basic_clean
from ..auxiliary import split_to_pairs
import joblib
import logging
import datetime
import time
from ..auxiliary.data_preprocessing import make_x


# Модель 2 - эвристики + обучение с учителем (Бонни)
class BonnieModel:
    pairs_implemented = ['btcusdt', 'bchusdt', 'ethusdt', 'bnbusdt']

    # Инициализация и загрузка модели
    def __init__(self, time_=-1, indent=3600):
        self.indent = indent
        self.time_ = time_
        self.models = {}
        self.columns = {}
        self.scalers = {}
        for pair in BonnieModel.pairs_implemented:
            self.models[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_model.joblib')
            self.columns[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_columns.joblib')
            self.scalers[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_scaler.joblib')

    def __call__(self, data, balance):  # Теперь data - список словарей, текущий момент - data.iloc[-1]
        for_one = balance['usdt'] / len(BonnieModel.pairs_implemented)
        query = []
        logs = []
        memory = {}
        for pair in BonnieModel.pairs_implemented:
            memory[pair] = basic_clean(data[pair].iloc[:-1])
        for pair in BonnieModel.pairs_implemented:
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

            prob_down, prob_up = self.models[pair].predict_proba(df)[0]
            if prob_up > 0.5:
                query.append((pair, 'sell quote', for_one))
            elif prob_down > 0.5:
                query.append((pair, 'sell base', balance[pair[:3]]))
            logs.append((pair, prob_down, prob_up))
        return query, logs

    # Эта функция возвращает класс модели (просто для гибкости)
    @staticmethod
    def current_model():
        return LogisticRegression(n_jobs=-1, solver='lbfgs')

    # Обучение. Вызывается перед использованием один раз.
    @staticmethod
    def fit(data: pd.DataFrame):
        for pair in BonnieModel.pairs_implemented:
            logging.debug('fitting ' + pair)
            semi_data = data[data['currency_pair'] == pair]
            model, cols, scaler = fit_supervised(semi_data, BonnieModel.current_model())
            joblib.dump(model, 'settings/Bonnie_settings/' + pair + '_model.joblib')
            joblib.dump(cols, 'settings/Bonnie_settings/' + pair + '_columns.joblib')
            joblib.dump(scaler, 'settings/Bonnie_settings/' + pair + '_scaler.joblib')
