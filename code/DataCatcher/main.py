from ..DataCatcher import DataCatcher, db
import logging


logging.basicConfig(level=logging.ERROR)
saver = db()
timeout = 86000  # сколько секунд до переподключения
period = 1.

while True:
    logging.info('starting new catcher')
    catcher = DataCatcher(saver=saver, timeout=timeout, period=period)
    catcher.start()
