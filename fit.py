from stonks.auxiliary import fit_model
from stonks.modeling import BonnieModel
from stonks.DataCatcher import DB
import time
import logging
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set()

# Файлик, в котором пишем скрипты для обучения моделей

logging.basicConfig(level='DEBUG')
logging.getLogger('matplotlib').setLevel(logging.WARNING)

pairs = ['bchbnb', 'ltcbnb']

dbase = DB()
for pair in pairs:
    BonnieModel.pairs_implemented = [pair]
    fit_model(BonnieModel, time.time() - 3600 * 24 * 7, time.time(), set(BonnieModel.pairs_implemented),
              dbase=dbase)
