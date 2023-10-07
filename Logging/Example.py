import logging

from CustomLogging import Logger, timetz, addLoggingLevel
from datetime import datetime
import pytz
import functools

def add_logging_level(text, level_number, function_name):
    if text not in dir(logging):
        addLoggingLevel(text, level_number, function_name)

add_logging_level('LOG',55,'custom_logs')

current_date = datetime.now(pytz.timezone('Asia/Singapore')).strftime('%Y%m%d')
logfilename = f"logfiles/{current_date}.log"
logfilename2 = f"logfiles/{current_date}.log2"
rootlogger  = Logger('Example',stream='',file=[logfilename,logfilename2])


def log_fuction(func):
    def wrapper(*args, **kwargs):
        rootlogger.logger.info(f'Calling function : {func.__name__}')
        try:
            result = func(*args, **kwargs)
            rootlogger.logger.custom_logs(f'Function {func.__name__} completed successfully')
            print(f'Function {func.__name__} completed successfully')
            return result
        except Exception as e:
            rootlogger.logger.error(f'Function {func.__name__} failed with error : {str(e)}')
            print(f'Function {func.__name__} failed with error : {str(e)}')
            # raise

    return wrapper

@log_fuction
def division(numerator, denominator):
    return numerator/denominator

print(division(3,2))
print(division(3,0))

print(rootlogger.stream.getvalue())