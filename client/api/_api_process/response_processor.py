from client.api._api_process import data_processor_wrapper


@data_processor_wrapper
def check_key(account, ret_data, logger, *args, **kwargs):
    keys, kvs = args, kwargs
    if ret_data is None:
        logger.error("[{}] fail in http connection".format(account.uid, ret_data))
        return False
    else:
        for key in keys:
            if key not in ret_data.keys():
                logger.warning("[{}] response didn't contain key={}".format(account.uid, key))
                return False
        for key, val in kvs.items():
            if key not in ret_data.keys():
                logger.warning("[{}] response didn't contain key={}".format(account.uid, key))
                return False
            if val != ret_data[key]:
                logger.warning("[{}] response {}={} didn't match {}={}".format(account.uid,
                                                                               key, ret_data[key],
                                                                               key, val))
                return False
        return True


@data_processor_wrapper
def update_player_delta(account, ret_data, logger, *args, **kwargs):
    if ret_data is None:
        logger.error("[{}] fail in http connection".format(account.uid))
        return False
    if ret_data.get("playerDataDelta") is None:
        logger.warning("[{}] update player delta failed, reason:{}".format(account.uid,
                                                                           ret_data))
        return False
    else:
        account.update_data(ret_data["playerDataDelta"]["modified"])
        logger.info("[{}] update player delta data success".format(account.uid))
        return True


@data_processor_wrapper
def just_log(account, ret_data, logger, *args, **kwargs):
    for log_text in args:
        logger.info(log_text.format(account.uid))
    return True
