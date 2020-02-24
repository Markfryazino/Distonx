class Emulator:
    # эта функция вызывается когда мы хотим купить amount монеток по текущей цене
    def make_buy_order(self, pair, amount):
        if not self.spend_till_end and amount > self.balance[1]:
            return [0, self.balance[1]]
        amount = min(amount, self.balance[1])
        capital = 0
        res_amount = amount
        for idx in range(len(self.orders['asks'])):
            can_afford = amount / self.orders['asks'][idx][0]  # сколько можем купить исходя из баланса
            spent_on_cur_iter = min(self.orders['asks'][idx][1], can_afford)
            capital += spent_on_cur_iter
            amount -= spent_on_cur_iter * self.orders['asks'][idx][0]
            if amount <= 1e-7:
                new_capital = math.floor(capital / self.min_order_size[pair][2]) * self.min_order_size[pair][2]
                delta = capital - new_capital
                amount += delta * self.orders['asks'][idx][0]
                capital = new_capital
                break
        return [capital * (1 - self.fee), -res_amount + amount]

    # если хотим продать amount монеток по рыночной цене - нам сюда
   def make_sell_order(self, pair, amount):
        if not self.spend_till_end and self.balance[0] < amount:
            return [self.balance[0], 0]
        capital = 0
        amount = min(amount, self.balance[0])
        res_amount = amount
        for idx in range(len(self.orders['bids'])):
            can_afford = min(amount, self.orders['bids'][idx][1])
            amount -= can_afford
            capital += can_afford * self.orders['bids'][idx][0]
            if amount <= 1e-7:
                new_capital = math.floor(capital / self.min_order_size[pair][2]) * self.min_order_size[pair][2]
                delta = capital - new_capital
                amount += delta / self.orders['bids'][idx][0]
                capital = new_capital
        return [-res_amount + amount, capital * (1 - self.fee)]

    # на вход поступает словарик {валютная пара: сколько хотим купить(если число отрицательное - продать)}
    # словарик с балансом {валюта: количество, которым мы располагаем}, словарик-стакан по всем нужным валютным
    # парам и флаг - что мы делаем, если у нас не хватает баланса для покупки желаемого количества валюты
    # по умолчанию мы покупаем столько, сколько позволяют наши средства
    def handle(self, query_dict, balance, orders, spend_till_end=True):
        self.spend_till_end = spend_till_end
        internal_balance = balance.copy()
        result = dict()
        for pair in query_dict:
            self.orders = orders[pair]
            self.balance = [internal_balance[pair[:3]], internal_balance[pair[3:]]]
            # print(self.balance)
            if query_dict[pair] < 0:
                result[pair] = self.make_buy_order(pair, -query_dict[pair])
            elif query_dict[pair] > 0:
                result[pair] = self.make_sell_order(pair, query_dict[pair])
            internal_balance[pair[:3]] += result[pair][0]
            internal_balance[pair[3:]] += result[pair][1]
        return {'delta_balance': result}  # возвращаем словарик с изменениями в количестве валюты А и В

    def __init__(self, ):
        self.balance = {}
        self.bnb_fee = 0.00075
        self.fee = 0.001
        self.orders = {}
        self.spend_till_end = True
        with open('../settings/min_order_size_and_step.txt', 'r') as f:
            self.min_order_size = eval(f.read())
