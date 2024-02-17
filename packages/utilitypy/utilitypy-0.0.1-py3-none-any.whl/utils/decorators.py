import time as _time
from functools import  wraps as _wraps


def timer(func):
    '''The `timer` function is a decorator that measures the execution time of a given function and prints
    it out.

    Parameters
    ----------
    func
        The `func` parameter is a function that we want to time the execution of.

    Returns
    -------
        The function `wrapper` is being returned.

    '''
    @_wraps(func)
    def wrapper(*args, **kwargs):
        start = _time.perf_counter()
        results = func(*args, **kwargs)
        end = _time.perf_counter()
        print(f"[{func.__name__}] Execution time: {end - start:.6f}")
        return results
    return wrapper


def atimer(func):
    '''The `atimer` function is a decorator that measures the execution time of an asynchronous function
    and prints it out.

    Parameters
    ----------
    func
        The `func` parameter is a function that you want to decorate with the `atimer` decorator.

    Returns
    -------
        The function `wrapper` is being returned.

    '''
    @_wraps(func)
    async def wrapper(*args, **kwargs):
        start = _time.perf_counter()
        results = await func(*args, **kwargs)
        end = _time.perf_counter()
        print(f"[{func.__name__}] Execution time: {end - start:.6f}")
        return results
    return wrapper