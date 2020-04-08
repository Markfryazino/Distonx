from ..DataCatcher import DataCatcher
import multiprocessing
import pandas as pd
import threading
import datetime
import logging
import time
from ..DataCatcher import DB


# Класс среды, который полностью организует взаимодействие агента и биржи
class RealTimeEnvironment:
    def __init__(self, agent, emulator, logger=None, timeout=None,
                 period=1., indent=3600):
        self.db = DB()
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
        logging.debug("START GETTING DATA FROM DB")
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]
        for pair in self.pairs:
            self.memory[pair] = self.db.fetch_last(indent=indent, pair_names={pair})
        logging.info('Environment initialization successful')
        logging.debug("DATA RECEIVED, TIME:", time.time() - debug_time)

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
