from ..DataCatcher import DataCatcher
import multiprocessing
import pandas as pd
import threading
import datetime
import logging
import time


class EnvHistorical:
    def __init__(self, agent, emulator, logger=None,
                 start_time=1581434096, indent=3600, db=None):
        self.agent = agent
        self.emulator = emulator
        self.logger = logger
        self.start_time = start_time
        self.indent = indent
        self.current_data = {}
        self.memory = {}
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]
        for pair in self.pairs:
            self.memory[pair] = db.fetch_pandas(start=start_time - indent,
                                                end=start_time + indent, pair_names={pair})
        logging.info('Environment initialization successful')

    def form_orderbook(self):
        # start = time.time()
        orderbook = {pair: {'bids': [], 'asks': []} for pair in self.pairs}
        for pair in self.pairs:
            for i in range(20):
                for side in ('bid', 'ask'):
                    price = float(self.current_data[pair][f'depth_{side}_price_{i + 1}'])
                    quantity = float(self.current_data[pair][f'depth_{side}_quantity_{i + 1}'])
                    orderbook[pair][side + 's'].append([price, quantity])
        # print("ORDERBOOK FORMING:", time.time() - start)
        return orderbook

    def step(self, data):
        # start = time.time()
        query, logs, balance = self.agent.form_query(data)
        # print("FORMING QUERY:", time.time() - start)
        # start = time.time()
        emulator_response = self.emulator.handle(query, balance, self.form_orderbook())
        # print("HANDLING:", time.time() - start)
        agent_response = self.agent.get_response(emulator_response)

        step_params = {'query': query, 'model_logs': logs, 'emulator_response': emulator_response,
                       'agent_response': agent_response}

        if self.logger is not None:
            self.logger.step(step_params)

    def start(self):
        ncalls, all_time = 0, 0.
        current_time = self.start_time
        window_data = {}
        for pair in self.pairs:
            window_data[pair] = self.memory[pair][self.memory[pair]['time'] <= current_time]

        while current_time <= self.start_time + self.indent:
            start_time = time.time()
            for pair in self.pairs:
                window_data[pair] = self.memory[pair][(current_time - self.indent <=
                                                       self.memory[pair]['time']) &
                                                      (self.memory[pair]['time'] <= current_time)]
                self.current_data[pair] = window_data[pair].iloc[-1]
            self.step(window_data)
            ncalls += 1
            time_spent = time.time() - start_time
            all_time += time_spent
            current_time += max(1., time_spent)
            # print("SPENT:", time_spent)
        logging.info(str(ncalls) + ' steps done, mean time ' + str(all_time / ncalls))
        logging.info('terminating process')


# Класс среды, который полностью организует взаимодействие агента и биржи
class EnvRealTime(EnvHistorical):
    def __init__(self, agent, emulator, logger=None, timeout=None,
                 period=10., indent=3600, db=None):
        super().__init__(agent, emulator, logger, indent)
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
        self.indent = indent
        self.memory = {}
        debug_time = time.time()
        print("START GETTING DATA FROM DB")
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]
        for pair in self.pairs:
            self.memory[pair] = db.fetch_last(indent=indent, pair_names={pair})
            print(self.memory[pair])
        logging.info('Environment initialization successful')
        print("DATA RECEIVED, TIME:", time.time() - debug_time)

    def handle_data(self, data):
        dct = data
        for pair in dct.keys():
            if pair not in self.memory:
                continue
            cur = dct[pair].copy()
            cur = {key: float(val) for (key, val) in cur.items()}
            cur['kline_time_since_update'] = time.time() * 1000 - cur['kline_update_time']
            cur = {key: [val] for key, val in cur.items()}
            df = pd.DataFrame(cur, index=pd.Series([datetime.datetime.fromtimestamp(time.time())],
                                                   name='normal_data'))
            self.memory[pair] = self.memory[pair].append(df)

    def finish(self):
        self.time_to_stop = True

    # Все выполняется в этой функции
    def start(self):
        self.socket_process.start()
        logging.info('waiting for 80 seconds for DataCatcher to wake up')
        time.sleep(80.)
        logging.info('starting action')

        timeout_timer = threading.Timer(self.timeout, self.finish)
        timeout_timer.start()

        ncalls, all_time = 0, 0.

        while not self.time_to_stop:
            start_time = time.time()
            self.handle_data(self.current_data)
            # убираем лишние строчки из memory
            for pair in self.pairs:
                self.memory[pair] = self.memory[pair][self.memory[pair]['time'] >=
                                                      self.memory[pair]['time'].iloc[-1] - self.indent]
            self.step(self.memory)
            ncalls += 1
            time_spent = time.time() - start_time
            all_time += time_spent
            if time_spent < self.period:
                time.sleep(self.period - time_spent)

        self.socket_process.terminate()
        self.socket_process.join()
        logging.info(str(ncalls) + ' steps done, mean time ' + str(all_time / ncalls))
        logging.info('terminating process')
