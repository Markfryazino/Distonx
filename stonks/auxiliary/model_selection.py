import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score
from sklearn.metrics import classification_report
import numpy as np
import xgboost
sns.set()


def fit_predict(X, y, model=None, drop_minus_one=True):
    """Обучает модель и возвращает вероятности для тестовой выборки"""

    if drop_minus_one:
        X = X[y != -1]
        y = y[y != -1]

    if model is None:
        model = LogisticRegression(n_jobs=-1, solver='lbfgs')
    x_train, x_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    print(classification_report(y_test, pred))

    proba = model.predict_proba(x_test)
    probas = pd.DataFrame(proba, columns=['goes_down', 'goes_up'], index=x_test.index)

    return model, x_train, x_test, y_train, y_test, probas


def get_importances(model: xgboost.XGBClassifier):
    """Возвращает важности моделей обученного xgboost-а"""
    imp = model.feature_importances_
    names = model.get_booster().feature_names
    li = list(zip(imp, names))
    li.sort(reverse=True)
    return li


def plot_predictions(X_test, y_test, target, probas, prob_up=0.5, prob_down=0.5):
    """Отрисовывает предсказания модели"""

    ups = probas['goes_down'] > prob_down
    downs = probas['goes_up'] > prob_up

    plt.figure(figsize=(15, 5))
    plt.plot(X_test.index, target)
    plt.scatter(X_test[y_test == 1].index, target[y_test == 1], color='g')
    plt.scatter(X_test[y_test == 0].index, target[y_test == 0], color='r')
    plt.show()
    plt.figure(figsize=(15, 5))
    plt.plot(X_test.index, target)
    plt.scatter(X_test[ups].index, target[ups], color='r')
    plt.scatter(X_test[downs].index, target[downs], color='g')


def approx_metric(target, state, start=100, com=0.999):
    """Приближенный результат тестирования на бумаге"""
    quote = start
    base = 0
    last = 0
    ind_red = []
    ind_green = []
    for ind in state.index:
        if state[ind] == 0:
            quote += target[ind] * base * com
            if base != 0:
                ind_red.append(ind)
            base = 0
            last = target[ind]
        else:
            base += quote / target[ind] * com
            if quote != 0:
                ind_green.append(ind)
            quote = 0
            last = target[ind]
    return ind_red, ind_green, (quote + base * last) / start


def choose_prob(y_true, probas, number=200):
    """Выбор пороговых вероятностей с учетом точности"""
    best_p = 0
    best_prob = ()
    for p_down in np.arange(0.5, 1., 0.05):
        for p_up in np.arange(0.5, 1., 0.05):
            up = y_true[:, 1]
            down = y_true[:, 0]

            pred_up = probas['goes_up'] > p_up
            pred_down = probas['goes_down'] > p_down

            num = pred_up.sum() + pred_down.sum()
            if min(pred_up.sum() / (y_true.shape[0] / 3600.), pred_down.sum() /
                                                              (y_true.shape[0] / 3600.)) < number:
                continue
            min_p = min(precision_score(up, pred_up), precision_score(down, pred_down))
            if min_p > best_p:
                best_p = min_p
                best_prob = (p_down, p_up)
    print(f'Probabilities: {best_prob}\nPrecision: {best_p}')