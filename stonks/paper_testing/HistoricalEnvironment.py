import logging
import time
from ..DataCatcher import DB


class HistoricalEnvironment:
    def __init__(self, agent, emulator, logger=None,
                 start_time=1581434096, test_time=3600, indent=3600, period=1.):
        """
        :param Agent agent: испытуемый агент
        :param EmulatorV2 emulator: эмулятор биржи
        :param logger: объект логгера
        :param float start_time: время в секундах начала тестирования
        :param float test_time: длина тестирования в секундах
        :param float indent: объем памяти модели
        :param float period: минимальное время между запусками модели
        """
        self.db = DB()
        self.agent = agent
        self.emulator = emulator
        self.logger = logger
        self.start_time = start_time
        self.indent = indent
        self.test_time = test_time
        self.period = period
        self.current_data = {}
        self.memory = {}
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]
        for pair in self.pairs:
            self.memory[pair] = self.db.fetch_pandas(start=start_time - indent,
                                                     end=start_time + test_time, pair_names={pair})
        logging.info('Environment initialization successful')

    def form_orderbook(self):
        orderbook = {pair: {'bids': [], 'asks': []} for pair in self.pairs}
        for pair in self.pairs:
            for i in range(20):
                for side in ('bid', 'ask'):
                    price = float(self.current_data[pair][f'depth_{side}_price_{i + 1}'])
                    quantity = float(self.current_data[pair][f'depth_{side}_quantity_{i + 1}'])
                    orderbook[pair][side + 's'].append([price, quantity])
        return orderbook

    def step(self, data):
        query, logs, balance = self.agent.form_query(data)
        emulator_response = self.emulator.handle(query, balance, self.form_orderbook())
        agent_response = self.agent.get_response(emulator_response)

        step_params = {'query': query, 'model_logs': logs, 'emulator_response': emulator_response,
                       'agent_response': agent_response}

        if self.logger is not None:
            self.logger.step(step_params)

    def start(self):
        ncalls, all_time = 0, 0.
        current_time = self.start_time
        window_data = {}

        while current_time <= self.start_time + self.test_time:
            iteration_start = time.time()
            for pair in self.pairs:
                window_data[pair] = self.memory[pair][(current_time - self.indent <=
                                                       self.memory[pair]['time']) &
                                                      (self.memory[pair]['time'] <= current_time)]
                self.current_data[pair] = window_data[pair].iloc[-1]
            self.step(window_data)
            ncalls += 1
            time_spent = time.time() - iteration_start
            all_time += time_spent
            current_time += max(self.period, time_spent)
        logging.info(str(ncalls) + ' steps done, mean time ' + str(all_time / ncalls))
        logging.info('terminating process')
