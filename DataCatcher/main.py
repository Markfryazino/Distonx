from DataCatcher import DataCatcher, RepeatTimer
from database_saver import db
import logging


logging.basicConfig(level=logging.INFO)
saver = db()
timeout = 5.  # 20 часов
period = 1.

while True:
    logging.info('starting new catcher')
    catcher = DataCatcher(saver, timeout, period)
    catcher.start()
