import functools
import logging
import sys


def logger_name(filename, lineno):
    return filename[:-3].split('/QTodoTxt/')[1].replace('/', '.') + ':' + str(lineno)


def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being logged
    when the function is used.'''

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        func_def_line = func.__code__.co_firstlineno
        func_def_filename = func.__code__.co_filename
        prev_frame = sys._getframe().f_back
        calling_lineno = prev_frame.f_lineno
        calling_filename = prev_frame.f_code.co_filename
        logger = logging.getLogger(logger_name(calling_filename, calling_lineno))
        logger.warning("Call to deprecated function {} ({}@{}).".format
                       (func.__name__, func_def_line, func_def_filename))
        return func(*args, **kwargs)
    return new_func
