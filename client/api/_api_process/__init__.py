import functools

from client import utils

def response_process_flow(logger, *data_processor):
    def a(api_func):
        @utils.log_wrapper(api_func)
        @functools.wraps(api_func)
        def b(*args, **kwargs):
            ret_data = api_func(*args, **kwargs)
            for d_p in data_processor:
                if d_p(api_func)(args[0], ret_data, logger):
                    continue
                else:
                    return ret_data
            return ret_data
        return b
    return a


def data_processor_wrapper(d_p):
    @functools.wraps(d_p)
    def take_p_arg(*args, **kwargs):
        def take_api_func(api_func):
            def take_ess_arg(account, ret_data, logger):
                return utils.log_wrapper(api_func)(d_p)(account, ret_data, logger, *args, *kwargs)
            return take_ess_arg
        return take_api_func
    return take_p_arg
