from .stupid_model import ArianaModel
from .write_all_logger import WriteAllLogger
import logging
from code.paper_testing import Agent, Emulator, Environment


def paper_test_1(start_balance=200., time=30.):
    logging.basicConfig(level=logging.DEBUG)

    open("trash/Ariana_output.txt", "w").close()
    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = start_balance

    model = ArianaModel()
    agent = Agent(balance, model)
    emulator = Emulator()
    env = Environment(agent, emulator, WriteAllLogger(), time)
    env.start()
