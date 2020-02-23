import random


class RandomModel:
    def __init__(self):
        with open('../settings/pairs.txt') as file:
            self.pairs = file.readlines()

    def __call__(self, data, balance):
        query = {}
        for pair in self.pairs:
            decision = random.randint(0, 2)
            base = pair[:3]
            quote = pair[3:]
            amount = decision
            if decision == 1:
                amount = random.uniform(0, balance[base])
            if decision == 2:
                amount = -random.uniform(0, balance[quote])
            query[pair] = amount
        return query
