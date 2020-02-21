from DataCatcher.DataCatcher import DataCatcher
import multiprocessing


class Environment:
    def __init__(self, agent, emulator, logger=None):
        self.agent = agent
        self.emulator = emulator
        self.logger = logger
        self.catcher = DataCatcher()

    def step(self, data):
        query = self.agent.form_query(data)
        emulator_response = self.emulator.handle(query)
        agent_response = self.agent.get_response(emulator_response)

        step_params = {'query': query, 'delta_balance': agent_response['delta_balance'],
                       'balance': agent_response['balance']}
        if self.logger:
            self.logger.update(step_params)
