from ..DataCatcher import DataCatcher
import multiprocessing
import pandas as pd
import threading
import datetime
import absl.logging as logging
import time
from .AbstractEnvironment import AbstractEnvironment
from ..auxiliary import split_to_pairs


def transform(data):
    dct = split_to_pairs(data)
    final = {}
    for pair in dct.keys():
        cur = data[pair].copy()
        cur = {key: float(val) for (key, val) in cur.items()}
        cur['kline_time_since_update'] = time.time() * 1000 - cur['kline_update_time']
        cur = {key: [val] for key, val in cur.items()}
        df = pd.DataFrame(cur)
        final[pair] = df
    return final


class RealTimeEnvironment(AbstractEnvironment):
    def __init__(self, agent, emulator, logger=None, timeout=None,
                 period=1., indent=3600):
        """
        Среда для тестирования на данных в реальном времени

        :param Agent agent: испытуемый агент
        :param Emulator emulator: эмулятор биржи
        :param logger: объект логгера
        :param float timeout: время тестирования в секундах
        :param float indent: объем памяти модели
        :param float period: минимальное время между запусками модели
        """

        super().__init__(agent, emulator, logger, indent=indent, period=period)
        self.manager = multiprocessing.Manager()
        self.current_data = self.manager.dict()
        self.short_term_memory = self.manager.list()
        self.catcher = DataCatcher(storage=self.current_data, process_inside=False)
        self.socket_process = multiprocessing.Process(target=self.catcher.main_socket.run)
        self.data_process = multiprocessing.Process(target=self.handle_data)
        self.timeout = timeout
        self.time_to_stop = False
        
        for pair in self.pairs:
            self.memory[pair] = self.db.fetch_last(indent=indent, pair_names={pair})
        logging.info('Environment initialization successful')

    def handle_data(self):
        while True:
            start_time = time.time()
            data = transform(self.current_data)
            self.short_term_memory.append(data)
            now = time.time()
            if now < start_time + self.period:
                time.sleep(start_time + self.period - now)

    def finish(self):
        self.time_to_stop = True

    def start(self):
        self.socket_process.start()
        logging.info('waiting for 80 seconds for DataCatcher to wake up')
        time.sleep(80.)
        logging.info('starting action')

        self.data_process.start()
        timeout_timer = threading.Timer(self.timeout, self.finish)
        timeout_timer.start()

        ncalls, all_time = 0, 0.

        while not self.time_to_stop:
            start_time = time.time()

            for pair in self.pairs:
                for row in self.short_term_memory:
                    self.memory[pair] = self.memory[pair].append(row[pair])
                self.memory[pair] = self.memory[pair][self.memory[pair]['time'] >=
                                                      self.memory[pair]['time'].iloc[-1] - self.indent]
            self.short_term_memory.clear()

            self.step(self.memory)
            ncalls += 1
            time_spent = time.time() - start_time
            all_time += time_spent
            if time_spent < self.period:
                time.sleep(self.period - time_spent)

        self.socket_process.terminate()
        self.data_process.terminate()
        self.data_process.join()
        self.socket_process.join()
        logging.info(str(ncalls) + ' steps done, mean time ' + str(all_time / ncalls))
        logging.info('terminating process')
