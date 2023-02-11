from typing import Union, List
from functools import wraps
import time
from custom_exceptions import InvalidInputArgumentType
from env.logger import CustomLogging
from utils.datetime_utils import round_it


logging = CustomLogging()
logger = logging.get_logger()


def timer(func):
    """
    Wrapper function that returns the execution time of a function.
    Use it as a decorator @timer while defining any function for testing the
    performance
    :param func: The function argument if we are calling  this explicitly as timer(func)
    instead as a wrapper
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        logger.info(f"execution time of {func.__name__} is {round_it(t2 - t1)}")
        return result
    return wrapper


def beautify_str(inp_item: Union[str, List]) -> Union[str, List]:
    """
    Description:removes following characters from string or list of strings--> white spaces,\r,\n

    :param inp_item : string to be passed
    :type inp_item : str or list
    :rtype : str or list

    """
    if isinstance(inp_item, str):
        return inp_item.replace(" ", "").replace("\n", "").replace("\r", "")
    elif isinstance(inp_item, list):
        return [item.replace(" ", "").replace("\n", "").replace("\r", "") for item in inp_item]
    else:
        raise InvalidInputArgumentType({'inp_item': 'str'})
