

# Мета-класс агента. В self.model инкапсулирована сама модель.
class Agent:
    def __init__(self, balance, model):
        self.balance = balance
        self.model = model

    def form_query(self, data):
        query, logs = self.model(data, self.balance)
        return query, logs, self.balance

    def get_response(self, response):
        delta_balance = response['delta_balance']
        previous_balance = self.balance.copy()
        for key in self.balance:
            self.balance[key] += delta_balance[key]

        return {'delta_balance': delta_balance, 'balance': self.balance,
                'previous_balance': previous_balance}
