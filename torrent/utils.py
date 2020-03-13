import logging
import os


def get_logger(name):
    os.makedirs('logs', exist_ok=True)
    handler = logging.FileHandler('logs/' + name + '.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    logger = logging.Logger(name)
    logger.addHandler(handler)
    return logger
