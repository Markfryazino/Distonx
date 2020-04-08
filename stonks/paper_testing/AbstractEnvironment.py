from ..DataCatcher import DB


class AbstractEnvironment:
    def __init__(self, agent, emulator, logger=None, indent=3600, period=1.):
        self.db = DB()
        self.agent = agent
        self.emulator = emulator
        self.logger = logger
        self.indent = indent
        self.period = period
        self.current_data = {}
        self.memory = {}
        with open('settings/pairs.txt') as file:
            self.pairs = [a[:-1] for a in file.readlines()]

    def form_orderbook(self):
        orderbook = {pair: {'bids': [], 'asks': []} for pair in self.pairs}
        for pair in self.pairs:
            for i in range(20):
                for side in ('bid', 'ask'):
                    price = float(self.current_data[pair][f'depth_{side}_price_{i + 1}'])
                    quantity = float(self.current_data[pair][f'depth_{side}_quantity_{i + 1}'])
                    orderbook[pair][side + 's'].append([price, quantity])
        return orderbook

    def step(self, data):
        query, logs, balance = self.agent.form_query(data)
        emulator_response = self.emulator.handle(query, balance, self.form_orderbook())
        agent_response = self.agent.get_response(emulator_response)

        step_params = {'query': query, 'model_logs': logs, 'emulator_response': emulator_response,
                       'agent_response': agent_response}

        if self.logger is not None:
            self.logger.step(step_params)
