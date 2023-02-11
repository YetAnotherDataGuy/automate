import os
import sys
import logging.config
import logging
import traceback
from copy import deepcopy
from pathlib import Path
import inspect
from utils.datetime_utils import get_current_time
from utils.read_write_utils import read_and_load_as_dict


class CustomLogging:
    """
    This is a logger class for basic logging. Some key attributes or behaviour are:

    1. Default logging config is getting parsed from logger.yml.Optionally you can pass a different name
    through config_file argument during instantiation

    2. Default logging level is logging.DEBUG. You can alter it through argument level

    3. Log file naming uses the convention : <log file prefix>_<yyyy-mm-dd_hhmmss>.log".
    Here "log file prefix" is handled as follows
        a. Default is name of the module from which the logger is instantiated
        b. Optionally you can add log file prefix using log_file_prefix argument while
        instantiation. If so , this will be used as log file name prefix

    4. Optionally you can add a log file path using log_file_path argument. By default it will use the directory of
    the module from which the logger is instantiated. If you add log_file_path, that directory will be used for

    5. Adjust Formatters , Handlers or Loggers from logger.yml. Currently only two loggers are  there "root" and
    "standard" which can be accessed through instance method get_logger() . Calling get_logger without any argument returns
    the root logger while calling get_logger("standard") returns standard logger. Former logs only to console while
    latter can log to both console and file

    """
    GLOBAL_CONFIG = dict()

    def __init__(self, config_file='logger.yml',
                 level=logging.DEBUG,
                 log_file_prefix=None,
                 log_file_path=None):
        self.logger_config = deepcopy(self.GLOBAL_CONFIG)
        self.config_file = config_file
        self.level = level
        self.log_config_path = self._resolve_path()
        self.GLOBAL_CONFIG = self._parse_config_file(self.log_config_path, default_level=level)
        self.__called_from = inspect.stack()[-1].filename
        if self.GLOBAL_CONFIG:
            self._add_log_file(self.GLOBAL_CONFIG, log_file_prefix=log_file_prefix, log_file_path=log_file_path)

        # pprint(self.GLOBAL_CONFIG)

    def get_logger(self, logger_name='root'):

        if self.GLOBAL_CONFIG:
            self._remove_unused_handlers(logger_name=logger_name)
            self._remove_unused_loggers(logger_name=logger_name)
            logging.config.dictConfig(self.logger_config)
        return logging.getLogger(logger_name)

    def _add_log_file(self, config, log_file_prefix=None, log_file_path=None):
        curr_time = get_current_time(output_as_string=True).replace(" ", "_").replace(":", "")
        if log_file_prefix:
            log_file_prefix = Path(log_file_path).joinpath(log_file_prefix) if log_file_path \
                else log_file_prefix
        else:
            log_file_prefix = Path(log_file_path).joinpath(Path(self.__called_from).name.split('.')[0]) if log_file_path \
                else Path(self.__called_from).name.split('.')[0]
        config['handlers']['file_handler']['filename'] = f"{log_file_prefix}_{curr_time}.log"

    def _resolve_path(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config_file)
        if os.path.exists(path):
            return str(path)
        elif os.path.exists(self.config_file):
            return self.config_file
        else:
            raise FileNotFoundError(f"{self.config_file} does not exist. Please provide a valid full qualified"
                                    f"path for the file if the file is not in side  {os.path.abspath(__file__)}.")

    def _parse_config_file(self, path, default_level=logging.DEBUG):
        try:
            if not self.GLOBAL_CONFIG:
                return read_and_load_as_dict(path, 'yml')
            else:
                return self.GLOBAL_CONFIG

        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
            logging.info(tb.format_exception_only())
            logging.info('Error in loading Logging Configuration. Using default configs')
            logging.basicConfig(level=default_level)
            return

    def _remove_unused_handlers(self, logger_name='root'):
        try:
            logger_handlers = self.GLOBAL_CONFIG['loggers'][logger_name]['handlers']
        except KeyError:
            logger_handlers = self.GLOBAL_CONFIG[logger_name]['handlers']

        for handler in self.GLOBAL_CONFIG['handlers']:
            if handler not in logger_handlers:
                del self.logger_config['handlers'][handler]

    def _remove_unused_loggers(self, logger_name='root'):
        for logger in self.GLOBAL_CONFIG['loggers']:
            if logger != logger_name:
                del self.logger_config['loggers'][logger]


if __name__ == '__main__':

    # Sample driver code which instantiate and log messages using CustomLogging class.

    logging_obj = CustomLogging(log_file_path="A:\JustLearn\logs")
    logger = logging_obj.get_logger('standard')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error("error message")
    logger.critical('critical message')
