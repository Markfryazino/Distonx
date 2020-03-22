import pymysql
import logging
from ..auxiliary import auth_db
from ..auxiliary import split_to_pairs


class db:
    def __init__(self):
        address, login, password = auth_db()
        self.connection = pymysql.connect(address, login, password, 'cryptodata', autocommit=True)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT VERSION()")
        logging.info('version: ' + str(self.cursor.fetchall()))

    def execute(self, command):
        self.cursor.execute(command)
        #  print(self.cursor.fetchall())

    def push_data(self, dct):
        time = dct['time']
        splitted_pairs = split_to_pairs(dct)
        for pairname in splitted_pairs:
            request = self.form_request(time, pairname, splitted_pairs[pairname])
            self.execute(request)

    def form_request(self, time, pairname, dct):
        base_start = "INSERT INTO `distonx` (`time`, `currency_pair`"
        keys = ""
        values = "'" + str(time) + "', '" + pairname + "'"
        for key, value in dct.items():
            keys += ", `" + str(key) + "`"
            values += ", '" + str(value) + "'"
        return base_start + keys + ") VALUES (" + values + ");"

    def get_data_from_DB(self, time_start, time_finish,
                         pair_name=''):  # возвращает тапл таплов. Один тапл = одна строчка в БД
        if pair_name:
            request = 'SELECT * FROM `distonx` WHERE time >= ' + str(
                time_start) + ' AND time < ' + str(
                time_finish) + ' AND currency_pair = ' + '"' + pair_name + '"'
        else:
            request = 'SELECT * FROM `distonx` WHERE time >= ' + str(
                time_start) + ' AND time < ' + str(time_finish)
        self.execute(request)
        ans = self.cursor.fetchall()
        return ans

    def get_columns_names(
            self):  # Возвращает названия всех стлобцов в том порядке, в котором они находятся в БД
        request = 'SHOW columns FROM distonx;'
        self.execute(request)
        ans = list([i[0] for i in self.cursor.fetchall()])
        return ans
