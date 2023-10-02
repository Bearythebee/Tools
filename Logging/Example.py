import logging

from CustomLogging import Logger
from datetime import datetime
import pytz
import functools

current_date = datetime.now(pytz.timezone('Asia/Singapore')).strftime('%Y%m%d')
logfilename = f"{current_date}.log"
rootlogger  = Logger()

logger = logging.getLogger()

def log_fuction(func):
    def wrapper(*args, **kwargs):
        logger.info(f'Calling function : {func.__name__}')
        try:
            result = func(*args, **kwargs)
            logger.custom_logs(f'Function {func.__name__} completed successfully')
            print(f'Function {func.__name__} completed successfully')
            return result
        except Exception as e:
            logger.error(f'Function {func.__name__} failed with error : {str(e)}')
            print(f'Function {func.__name__} failed with error : {str(e)}')
            # raise

    return wrapper

@log_fuction
def division(numerator, denominator):
    return numerator/denominator

print(division(3,2))
print(division(3,0))

print(rootlogger.stream.getvalue())