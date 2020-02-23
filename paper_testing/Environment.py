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
        self.catcher_process = multiprocessing.Process(target=self.catcher.start())
        self.timeout = timeout
        self.period = period
        logging.info('initialization successful')

    def step(self, data):
        query = self.agent.form_query(data)
        emulator_response = self.emulator.handle(query, data)
        agent_response = self.agent.get_response(emulator_response)

        step_params = {'query': query, 'delta_balance': agent_response['delta_balance'],
                       'balance': agent_response['balance']}
        if self.logger:
            self.logger.update(step_params)

    def start(self):
        self.catcher_process.start()
        logging.info('waiting for 4 minutes for DataCatcher to wake up')
        time.sleep(240.)

        while self.catcher_process.is_alive():
            start_time = time.time()
            self.step(self.current_data)
            end_time = time.time()
            if end_time < start_time + self.period * 1000.:
                time.sleep((start_time + self.period * 1000 - end_time) / 1000.)
