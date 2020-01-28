from DataCatcher import DataCatcher
from DataSaver import TxtDataSaver
import logging

logging.basicConfig(level=logging.DEBUG)

saver = TxtDataSaver()
catcher = DataCatcher(saver, 5., 1.)
catcher.start()
saver.save_data('../trash/savings.txt')
