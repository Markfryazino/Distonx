from code.auxiliary import split_to_pairs


class BonnieModel:
    def __init__(self):
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]

    def __call__(self, data, balance):
        dct_data = split_to_pairs(data)