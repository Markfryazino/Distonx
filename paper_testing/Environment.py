from DataCatcher.DataCatcher import DataCatcher
import multiprocessing
import logging
import time


class Environment:
    def update_data(self, data):
        for key in data:
            self.current_data[key] = data[key]

    def __init__(self, agent, emulator, logger=None, timeout=None, period=1.):
        self.agent = agent
        self.emulator = emulator
        self.logger = logger
        self.manager = multiprocessing.Manager()
        self.current_data = self.manager.dict()
        self.catcher = DataCatcher(self.update_data, timeout)
        self.catcher_process = multiprocessing.Process(target=self.catcher.start)
        self.timeout = timeout
        self.period = period
        logging.info('Environment initialization successful')

    def form_orderbook(self):
        with open('../settings/pairs.txt') as file:
            pairs = [a[:-1] for a in file.readlines()]
        orderbook = {pair: {'bids': [], 'asks': []} for pair in pairs}
        for pair in pairs:
            for i in range(20):
                for side in ('bids', 'asks'):
                    price = self.current_data[pair + '_' + side + '_orderbook_price_level_' + str(i)]
                    quantity = self.current_data[pair + '_' + side + '_orderbook_quantity_level_' + str(i)]
                    orderbook[pair][side].append([price, quantity])

    def step(self, data):
        query, balance = self.agent.form_query(data)
        emulator_response = self.emulator.handle(query, balance, self.form_orderbook())
        agent_response = self.agent.get_response(emulator_response)

        step_params = {'query': query, 'emulator_response': emulator_response,
                       'agent_response': agent_response}
        if self.logger:
            self.logger.step(step_params)

    def start(self):
        self.catcher_process.start()
        logging.info('waiting for 4 minutes for DataCatcher to wake up')
        time.sleep(240.)
        logging.info('starting action')

        while self.catcher_process.is_alive():
            start_time = time.time()
            # self.step(self.current_data)
            logging.debug('step done, time ' + str((time.time() - start_time) / 1000.) + ' seconds')
