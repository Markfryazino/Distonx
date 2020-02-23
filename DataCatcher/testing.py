from DataCatcher import DataCatcher, RepeatTimer
from database_saver import db
import logging


class StupidSaver:
    def __init__(self):
        pass

    def push_data(self, data):
        pass


logging.basicConfig(level=logging.INFO)
saver = StupidSaver()
timeout = 20. # сколько секунд до переподключения
period = 1.

while True:
    logging.info('starting new catcher')
    catcher = DataCatcher(saver=saver, timeout=timeout, period=period)
    catcher.start()
