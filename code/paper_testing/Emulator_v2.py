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

    def count_in_usdt(self):
        result = 0.
        for name in self.balance.keys():
            if name == 'usdt':
                result += self.balance[name]
            else:
                base, quote = self.make_sell_base_order(name + 'usdt', self.balance[name], False)
                result += quote
        return result

    # TODO - прикрутить оплату в BNB
    def compute_commission(self, name, amount):
        return amount * self.fee

    # TODO - реализовать
    def round(self, pair, amount):
        return amount

    def make_sell_quote_order(self, pair, amount):
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
                bought -= self.compute_commission(pair[:3], bought)
                return bought, -eager_to_spend

    def make_buy_base_order(self, pair, amount):
        if not amount:
            return 0., 0.
        can_spend = self.balance[pair[3:]]
        spent = 0.
        bought = 0.
        for idx, (price, quantity) in enumerate(self.orders[pair]['asks']):
            if (amount > quantity) and (can_spend > price * quantity):
                spent += price * quantity
                can_spend -= price * quantity
                bought += quantity
                amount -= quantity
            elif (amount < quantity) and (can_spend >= amount * price):
                bought += amount
                spent += amount * price
                return bought - self.compute_commission(pair[:3], bought), -spent
            elif ((amount >= quantity) and (can_spend < quantity * price)) or \
                    ((amount < quantity) and (can_spend < amount * price)):
                if not self.spend_till_end:
                    return 0., 0.
                bought += can_spend / price
                spent += can_spend
                return bought - self.compute_commission(pair[:3], bought), -spent

    def make_sell_base_order(self, pair, amount, to_round=True):
        if (not amount) or (not self.spend_till_end and amount > self.balance[pair[:3]]):
            return 0., 0.

        amount = min(amount, self.balance[pair[:3]])
        if to_round:
            amount = self.round(pair, amount)
        eager_to_spend = amount
        bought = 0.

        for idx, (price, quantity) in enumerate(self.orders[pair]['bids']):
            if amount > quantity:
                amount -= quantity
                bought += price * quantity
            else:
                bought += price * amount
                bought -= self.compute_commission(pair[3:], bought)
                return -eager_to_spend, bought

    def handle(self, query_dict, balance, orders):
        self.balance = balance.copy()
        self.orders = orders
        old_usdt = self.count_in_usdt()

        for pair, (action, amount) in query_dict.items():
            delta_first = 0
            delta_second = 0
            if action == 'bb':
                delta_first, delta_second = self.make_buy_base_order(pair, amount)
            elif action == 'sb':
                delta_first, delta_second = self.make_sell_base_order(pair, amount)
            elif action == 'sq':
                delta_first, delta_second = self.make_sell_quote_order(pair, amount)
            self.balance[pair[:3]] += delta_first
            self.balance[pair[3:]] += delta_second

        delta_balance = {name: self.balance[name] - balance[name] for name in self.balance.keys()}
        new_usdt = self.count_in_usdt()

        return {'delta_balance': delta_balance, 'old_usdt': old_usdt, 'new_usdt': new_usdt,
                'delta_usdt': new_usdt - old_usdt}
