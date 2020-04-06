from ..DataCatcher import DataCatcher
from ..auxiliary import split_to_pairs
from ..DataCatcher.database_saver import DB
import multiprocessing
import pandas as pd
import threading
import datetime
import logging
import time


# Класс среды, который полностью организует взаимодействие агента и биржи
class EnvironmentV2:
    def __init__(self, agent, emulator, logger=None,
                 timeout=None, period=10., start_with=-1, indent=3600, ):
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
        self.start_with = start_with
        self.indent = indent
        self.memory = {}
        db = DB()
        # Инициализация memory
        debug_time = time.time()
        print("START GETTING DATA FROM DB")
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]
        if start_with == -1:
            for pair in self.pairs:
                self.memory[pair] = db.fetch_last(indent=indent, pair_names={pair})
        else:
            for pair in self.pairs:
                self.memory[pair] = db.fetch_pandas(start=start_with - indent,
                                                    end=start_with + indent, pair_names={pair})
        logging.info('Environment initialization successful')
        print("DATA RECEIVED, TIME:", time.time() - debug_time)

    # Формирование ордербука для эмулятора
    def form_orderbook(self):  # works ~0.6 sec
        start = time.time()
        orderbook = {pair: {'bids': [], 'asks': []} for pair in self.pairs}
        for pair in self.pairs:
            for i in range(20):
                for side in ('bid', 'ask'):
                    if self.start_with == -1:
                        price = float(self.current_data[f'pair_{side}_orderbook_price_level_{i}'])
                        quantity = float(self.current_data[f'{pair}_{side}_orderbook_quantity_level_{i}'])
                    else:
                        price = float(self.current_data[pair][f'depth_{side}_price_{i + 1}'])
                        quantity = float(self.current_data[pair][f'depth_{side}_quantity_{i + 1}'])
                    orderbook[pair][side + 's'].append([price, quantity])
        print("ORDERBOOK FORMING:", time.time() - start)
        return orderbook

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

    @staticmethod
    def debug_output(self, data):
        data['btcusdt'].to_csv('trash/DEBUGOUTPUT.txt')

    # Один тик
    def step(self, data):
        query, logs, balance = self.agent.form_query(data)
        emulator_response = self.emulator.handle(query, balance, self.form_orderbook())
        start = time.time()
        agent_response = self.agent.get_response(emulator_response)
        print("GETING RESPONSE:", time.time() - start)
        step_params = {'query': query, 'model_logs': logs, 'emulator_response': emulator_response,
                       'agent_response': agent_response, 'data': self.current_data}

        if self.logger is not None:
            self.logger.step(step_params)

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

    def start_historical(self):
        ncalls, all_time = 0, 0.
        current_time = self.start_with
        window_data = {}
        for pair in self.pairs:
            window_data[pair] = self.memory[pair][self.memory[pair]['time'] <= current_time]

        while current_time <= self.start_with + self.indent:
            start_time = time.time()
            for pair in self.pairs:  # works ~0.04 sec
                window_data[pair] = self.memory[pair][(current_time - self.indent <=
                                                       self.memory[pair]['time']) &
                                                      (self.memory[pair]['time'] <= current_time)]
                self.current_data[pair] = window_data[pair].iloc[-1]
            print("LINE 134 FOR:", time.time() - start_time)
            # self.debug_output(self.current_data)
            self.step(window_data)
            ncalls += 1
            time_spent = time.time() - start_time
            all_time += time_spent
            current_time += max(1., time_spent)
            print("SPENT:", time_spent)
        logging.info(str(ncalls) + ' steps done, mean time ' + str(all_time / ncalls))
        logging.info('terminating process')
