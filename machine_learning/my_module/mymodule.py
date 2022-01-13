""" this respository includes modules designed by myself

get_exec_time(fn): print execute time
"""
import time
from functools import wraps
# a decorator to count time
def get_exec_time(fn):
    """ a decorator to get execute time of fn """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        end = time.time()
        print("consuming time: {:.2f}s".format(end - start))
        # return fn(*args, **kwargs)  if add this, it will execute two times
    return wrapper