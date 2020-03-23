from stonks.auxiliary import fit_model
from stonks.modeling import BonnieModel
import time
import logging

logging.basicConfig(level='DEBUG')
fit_model(BonnieModel, time.time() - 604800, time.time(), 'btcusdt')
