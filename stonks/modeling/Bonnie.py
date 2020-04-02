from sklearn.linear_model import LogisticRegression
import pandas as pd
from ..auxiliary.fitting import fit_supervised
from ..auxiliary import split_to_pairs
import joblib
import time
from ..auxiliary.data_preprocessing import construct_order_names, count_some, basic_clean


# Модель 2 - эвристики + обучение с учителем (Бонни)
class BonnieModel:
    pairs_implemented = ['btcusdt']

    # Инициализация и загрузка модели
    def __init__(self):
        self.models = {}
        self.columns = {}
        self.scalers = {}
        for pair in BonnieModel.pairs_implemented:
            self.models[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_model.joblib')
            self.columns[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_columns.joblib')
            self.scalers[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_scaler.joblib')

    # TODO - ну как бы сделать
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
            ok_cols = self.columns[pair]
            scaler = self.scalers[pair]

            orders = df[construct_order_names(5)]
            some = count_some(orders, 5)
            some.drop(construct_order_names(5), axis=1, inplace=True)
            some.drop('mid_price', axis=1, inplace=True)
            df = pd.DataFrame(scaler.transform(some), index=some.index, columns=some.columns)
            df = df.reindex(columns=ok_cols)

            prob_down, prob_up = self.models[pair].predict_proba(df)[0]
            if prob_up > 0.5:
                query[pair] = ('sell quote', for_one)
            elif prob_up > 0.5:
                query[pair] = ('sell base', balance[pair[:3]])
        return query

    # Эта функция возвращает класс модели (просто для гибкости)
    @staticmethod
    def current_model():
        return LogisticRegression(n_jobs=-1, solver='lbfgs')

    # Обучение. Вызывается перед использованием один раз.
    @staticmethod
    def fit(data: pd.DataFrame):
        for pair in BonnieModel.pairs_implemented:
            semi_data = data[data['currency_pair'] == pair]
            model, cols, scaler = fit_supervised(semi_data, BonnieModel.current_model())
            joblib.dump(model, 'settings/Bonnie_settings/' + pair + '_model.joblib')
            joblib.dump(cols, 'settings/Bonnie_settings/' + pair + '_columns.joblib')
            joblib.dump(scaler, 'settings/Bonnie_settings/' + pair + '_scaler.joblib')
