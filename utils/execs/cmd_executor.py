import os
from utils.logger.logger import Logger

logger = Logger('log/executor')
logger.set_level(10)


class Executor(object):
    @staticmethod
    def exec_cmd(executable, *args):
        """
        execute executable with given arguments

        :param executable:
        :param args:
        :return: True if cmd is successful, false otherwise
        """
        cmd = executable

        for arg in args:
            cmd = cmd + ' ' + arg

        logger.debug("Executing Command: " + cmd)
        exit_status = os.system(cmd)
        logger.debug("Exit status = %d" % exit_status)
        return exit_status is 0
