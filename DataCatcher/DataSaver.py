import time
import logging


# Простой saver для тестирования, который просто все сохраняет в txt файл
class TxtDataSaver:
    def __init__(self):
        self.data = []

    def get_data(self, manager_dict):
        self.data.append({})
        self.data[-1]['time'] = time.time()
        for key in manager_dict:
            self.data[-1][key] = manager_dict[key]

    def save_data(self, file_name):
        logging.debug('saving data to ' + file_name)
        with open(file_name, 'w') as file:
            file.write(str(self.data))
