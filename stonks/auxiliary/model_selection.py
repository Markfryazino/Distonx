import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import xgboost
sns.set()


def fit_predict(X, y, model=None):
    """Обучает модель и возвращает вероятности для тестовой выборки"""
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
    plt.plot(X_test.index, X_test['target'])
    plt.scatter(X_test[y_test == 1].index, target[y_test == 1], color='g')
    plt.scatter(X_test[y_test == 0].index, target[y_test == 0], color='r')
    plt.show()
    plt.figure(figsize=(15, 5))
    plt.plot(X_test.index, target)
    plt.scatter(X_test[ups].index, target[ups], color='r')
    plt.scatter(X_test[downs].index, target[downs], color='g')
