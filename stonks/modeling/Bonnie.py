from sklearn.linear_model import LogisticRegression
import pandas as pd
from ..auxiliary.fitting import fit_supervised
import joblib


# Модель 2 - эвристики + обучение с учителем (Бонни)
class BonnieModel:
    pairs_implemented = ['btcusdt']

    # Инициализация и загрузка модели
    def __init__(self):
        self.models = {}
        for pair in BonnieModel.pairs_implemented:
            self.models[pair] = joblib.load('settings/Bonnie_settings/' + pair + '_model.joblib')

    # TODO - ну как бы сделать
    def __call__(self, data, balance):
        pass

    # Эта функция возвращает класс модели (просто для гибкости)
    @staticmethod
    def current_model():
        return LogisticRegression(n_jobs=-1)

    # Обучение. Вызывается перед использованием один раз.
    @staticmethod
    def fit(data: pd.DataFrame):
        for pair in BonnieModel.pairs_implemented:
            semi_data = data[data['currency_pair'] == pair]
            model = fit_supervised(semi_data, BonnieModel.current_model())
            joblib.dump(model, 'settings/Bonnie_settings/' + pair + '_model.joblib')
