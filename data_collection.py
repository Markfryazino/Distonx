from stonks.DataCatcher.DataCatcher import DataCatcher
from stonks.DataCatcher.database_saver import DB
import logging

# Это файлик для запуска кэчера, который собирает данные на серваке

logging.basicConfig(level=logging.INFO)
saver = DB()
timeout = 86000  # сколько секунд до переподключения
period = 1.

while True:
    logging.info('starting new catcher')
    catcher = DataCatcher(saver=saver, timeout=timeout, period=period)
    catcher.start()
