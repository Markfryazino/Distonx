import pymysql
from absl import logging
import pandas as pd
from ..auxiliary import auth_db
from ..auxiliary import split_to_pairs
import time


class DB:
    authorized = False
    credentials = ()

    def __init__(self):
        address, login, password = auth_db()
        self.connection = pymysql.connect(address, login, password, 'cryptodata', autocommit=True)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT VERSION()")
        logging.info('version: ' + str(self.cursor.fetchall()))

    def execute(self, command):
        self.cursor.execute(command)

    def push_data(self, dct):
        cur_time = dct['time']
        splitted_pairs = split_to_pairs(dct)
        for pairname in splitted_pairs:
            request = DB.form_request(cur_time, pairname, splitted_pairs[pairname])
            self.execute(request)

    @staticmethod
    def form_request(cur_time, pairname, dct):
        base_start = "INSERT INTO `distonx` (`time`, `currency_pair`"
        keys = ""
        values = "'" + str(cur_time) + "', '" + pairname + "'"
        for key, value in dct.items():
            keys += ", `" + str(key) + "`"
            values += ", '" + str(value) + "'"
        return base_start + keys + ") VALUES (" + values + ");"

    def get_data_from_db(self, time_start, time_finish,
                         pair_name='', pair_names=None):  # возвращает тапл таплов. Один тапл = одна строчка в БД
        if pair_names is None:
            pair_names = set()
        if pair_names:
            tmp = '('
            count = len(pair_names)
            for pair_name in pair_names:
                tmp += 'currency_pair = ' + '"' + pair_name + '"'
                count -= 1
                if count != 0:
                    tmp += ' OR '
            tmp += ')'
            request = 'SELECT * FROM `distonx` WHERE time >= ' + str(
                time_start) + ' AND time < ' + str(
                time_finish) + ' AND ' + tmp
        elif pair_name:
            request = 'SELECT * FROM `distonx` WHERE time >= ' + str(
                time_start) + ' AND time < ' + str(
                time_finish) + ' AND currency_pair = ' + '"' + pair_name + '"'
        else:
            request = 'SELECT * FROM `distonx` WHERE time >= ' + str(
                time_start) + ' AND time < ' + str(time_finish)
        self.execute(request)
        ans = self.cursor.fetchall()
        return ans

    def get_data_by_id(self, sid):  # возвращает строку по id
        request = 'SELECT * FROM  `distonx` WHERE id = ' + str(sid)
        self.execute(request)
        ans = self.cursor.fetchone()
        return ans

    # Возвращает названия всех стлобцов в том порядке, в котором они находятся в БД
    def get_columns_names(self):
        request = 'SHOW columns FROM distonx;'
        self.execute(request)
        ans = list([i[0] for i in self.cursor.fetchall()])
        return ans

    def fetch_pandas(self, start, end, pair_names=None):
        if pair_names is None:
            pair_names = set()
        names = self.get_columns_names()
        data = self.get_data_from_db(start, end, pair_names=pair_names)
        data = pd.DataFrame(data=data, columns=names)
        return data

    def fetch_last(self, indent=3600, pair_names=None):
        if pair_names is None:
            pair_names = set()
        return self.fetch_pandas(time.time() - indent, time.time(), pair_names)
