import logging
import time
import pathlib
import os


def log_function_name(func):
    '''
    Print in the terminal the decorated function


    Parameters
    ----------
    func : function
        Function address that will be logged


    Returns
    -------
    inner_func : function
        Decorated function
    '''
    def inner_func(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return inner_func


def config_logger(path):
    '''
    Save in log file about decorated function


    Parameters
    ----------
    path : str
        Path of log file


    Returns
    -------
        None
    '''
    dir_log = os.path.join(path, "logs")
    pathlib.Path(dir_log).mkdir(parents=True, exist_ok=True) 
    path_log = os.path.join(dir_log, "project.log")
    logging.basicConfig(
        filename=path_log,
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True
    )
    
