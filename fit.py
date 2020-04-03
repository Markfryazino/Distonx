from stonks.auxiliary import fit_model
from stonks.modeling import BonnieModel
import time
import logging
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set()

# Файлик, в котором пишем скрипты для обучения моделей

logging.basicConfig(level='DEBUG')
logging.getLogger('matplotlib').setLevel(logging.WARNING)
fit_model(BonnieModel, time.time() - 604800, time.time(), set(BonnieModel.pairs_implemented))
