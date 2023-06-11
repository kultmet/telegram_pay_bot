import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    # logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
info_logger = setup_logger('info_logger', 'logs/info_logfile.log')
# logger.info('This is just info message')

# second file logger
warning_logger = setup_logger('errors_logger', 'logs/errors_logfile.log')
# super_logger.error('This is an error message')