from ..DataCatcher.database_saver import DB
import time

class LogSaver:

    def __init__(self):
        self.db = DB()
        self.db.execute('SHOW COLUMNS FROM deals;')
        self.COLUMN_NAMES = list([i[0] for i in self.db.cursor.fetchall()])
        self.db.execute()
        self.db.execute('SELECT time FROM deals;')
        self.TIMEZERO = int(self.db.cursor.fetchone())
        self.cache = dict()

    #возвращает словарь {'time': [], 'balance': []}
    def GetBalance(self, time_start = 0, time_finish = 0, balance_name = 'new_balance', type = None):
        # balace_name - название поля баланса в базе данных, по умолчанию береётся общий баланс, можно поставить, например, new_balance_btc
        # type - краткий комментарий, предполагается использование для задавания моделям имён
        request = 'SELECT time, ' + balance_name + ' FROM `deals` WHERE 1 '
        if time_start != 0:
            request += ' AND time >= ' + str(time_start)
        if time_finish != 0:
            request += ' AND time < ' + str(time_finish)
        if type is not None:
            request += 'AND type = ' + "'" + str(type) +  "'"
        self.db.execute(request)
        data = dict()
        data['time'] = []
        data['balance'] = []
        raw_data = self.db.cursor.fetchall()
        for time, balance in raw_data:
            data['time'].append(time)
            data['balance'].append(balance)
        return data

    #возвращает целое число - количество сделок на валютной паре pairname (по умолчанию общее)
    # и типом (именем модели) type
    def GetDealsAmount(self, time_start = 0, time_finish = 0, type = None, pairname = ''):
        request = 'SELECT id FROM `deals` WHERE 1 '
        if time_start != 0:
            request += ' AND time >= ' + str(time_start)
        if time_finish != 0:
            request += ' AND time < ' + str(time_finish)
        if pairname:
            request += ' AND ' + pairname + '_query_type != NULL'
        if type:
            request += ' AND type = ' + "'" + type + "'"
        self.db.execute(request)
        return len(self.db.cursor.fetchall())

    #возвращает словарь {'candle_time_start': [], 'amount': []}
    #period - продолжительность одной свечи, amount - количество сделок за этот промежуток
    def GetDealsAmountDict(self, time_start = 0, time_finish= 0, type = None, pairname = '', period = 60):
        data = dict()
        data['candle_time_start'] = []
        data['amount'] = []
        if time_start == 0:
            time_start = self.TIMEZERO
        for time_cur in range(time_start, time_finish, period):

            if (time_cur, period, type, pairname) not in self.cache or \
                    (time_finish == 0  and time_cur + period > time.time()
                     or time_finish != 0 and time_cur + period > time_finish):
                self.cache[(time_cur, period, type, pairname)] = self.GetDealsAmount(time_cur, time_cur + period, type, pairname)
            if (time_cur, period, type, pairname) in self.cache:
                data['candle_time_start'].append(time_cur)
                data['amount'].append(self.cache[(time_cur, period, type, pairname)])
        return data



    #возвращает тапл таплов. в каждом тапле - строка из базы данных
    def GetDeals(self, time_start = 0, time_finish = 0, type = None, pairname = ''):
        request = 'SELECT * FROM `deals` WHERE 1 '
        if time_start != 0:
            request += ' AND time >= ' + str(time_start)
        if time_finish != 0:
            request += ' AND time < ' + str(time_finish)
        if pairname:
            request += ' AND ' + pairname + '_query_type != NULL'
        if type:
            request += ' AND type = ' + "'" + type + "'"
        self.db.execute(request)
        return self.db.cursor.fetchall()


ls = LogSaver()
print(ls.GetBalance())
print(ls.GetDealsAmountDict())
