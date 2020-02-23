

class Agent:
    def __init__(self, balance, preprocessor, model):
        self.balance = balance
        self.preprocessor = preprocessor
        self.model = model

    def form_query(self, data):
        processed_data = self.preprocessor(data)
        query = self.model(processed_data)
        return query

    def get_response(self, response):
        delta_balance = response['delta_balance']
        for key in self.balance:
            self.balance[key] += delta_balance[key]

        return {'delta_balance': delta_balance, 'balance': self.balance}
