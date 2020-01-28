import multiprocessing
import threading
from binance.client import Client
from binance.websockets import BinanceSocketManager
import time
import logging


# Класс таймера, который срабатывает каждые N секунд (скопировал со stackoverflow)
class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


# Инициализация клиента, нужного для взаимодействия с биржей
def init_client():
    with open('../top_secret/key.txt') as file:
        key = file.readlines()[0][:-1]
    with open('../top_secret/api_secret.txt') as file:
        secret = file.readlines()[0][:-1]
    return Client(key, secret)


# Собственно, класс, который осуществляет весь функционал
class DataCatcher:
    # Функция, которая ничего не делает (для потоков, обработку которых мы еще не написали)
    def pass_query(self, query):
        pass

    # Функция для обработки потока ticker
    def ticker_callback(self, query):
        pair = query['stream'].split('@')[0]
        logging.debug('got ticker query for ' + pair)
        name_dict = {'PriceChange': 'p', 'PriceChangePercent': 'P', 'WeightedAveragePrice': 'w',
                     'FirstPrice': 'x', 'LastPrice': 'c', 'LastQuantity': 'Q',
                     'BestBidPrice': 'b', 'BestAskPrice': 'a', 'BestBidQuantity': 'B',
                     'BestAskQuantity': 'A', 'TradeNumber': 'n'}

        # Записываем в наш словарь с данными
        for here in name_dict:
            self.storage[pair + '_ticker_' + here] = query['data'][name_dict[here]]

    # Функция, которая вызывается, когда мы ловим сообщение
    def general_callback(self, query):
        stream_type = query['stream'].split('@')[1]
        # Ниже мы определяем, какой поток какая функция обрабатывает и запускаем
        # обработку в отдельном потоке, чтобы не тормозить
        stream_callbacks = {'trade': self.pass_query, 'kline_1m': self.pass_query,
                            'ticker': self.ticker_callback, 'depth20': self.pass_query}
        action = threading.Thread(target=stream_callbacks[stream_type], args=(query,))
        action.start()

    def init_streams(self):
        # Считываем из настроек, какие мы рассматриваем крипты и потоки и инициализируем потоки
        with open('../settings/pairs.txt') as file:
            self.pairs = file.readlines()
        self.pairs = [el[:-1] for el in self.pairs]
        with open('../settings/streams.txt') as file:
            streams = file.readlines()
        streams = [el[:-1] for el in streams]
        for pair in self.pairs:
            for stream in streams:
                self.streams.append(pair + stream)

    # saver - объект, который сохраняет наши данные. Должен иметь функцию get_data(self, manager_dict) -
    # эту функцию мы будем вызывать каждую секунду
    # timeout - через сколько вырубать обработку, period - длина одного тика
    def __init__(self, saver, timeout=None, period=1.):
        self.timeout = timeout
        self.period = period
        self.manager = multiprocessing.Manager()

        # storage - куда мы сохраняем данные
        self.storage = self.manager.dict()
        self.pairs = []
        self.streams = []
        self.init_streams()
        self.start_time = time.time()
        self.client = init_client()

        # Сокет, который все слушает (запускаем в отдельном процессе)
        self.main_socket = BinanceSocketManager(self.client)
        self.connection_key = self.main_socket.start_multiplex_socket(self.streams, self.general_callback)
        self.socket_process = multiprocessing.Process(target=self.main_socket.run)
        self.data_saver = saver
        self.timer = RepeatTimer(self.period, self.give_data)
        logging.debug('DataCatcher initialization successful')

    # Функция завершения работы
    def finish(self):
        logging.debug('finishing listening')
        self.timer.cancel()
        self.main_socket.stop_socket(self.connection_key)
        self.main_socket.close()
        self.socket_process.terminate()

    # Функция передачи данных saver-у
    def give_data(self):
        logging.debug('giving data, time ' + str(time.time()))
        self.data_saver.get_data(self.storage)

    def start(self):
        logging.debug('started listening')
        self.socket_process.start()

        # Ждем немного, чтобы все успело прийти
        logging.debug('waiting for 10 seconds')
        time.sleep(10.)
        logging.debug('started transferring data')
        if self.timeout:
            timeout_timer = threading.Timer(self.timeout, self.finish)
            timeout_timer.start()

        self.timer.start()
        self.socket_process.join()
