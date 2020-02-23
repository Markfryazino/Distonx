import logging


class WriteAllLogger:
    def __init__(self):
        pass

    def step(self, step_params):
        logging.debug(str(step_params))
