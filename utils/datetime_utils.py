import datetime
import time
import pytz
from typing import Union
from pytz import UnknownTimeZoneError
# import traceback
import sys
from pprint import pprint


def get_current_time(tz: str = 'UTC',
                     output_as_string: bool = False,
                     convert_to_unixtime: bool = False,
                     retain_tz_info: bool = False) -> Union[datetime.datetime, float, str]:
    """
    returns current time for specific timezone mentioned either as datetime or unix time float value or as string
    """
    try:
        now = datetime.datetime.now(pytz.timezone(tz))
        if not retain_tz_info:
            now = now.replace(tzinfo=None)

        if convert_to_unixtime:
            now = time.mktime(now.timetuple())

        if output_as_string:
            now = str(now)

        return now

    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_type == UnknownTimeZoneError:
            #             tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
            print("Time zone(tz) value provided is invalid. It should be one of the below values:")
            pprint(pytz.all_timezones)
            raise
        else:
            raise


def round_it(seconds: float):
    """
    round seconds to nearest possible scale (ranging from hours to micro seconds) and return a meaningful formatted string .
    For example :
    round_it(15000) --> Returns '4.1667 hrs'
    round_it(1500) --> Returns '25.0 mins'
    round_it(15) --> Returns '15 secs'
    round_it(0.15) --> Returns '150.0 ms'
    round_it(0.00015) --> Return '150.0 μs'

    :param seconds: number of seconds in float value
    :return: float value rounded up or down to appropriate scale with up to 4 decimal points
    """
    if (seconds / 60) / 60 >= 1:
        return f"{round((seconds / 60) / 60, 4)} hrs"
    elif (seconds / 60) >= 1:
        return f"{round(seconds / 60, 4)} mins"
    elif seconds >= 1:
        return f"{round(seconds, 4)} secs"
    elif seconds * 1000 >= 1:
        return f"{round(seconds * 1000, 4)} ms"
    elif seconds * 1000000 >= 1:
        return f"{round(seconds * 1000000, 4)} μs"
    else:
        return "0 secs"
