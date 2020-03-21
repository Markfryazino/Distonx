import pymysql
import logging
from code.auxiliary import auth_db
from code.auxiliary import split_to_pairs


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
