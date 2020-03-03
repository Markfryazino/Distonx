import logging


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
