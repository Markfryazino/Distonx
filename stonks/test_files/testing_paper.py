from .stupid_model import ArianaModel
from .write_all_logger import WriteAllLogger, SparseLogger
from absl import logging
from ..paper_testing import Agent, Emulator
from ..paper_testing.HistoricalEnvironment import HistoricalEnvironment
from ..paper_testing.RealTimeEnvironment import RealTimeEnvironment
from ..modeling import BonnieModel
from stonks.logging.logger import DealsLogger
from ..DataCatcher.database_saver import DB


# Тест с Арианой
def paper_test_1(start_balance=200., time=60.):

    open("trash/Ariana_output.txt", "w").close()
    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = start_balance

    model = ArianaModel()
    agent = Agent(balance, model)
    emulator = Emulator()
    env = RealTimeEnvironment(agent, emulator, WriteAllLogger(), time)
    env.start()


# Тест с Бонни
def bonnie_test(start_balance=200., time=60.):

    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = start_balance

    model = BonnieModel()
    agent = Agent(balance, model)
    emulator = Emulator()
    logger = DealsLogger('Bonnie_test_RealTime_1')
    db = DB()
    env = RealTimeEnvironment(agent, emulator, logger, time, period=1.)
    try:
        env.start()
    except KeyboardInterrupt:
        logging.debug('Interruption')


def another_bonnie_test(start_balance=200., time=60.):

    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = start_balance

    model = BonnieModel()
    agent = Agent(balance, model)
    emulator = Emulator()
    logger = DealsLogger('Bonnie_test_Hist_1')
    env = HistoricalEnvironment(agent, emulator, logger)
    try:
        env.start()
    except KeyboardInterrupt:
        logging.debug('Interruption')
