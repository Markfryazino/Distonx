from .DataCatcher import DataCatcher, RepeatTimer
from .database_saver import db
import logging


logging.basicConfig(level=logging.ERROR)
saver = db()
timeout = 86000  # сколько секунд до переподключения
period = 1.

while True:
    logging.info('starting new catcher')
    catcher = DataCatcher(saver, timeout, period)
    catcher.start()
