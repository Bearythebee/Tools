import logging, pytz, sys, re, io
from datetime import datetime

def timetz(*args):
    tz = pytz.timezone('Asia/Singapore')
    return datetime.now(tz).timetuple()

def addLoggingLevel(levelName, levelNum, methodName=None):
    """

    Source : https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility

    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    #>>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    #>>> logging.getLogger(__name__).setLevel("TRACE")
    #>>> logging.getLogger(__name__).trace('that worked')
    #>>> logging.trace('so did this')
    #>>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

class Logger():

    def __init__(self):

        self.stream = io.StringIO()

        # Add custom logging with levels (Higher number take precedence)
        #Logging levels for reference
        # NOTSET = 0
        # DEBUG = 10
        # INFO = 20
        # WARN = 30
        # ERROR = 40
        # CRITICAL = 50

        if 'LOG' not in dir(logging):
            addLoggingLevel('LOG', 55, 'custom_logs')

        rootlogger = logging.getLogger()
        rootlogger.setLevel(logging.ERROR)
        rootlogger.propagate = False

        ch = logging.StreamHandler(self.stream)
        logging.Formatter.converter = timetz
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',"%Y-%m-%d %H:%M:%S")
        ch.setFormatter(formatter)

        rootlogger.addHandler(ch)

        self.log = rootlogger
        self.handler = ch

    def custom_logs(self, text):
        self.custom_logs(text)
        self.handler.flush()

    def log_error(self, text):
        self.log.error(text)
        self.handler.flush