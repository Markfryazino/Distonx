from .stupid_model import ArianaModel
from .write_all_logger import WriteAllLogger, SparseLogger
import logging
from ..paper_testing import Agent, EmulatorV2, Environment
from ..paper_testing.Environment_v2 import EnvHistorical, EnvRealTime
from ..modeling import BonnieModel
from stonks.logging.logger import DealsLogger
from ..DataCatcher.database_saver import DB

# Тест с Арианой
def paper_test_1(start_balance=200., time=60.):
    logging.basicConfig(level=logging.DEBUG)

    open("trash/Ariana_output.txt", "w").close()
    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = start_balance

    model = ArianaModel()
    agent = Agent(balance, model)
    emulator = EmulatorV2()
    env = Environment(agent, emulator, WriteAllLogger(), time)
    env.start()


# Тест с Бонни
def bonnie_test(start_balance=200., time=60.):
    logging.basicConfig(level=logging.DEBUG)

    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = start_balance

    model = BonnieModel()
    agent = Agent(balance, model)
    emulator = EmulatorV2()
    logger = DealsLogger('Bonnie_test_LR')
    db = DB()
    env = EnvRealTime(agent, emulator, logger, time, db=db, period=1.)
    try:
        env.start()
    except KeyboardInterrupt:
        logging.debug('Interruption')


def another_bonnie_test(start_balance=200., time=60.):

    logging.basicConfig(level=logging.DEBUG)

    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = start_balance

    model = BonnieModel()
    agent = Agent(balance, model)
    emulator = EmulatorV2()
    logger = DealsLogger('Bonnie_test_LR')
    db = DB()
    env = EnvHistorical(agent, emulator, logger, db=db)
    try:
        env.start()
    except KeyboardInterrupt:
        logging.debug('Interruption')
