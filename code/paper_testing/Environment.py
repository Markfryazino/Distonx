from code.DataCatcher import DataCatcher
import multiprocessing
import threading
import logging
import time


class Environment:
    def __init__(self, agent, emulator, logger=None, timeout=None, period=1.):
        self.agent = agent
        self.emulator = emulator
        self.logger = logger
        self.manager = multiprocessing.Manager()
        self.current_data = self.manager.dict()
        self.catcher = DataCatcher(storage=self.current_data, process_inside=False)
        self.socket_process = multiprocessing.Process(target=self.catcher.main_socket.run)
        self.timeout = timeout
        self.period = period
        self.time_to_stop = False
        logging.info('Environment initialization successful')

    def form_orderbook(self):
        with open('settings/pairs.txt') as file:
            pairs = [a[:-1] for a in file.readlines()]
        orderbook = {pair: {'bids': [], 'asks': []} for pair in pairs}
        for pair in pairs:
            for i in range(20):
                for side in ('bids', 'asks'):
                    price = float(self.current_data[pair + '_' + side + '_orderbook_price_level_' + str(i)])
                    quantity = float(self.current_data[pair + '_' + side + '_orderbook_quantity_level_'
                                                       + str(i)])
                    orderbook[pair][side].append([price, quantity])

        return orderbook

    def step(self, data):
        query, balance = self.agent.form_query(data)
        emulator_response = self.emulator.handle(query, balance, self.form_orderbook())
        agent_response = self.agent.get_response(emulator_response)

        step_params = {'query': query, 'emulator_response': emulator_response,
                       'agent_response': agent_response, 'data': self.current_data}

        if self.logger is not None:
            self.logger.step(step_params)

    def finish(self):
        self.time_to_stop = True

    def start(self):
        self.socket_process.start()
        logging.info('waiting for 2 minutes for DataCatcher to wake up')
        time.sleep(120.)
        logging.info('starting action')

        timeout_timer = threading.Timer(self.timeout, self.finish)
        timeout_timer.start()

        ncalls, all_time = 0, 0.

        while not self.time_to_stop:
            start_time = time.time()
            self.step(self.current_data)
            ncalls += 1
            all_time += time.time() - start_time

        self.socket_process.terminate()
        self.socket_process.join()
        logging.info(str(ncalls) + ' steps done, mean time ' + str(all_time / ncalls))
        logging.info('terminating process')
