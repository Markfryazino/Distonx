from .stupid_model import RandomModel
from .write_all_logger import WriteAllLogger
from paper_testing import Agent, Emulator, Environment
import random


with open('../settings/cryptos.txt') as file:
    cryptos = file.readlines()
balance = {asset: 0. for asset in cryptos}
balance['usdt'] = 200.

model = RandomModel()
agent = Agent(balance, model)
emulator = Emulator()
env = Environment(agent, emulator, WriteAllLogger, 600)
env.start()