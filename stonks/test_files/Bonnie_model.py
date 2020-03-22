from ..auxiliary import split_to_pairs


class BonnieModel:
    def __init__(self):
        self.window = 10
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]
        self.balance = {pair: [] for pair in self.pairs}

    def __call__(self, data, balance):
        dct_data = split_to_pairs(data)
        for pair in self.pairs:
            self.balance[pair].append((dct_data[pair]['depth_ask_price_1'] +
                                       dct_data[pair]['depth_bid_price_1']) / 2.)
        if len(self.balance['btcusdt']) < self.window + 1:
            return {}

        for pair in self.pairs:
            diff = [self.balance[pair][i] - self.balance[pair][i - 1] for i in range(1, self.window)]
            self.balance[pair].pop(0)
            indicator = sum(diff)
