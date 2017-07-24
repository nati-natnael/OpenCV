import logging
import time

# CRITICAL - 50
# ERROR - 40
# WARNING - 30
# INFO - 20
# DEBUG - 10


class Logger(object):

    def __init__(self, log_name):
        self.file_logger = logging.getLogger(log_name)

        t = time.strftime("%H_%M_%S")
        d = time.strftime("%d_%m_%Y")
        file_name = log_name + "_" + d + "_" + t + ".log"

        formatter = logging.Formatter("%(asctime)s: [%(levelname)s] %(message)s")

        self.file_log_handler = logging.FileHandler(file_name, mode='w+')
        self.stream_handler = logging.StreamHandler()

        # Default settings
        self.file_log_handler.setFormatter(formatter)
        self.stream_handler.setFormatter(formatter)

        self.file_logger.setLevel(logging.DEBUG)

        self.file_logger.addHandler(self.file_log_handler)
        self.file_logger.addHandler(self.stream_handler)

    def set_formatter(self, formatter):
        """

        :param formatter:
        :return:
        """
        self.file_log_handler.setFormatter(formatter)
        self.stream_handler.setFormatter(formatter)

        self.file_logger.addHandler(self.file_log_handler)
        self.file_logger.addHandler(self.stream_handler)

    def set_level(self, level):
        """

        :param level:
        :return:
        """
        self.file_logger.setLevel(level=level)

    def critical(self, message):
        """

        :param message:
        :return:
        """
        self.file_logger.critical(message)

    def error(self, message):
        """

        :param message:
        :return:
        """
        self.file_logger.error(message)

    def warning(self, message):
        """

        :param message:
        :return:
        """
        self.file_logger.warning(message)

    def info(self, message):
        """

        :param message:
        :return:
        """
        self.file_logger.info(message)

    def debug(self, message):
        """

        :param message:
        :return:
        """
        self.file_logger.debug(message)