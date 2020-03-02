import math


class EmulatorV2:
    def __init__(self, spend_till_end=True, pay_in_bnb=True):
        self.spend_till_end = spend_till_end
        self.bnb_fee = 0.00075
        self.fee = 0.001
        self.pay_in_bnb = pay_in_bnb
        self.balance = {}
        self.orders = {}

        with open('settings/cryptos.txt') as file:
            self.cryptos = file.readlines()
        self.cryptos = [el[:-1] for el in self.cryptos]

        with open('settings/min_order_size_and_step.txt', 'r') as f:
            self.min_order_size = eval(f.read())

    # TODO - реализовать более умно
    def count_in_usdt(self, balance):
        result = 0.
        for name in balance.keys():
            if name == 'usdt':
                result += balance[name]
            else:
                result += self.orders[name + 'usdt']['asks'][0][0] * balance[name]
        return result

    # TODO - прикрутить оплату в BNB
    def compute_commission(self, pair, amount):
        return amount * self.fee

    # TODO - реализовать
    def round(self, pair, amount):
        return amount

    def make_buy_order(self, pair, amount):
        if (not amount) or (not self.spend_till_end and amount > self.balance[pair[3:]]):
            return 0., 0.

        amount = min(amount, self.balance[pair[3:]])
        amount = self.round(pair, amount)
        eager_to_spend = amount
        bought = 0.

        for idx, (price, quantity) in enumerate(self.orders[pair]['asks']):
            if amount > price * quantity:
                amount -= price * quantity
                bought += quantity
            else:
                bought += amount / price
                bought -= self.compute_commission(pair, bought)
                return bought, -eager_to_spend

    def make_sell_order(self, pair, amount):
        if (not amount) or (not self.spend_till_end and amount > self.balance[pair[:3]]):
            return 0., 0.

        amount = min(amount, self.balance[pair[:3]])
        amount = self.round(pair, amount)
        eager_to_spend = amount
        bought = 0.

        for idx, (price, quantity) in enumerate(self.orders[pair]['bids']):
            if amount > quantity:
                amount -= quantity
                bought += price * quantity
            else:
                bought += price * amount
                bought -= self.compute_commission(pair, bought)
                return -eager_to_spend, bought

    def handle(self, query_dict, balance, orders):
        self.balance = balance.copy()
        self.orders = orders

        for query in query_dict.keys():
            delta_first = 0
            delta_second = 0
            if query_dict[query] > 0:
                delta_first, delta_second = self.make_buy_order(query, query_dict[query])
            elif query_dict[query] < 0:
                delta_first, delta_second = self.make_sell_order(query, -query_dict[query])
            self.balance[query[:3]] += delta_first
            self.balance[query[3:]] += delta_second

        delta_balance = {name: self.balance[name] - balance[name] for name in self.balance.keys()}
        return {'delta_balance': delta_balance, 'delta_usdt': self.count_in_usdt(delta_balance)}
