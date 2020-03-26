from .stupid_model import ArianaModel
from .write_all_logger import WriteAllLogger, SparseLogger
import logging
from ..paper_testing import Agent, EmulatorV2, Environment
from ..modeling import BonnieModel


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
    logger = SparseLogger()
    env = Environment(agent, emulator, logger, time)
    try:
        env.start()
    except KeyboardInterrupt:
        logging.debug('Interruption')
    logger.save()
