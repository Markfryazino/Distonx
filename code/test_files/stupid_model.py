import random


# Модель 1 - случайная
class ArianaModel:
    def __init__(self):
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]

    def __call__(self, data, balance):
        query = {}
        for pair in self.pairs:
            decision = random.randint(0, 2)
            base = pair[:3]
            quote = pair[3:]
            amount = decision
            if decision == 0:
                amount = ('nothing', 0.)
            elif decision == 1:
                amount = ('sell quote', random.uniform(0, balance[quote]))
            elif decision == 2:
                amount = ('sell base', random.uniform(0, balance[base]))
            query[pair] = amount
        return query

# bb - buy base
# sb - sell base
# sq - sell quote
