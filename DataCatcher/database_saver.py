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
        base_start = "INSERT INTO `distonx` (`time`, `currancy_pair`"
        keys = ""
        values = "'" + str(time) + "', '" + pairname + "'"
        for key, value in dct.items():
            keys += ", `" + str(key) + "`"
            values += ", '" + str(value) + "'"
        return base_start + keys + ") VALUES (" + values + ");"

"""INSERT INTO `distonx` (`time`, `currancy_pair`, `kline_interval`, `kline_timedelta`, `kline_trade_number`, `kline_open_price`, `kline_close_price`, `kline_high_price`, `kline_low_price`, `kline_base_volume`, `kline_quote_volume`, `kline_taker_base_volume`, `kline_taker_quote_volume`, `kline_update_time`, `depth_bid_price_1`, `depth_bid_price_2`, `depth_bid_price_3`, `depth_bid_price_4`, `depth_bid_price_5`, `depth_bid_price_6`, `depth_bid_price_7`, `depth_bid_price_8`, `depth_bid_price_9`, `depth_bid_price_10`, `depth_bid_price_11`, `depth_bid_price_12`, `depth_bid_price_13`, `depth_bid_price_14`, `depth_bid_price_15`, `depth_bid_price_16`, `depth_bid_price_17`, `depth_bid_price_18`, `depth_bid_price_19`, `depth_bid_price_20`, `depth_bid_quantity_1`, `depth_bid_quantity_2`, `depth_bid_quantity_3`, `depth_bid_quantity_4`, `depth_bid_quantity_5`, `depth_bid_quantity_6`, `depth_bid_quantity_7`, `depth_bid_quantity_8`, `depth_bid_quantity_9`, `depth_bid_quantity_10`, `depth_bid_quantity_11`, `depth_bid_quantity_12`, `depth_bid_quantity_13`, `depth_bid_quantity_14`, `depth_bid_quantity_15`, `depth_bid_quantity_16`, `depth_bid_quantity_17`, `depth_bid_quantity_18`, `depth_bid_quantity_19`, `depth_bid_quantity_20`, `depth_ask_price_1`, `depth_ask_price_2`, `depth_ask_price_3`, `depth_ask_price_4`, `depth_ask_price_5`, `depth_ask_price_6`, `depth_ask_price_7`, `depth_ask_price_8`, `depth_ask_price_9`, `depth_ask_price_10`, `depth_ask_price_11`, `depth_ask_price_12`, `depth_ask_price_13`, `depth_ask_price_14`, `depth_ask_price_15`, `depth_ask_price_16`, `depth_ask_price_17`, `depth_ask_price_18`, `depth_ask_price_19`, `depth_ask_price_20`, `depth_ask_quantity_1`, `depth_ask_quantity_2`, `depth_ask_quantity_3`, `depth_ask_quantity_4`, `depth_ask_quantity_5`, `depth_ask_quantity_6`, `depth_ask_quantity_7`, `depth_ask_quantity_8`, `depth_ask_quantity_9`, `depth_ask_quantity_10`, `depth_ask_quantity_11`, `depth_ask_quantity_12`, `depth_ask_quantity_13`, `depth_ask_quantity_14`, `depth_ask_quantity_15`, `depth_ask_quantity_16`, `depth_ask_quantity_17`, `depth_ask_quantity_18`, `depth_ask_quantity_19`, `depth_ask_quantity_20`) VALUES ('23480234.238947', 'btcusd', '2423', '2384.3487', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);"""
