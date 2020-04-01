from stonks.auxiliary import fit_model
from stonks.modeling import BonnieModel
import time
import logging
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

# Файлик, в котором пишем скрипты для обучения моделей

logging.basicConfig(level='DEBUG')
logging.getLogger('matplotlib').setLevel(logging.WARNING)
fit_model(BonnieModel, time.time() - 100000, time.time(), 'btcusdt')
plt.show()
