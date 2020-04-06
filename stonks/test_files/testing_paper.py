from .stupid_model import ArianaModel
from .write_all_logger import WriteAllLogger, SparseLogger
import logging
from ..paper_testing import Agent, EmulatorV2, Environment
from ..paper_testing.Environment_v2 import EnvironmentV2
from ..modeling import BonnieModel
from stonks.logging.logger import DealsLogger


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
    env = EnvironmentV2(agent, emulator, logger, time, period=1.)
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
    env = EnvironmentV2(agent, emulator, logger, time, start_with=1581434096, period=1.)
    try:
        env.start_historical()
    except KeyboardInterrupt:
        logging.debug('Interruption')
