import datetime
import functools
import logging
import random
import string
from client import encryption


# 生成随机device_id
def get_random_device_id():
    return encryption.get_md5(''.join(random.choices(string.ascii_letters + string.digits, k = 12)))

# 生成随机device_id2
def get_random_device_id2():
    return '91' + ''.join(random.choices(string.digits, k = 13))

def deep_update(origin:dict,modified:dict):
    for key in modified.keys():
        if key in origin.keys():
            if isinstance(modified[key], dict):
                deep_update(origin[key], modified[key])
            else:
                origin[key] = modified[key]
        else:
            origin[key] = modified[key]
    return origin

def log_wrapper(func_overrider):
    old_factory = logging.getLogRecordFactory()

    def new_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.funcName = func_overrider.__name__
        return record

    def decorator(func):
        def wrapper(*args, **kwargs):
            logging.setLogRecordFactory(new_factory)
            result = func(*args, **kwargs)
            logging.setLogRecordFactory(old_factory)
            return result
        return wrapper
    return decorator