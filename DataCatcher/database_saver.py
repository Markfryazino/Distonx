import pymysql
import logging


class db:
    def __init__(self):
        self.connection = pymysql.connect('45.12.18.221', 'hinser', 'anime1', 'cryptodata', autocommit=True)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT VERSION()")
        logging.info('version: ' + str(self.cursor.fetchall()))

    def execute(self, command):
        self.cursor.execute(command)
        #  print(self.cursor.fetchall())

    def push_data(self, dct):
        time = dct['time']
        splitted_pairs = self.split_to_pairs(dct)
        for pairname in splitted_pairs:
            request = self.form_request(time, pairname, splitted_pairs[pairname])
            #  print(request)
            self.execute(request)

    def split_to_pairs(self, dct):
        dict_of_pairs = dict()
        for key in dct:
            splited_key = key.split('_')
            if len(splited_key) > 1:
                pairname = splited_key[0]
                if pairname not in dict_of_pairs.keys():
                    dict_of_pairs[pairname] = dict()
                if splited_key[1] == 'kline':
                    dict_of_pairs[pairname]['_'.join(splited_key[1:])] = dct[key]
                elif splited_key[1] == 'asks':
                    if splited_key[3] == 'price':
                        dict_of_pairs[pairname]['depth_ask_price_' + str(int(splited_key[-1]) + 1)] = dct[key]
                    if splited_key[3] == 'quantity':
                        dict_of_pairs[pairname]['depth_ask_quantity_' + str(int(splited_key[-1]) + 1)] = dct[key]
                elif splited_key[1] == 'bids':
                    if splited_key[3] == 'price':
                        dict_of_pairs[pairname]['depth_bid_price_' + str(int(splited_key[-1]) + 1)] = dct[key]
                    if splited_key[3] == 'quantity':
                        dict_of_pairs[pairname]['depth_bid_quantity_' + str(int(splited_key[-1]) + 1)] = dct[key]
        return dict_of_pairs

    def form_request(self, time, pairname, dct):
        base_start = "INSERT INTO `distonx` (`time`, `currency_pair`"
        keys = ""
        values = "'" + str(time) + "', '" + pairname + "'"
        for key, value in dct.items():
            keys += ", `" + str(key) + "`"
            values += ", '" + str(value) + "'"
        return base_start + keys + ") VALUES (" + values + ");"
