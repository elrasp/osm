import logging
import os


def get_logger(filename, logger_name=__name__):
    """
    Create a logger
    :param logger_name: the name of the logger
    :param filename: the log file name
    :return: logger
    """
    log_filename = os.path.join("logs", filename)

    handler = logging.FileHandler(log_filename, mode='w')

    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    return logger
