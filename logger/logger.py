from ..stonks.DataCatcher import database_saver
import time

#отслеживает баланс и сделки
class DealsLogger:
    def __init__(self):
        self.db = database_saver.DB()

    def deal(self, data, type='test', comment=''):
        req_dct = dict()
        req_dct['time'] = time.time()
        for currency, balance in data['agent_response']['balance'].items():
            req_dct['new_balance' + currency] = str(balance)
        req_dct['balance'] = data['emulator_response']['new_usdt']
        for pairname, doing, amount in data['agent']:
            if doing == 'sell base':
                req_dct[pairname] = str(-amount)
            else:
                req_dct[pairname] = str(amount)
        req_dct['type'] = type
        req_dct['comment'] = comment
        request = 'INSERT INTO `deals` (`' + '`, `'.join(req_dct.keys()) + '`) VALUES (`' + "', '".join(req_dct.values()) + "')"
        self.db.execute(request)
