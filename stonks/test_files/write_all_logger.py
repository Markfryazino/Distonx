import logging
import joblib
import time


# Все пишем в Ariana_output
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


# Пишем не все, а только когда есть запрос
class SparseLogger:
    def __init__(self):
        open("trash/output.joblib", "w").close()
        self.data = []

    def step(self, step_params):
        if (step_params['query']) and (step_params['emulator_response']['delta_usdt']):
            logging.debug(str(time.time()) + ' | ' + str(step_params['emulator_response']['new_usdt']))
        self.data.append((time.time(), step_params['query'],
                          step_params['emulator_response']['delta_balance'],
                          step_params['agent_response']['balance'],
                          step_params['emulator_response']['new_usdt'],
                          step_params['emulator_response']['delta_usdt'],
                          step_params['model_logs']))

    def save(self):
        joblib.dump(self.data, 'trash/output.joblib')
