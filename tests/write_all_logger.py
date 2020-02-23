import logging


class WriteAllLogger:
    @staticmethod
    def step(step_params):
        logging.debug(str(step_params))
