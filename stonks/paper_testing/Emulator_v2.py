

# Класс эмулятора биржи, который обрабатывает запросы модели.
class EmulatorV2:
    def __init__(self, fee=0.001, spend_till_end=True, pay_in_bnb=True):
        self.spend_till_end = spend_till_end
        self.bnb_fee = 0.00075
        self.fee = fee
        self.pay_in_bnb = pay_in_bnb
        self.balance = {}
        self.orders = {}

        with open('settings/cryptos.txt') as file:
            self.cryptos = file.readlines()
        self.cryptos = [el[:-1] for el in self.cryptos]

        with open('settings/min_order_size_and_step.txt', 'r') as f:
            self.min_order_size = eval(f.read())

    # Подсчет стоимости текущего кошелька в долларах
    def count_in_usdt(self):
        result = 0.
        for name in self.balance.keys():
            if name == 'usdt':
                result += self.balance[name]
            else:
                base, quote = self.make_sell_base_order(name + 'usdt', self.balance[name], False, False)
                result += quote
        return result

    # TODO - прикрутить оплату в BNB
    def compute_commission(self, name, amount):
        return self.fee * amount

    # Округление (не можем выставлять ордера с произвольными ценами)
    def round(self, pair, amount):
        min_val = self.min_order_size[pair][0]
        new_val = (amount // min_val) * min_val
        return new_val

    # Проверка, достаточно ли большой ордер (иначе биржа может не принять)
    def check_if_enough(self, pair, amount):
        min_val = self.min_order_size[pair][1]
        return amount >= min_val

    # Оценка того, сколько мы можем купить base на фиксированное количество quote
    def quote_to_base(self, pair, amount):
        if not amount:
            return 0.

        bought = 0.
        for idx, (price, quantity) in enumerate(self.orders[pair]['asks']):
            if amount > price * quantity:
                amount -= price * quantity
                bought += quantity
            else:
                bought += amount / price
                return bought

    # Покупка коинов
    def make_buy_base_order(self, pair, amount, ignore_bnb=True):
        if not amount:
            return 0., 0.
        amount = self.round(pair, amount)
        can_spend = self.balance[pair[3:]]
        spent = 0.
        bought = 0.
        for idx, (price, quantity) in enumerate(self.orders[pair]['asks']):
            if (amount > quantity) and (can_spend > price * quantity +
                                        self.compute_commission(pair[3:], price * quantity)):
                spent += price * quantity + self.compute_commission(pair[3:], price * quantity)
                can_spend -= price * quantity + self.compute_commission(pair[3:], price * quantity)
                bought += quantity
                amount -= quantity
            elif (amount < quantity) and \
                    (can_spend >= amount * price + self.compute_commission(pair[3:], amount * price)):
                bought += amount
                spent += amount * price + self.compute_commission(pair[3:], amount * price)
                return bought, -spent
            elif ((amount >= quantity) and
                  (can_spend < quantity * price + self.compute_commission(pair[3:], quantity * price))) \
                    or ((amount < quantity) and (can_spend < amount * price +
                                                 self.compute_commission(pair[3:], amount * price))):
                if not self.spend_till_end:
                    return 0., 0.

                if ignore_bnb:
                    bought += can_spend / (price * (1 + self.fee))
                    spent += can_spend
                else:
                    to_buy = can_spend / price
                    for i in range(10):
                        com = self.compute_commission(pair[3:], to_buy * price)
                        to_buy = (can_spend - com) / price
                    spent += to_buy * price + self.compute_commission(pair[3:], to_buy * price)
                    bought += to_buy

                return bought, -spent

    # Продажа коинов
    def make_sell_base_order(self, pair, amount, to_round=True, use_comm=True):
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
                bought += price * quantity - use_comm * self.compute_commission(pair[3:], price * quantity)
            else:
                bought += price * amount - use_comm * self.compute_commission(pair[3:], price * amount)
                return -eager_to_spend, bought

    # Основная функция, обрабатывающая запросы модели
    def handle(self, query, balance, orders):
        self.balance = balance.copy()
        self.orders = orders
        old_usdt = self.count_in_usdt()

        for (action, amount) in query.items():
            delta_first = 0
            delta_second = 0
            if action == 'buy base':
                delta_first, delta_second = self.make_buy_base_order(pair, amount)
            elif action == 'sell base':
                delta_first, delta_second = self.make_sell_base_order(pair, amount)
            elif action == 'sell quote':
                base_to_buy = self.quote_to_base(pair, amount)
                delta_first, delta_second = self.make_buy_base_order(pair, base_to_buy)

            if not self.check_if_enough(pair, abs(delta_second)):
                delta_first, delta_second = 0, 0

            self.balance[pair[:3]] += delta_first
            self.balance[pair[3:]] += delta_second

        delta_balance = {name: self.balance[name] - balance[name] for name in self.balance.keys()}
        new_usdt = self.count_in_usdt()

        return {'delta_balance': delta_balance, 'old_usdt': old_usdt, 'new_usdt': new_usdt,
                'delta_usdt': new_usdt - old_usdt}
