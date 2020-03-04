import random


# Модель 1 - случайная
class ArianaModel:
    def __init__(self):
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]

    def __call__(self, data, balance):
        query = {}
        for pair in self.pairs:
            decision = random.randint(0, 3)
            base = pair[:3]
            quote = pair[3:]
            amount = decision
            if decision == 1:
                amount = ('bb', random.uniform(0, 0.01))
            elif decision == 2:
                amount = ('sb', random.uniform(0, balance[base]))
            elif decision == 3:
                amount = ('sq', random.uniform(0, balance[quote]))
            query[pair] = amount
        return query

# bb - buy base
# sb - sell base
# sq - sell quote
