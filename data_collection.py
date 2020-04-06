from stonks.DataCatcher.DataCatcher import DataCatcher
from stonks.DataCatcher.database_saver import DB
from absl import logging

# Это файлик для запуска кэчера, который собирает данные на серваке

logging._warn_preinit_stderr = 0
logging.set_verbosity(logging.DEBUG)

saver = DB()
timeout = 86000  # сколько секунд до переподключения
period = 1.

while True:
    logging.info('starting new catcher')
    catcher = DataCatcher(saver=saver, timeout=timeout, period=period)
    catcher.start()
