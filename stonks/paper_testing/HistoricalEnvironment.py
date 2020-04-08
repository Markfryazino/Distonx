import absl.logging as logging
import time
from .AbstractEnvironment import AbstractEnvironment


class HistoricalEnvironment(AbstractEnvironment):
    def __init__(self, agent, emulator, logger=None,
                 start_time=1581434096, test_time=3600, indent=3600, period=1.):
        """
        Среда для тестирования на исторических данных

        :param Agent agent: испытуемый агент
        :param Emulator emulator: эмулятор биржи
        :param logger: объект логгера
        :param float start_time: время в секундах начала тестирования
        :param float test_time: длина тестирования в секундах
        :param float indent: объем памяти модели
        :param float period: минимальное время между запусками модели
        """
        super().__init__(agent, emulator, logger, indent, period)
        self.start_time = start_time
        self.test_time = test_time
        for pair in self.pairs:
            self.memory[pair] = self.db.fetch_pandas(start=start_time - indent,
                                                     end=start_time + test_time, pair_names={pair})
        logging.info('Environment initialization successful')

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
