import logging
import joblib
import time


class WriteAllLogger:
    def __init__(self):
        pass

    def step(self, step_params):
        with open('trash/Ariana_output.txt', 'a') as file:
            file.write('Query: ' + str(step_params['query']) + '\n')
            file.write('delta_balance: ' + str(step_params['emulator_response']['delta_balance']) + '\n')
            file.write('new balance: ' + str(step_params['agent_response']['balance']) + '\n')
            file.write('usdt balance: ' + str(step_params['emulator_response']['new_usdt']) + '\n')
            file.write('delta usdt: ' + str(step_params['emulator_response']['delta_usdt']) + '\n\n')


class SparseLogger:
    def __init__(self):
        open("trash/output.pickle", "w").close()
        self.data = []

    def step(self, step_params):
        if step_params['query'] != {}:
            logging.debug(str(time.time()))
            self.data.append((time.time(), step_params['query'],
                              step_params['emulator_response']['delta_balance'],
                              step_params['agent_response']['balance'],
                              step_params['emulator_response']['new_usdt'],
                              step_params['emulator_response']['delta_usdt']))

    def save(self):
        joblib.dump(self.data, 'trash/output.joblib')
