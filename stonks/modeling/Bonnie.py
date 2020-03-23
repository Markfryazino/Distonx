from ..auxiliary import split_to_pairs
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import logging
import pandas as pd
import time
import logging
import numpy as np
import joblib


def fill(x):
    if x['is_min']:
        return 0
    elif x['is_max']:
        return 1
    else:
        return np.NaN


class BonnieModel:
    pairs_implemented = ['btcusdt']

    def __init__(self):
        self.models = {}
        for pair in BonnieModel.pairs_implemented:
            self.models[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_model.joblib')

    def __call__(self, data, balance):
        for_one = balance['usdt'] / len(BonnieModel.pairs_implemented)
        dct = split_to_pairs(data)
        query = {}
        for pair in BonnieModel.pairs_implemented:
            cur = dct[pair].copy()
            cur = {key: float(val) for (key, val) in cur.items()}
            cur['kline_time_since_update'] = time.time() * 1000 - cur['kline_update_time']
            cur['target'] = (cur['depth_bid_price_1'] + cur['depth_ask_price_1']) / 2.
            del cur['kline_update_time']
            cur = {key: [val] for key, val in cur.items()}
            df = pd.DataFrame(cur)
            ok_cols = self.models[pair].get_booster().feature_names
            df = df.reindex(columns=ok_cols)

            prob_up = self.models[pair].predict_proba(df)[0][1]
            if prob_up > 0.7:
                query[pair] = ('sell quote', for_one)
            elif prob_up < 0.3:
                query[pair] = ('sell base', balance[pair[:3]])
        return query



    @staticmethod
    def get_model():
        return XGBClassifier()

    @staticmethod
    def fit_partial(pair, data: pd.DataFrame, window_size=200):
        logging.debug('starting fitting Bonnie on ' + pair)
        data['target'] = (data['depth_bid_price_1'] + data['depth_ask_price_1']) / 2.
        data['minimum'] = data['target'].rolling(window_size, center=True).min()
        data['maximum'] = data['target'].rolling(window_size, center=True).max()
        data['is_min'] = data['target'] == data['minimum']
        data['is_max'] = data['target'] == data['maximum']
        data['state'] = data.apply(fill, axis=1)
        data['state'].bfill(inplace=True)
        data.dropna(inplace=True)

        X = data.drop(['id', 'state', 'currency_pair', 'minimum', 'maximum', 'is_min', 'is_max',
                       'time', 'kline_update_time'], axis=1)
        y = data['state']
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True)
        model = BonnieModel.get_model()
        logging.debug('fitting model')
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        logging.debug('\n' + classification_report(y_test, pred))
        return model

    @staticmethod
    def fit(data: pd.DataFrame, window_size=200):
        for pair in BonnieModel.pairs_implemented:
            semi_data = data[data['currency_pair'] == pair]
            model = BonnieModel.fit_partial(pair, semi_data, window_size=window_size)
            joblib.dump(model, 'settings/Bonnie_settings/' + pair + '_model.joblib')
