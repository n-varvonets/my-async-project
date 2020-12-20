import datetime
import logging
import os


def init_logger(logger_name, file_name):
    """ ~~~~ Set Logger ~~~~ """
    if not os.path.exists('logs'):
        os.mkdir('logs')

    time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M')
    log_file = f'logs/{file_name}_{time}.log'
    formatter = logging.Formatter('[%(asctime)s] - [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s')

    log_handler = logging.FileHandler(log_file)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)

    log = logging.getLogger(logger_name)
    log.setLevel(logging.INFO)
    log.addHandler(log_handler)
    return log
