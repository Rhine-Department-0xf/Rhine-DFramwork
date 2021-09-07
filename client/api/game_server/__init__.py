import json

from client.data_model.akaccount import PlayerAccount
from client.api import http_client, logger
from client import config
from client.api._api_process import response_process_flow
from client.api._api_process.response_processor import update_player_delta, just_log

logger = logger.getChild("game_server")

LOGIN_URL = config.NetworkConfig.get_game_server_url("/account/login")
LOGIN_DATA = {
    "assetsVersion": "21-04-20-13-10-55-17ee8d",
    "clientVersion": "1.5.01",
    "deviceId": "a96df156d79640461a0d49511f490129",
    "deviceId2": "910000000146166",
    "deviceId3": "",
    "networkVersion": "5",
    "platform": 1,
    "token": "z4y9wQpNz4zdQ4cp6anMJabf",
    "uid": "89316304"
}


def login(account: PlayerAccount):
    logger.info("[{}] login to game server".format(account.uid))
    data = LOGIN_DATA.copy()
    data["assetsVersion"] = config.ProductionConfig.assetsVersion
    data["clientVersion"] = config.ProductionConfig.clientVersion
    data["deviceId"] = account.device_id
    data["deviceId2"] = account.device_id2
    data["networkVersion"] = config.NetworkConfig.version
    data["platform"] = config.PlatformKey.ANDROID.value
    data["token"] = account.token
    data["uid"] = account.uid

    ret_data = http_client.post_with_seqnum(account, LOGIN_URL,
                                            data=json.dumps(data))
    if ret_data is None:
        logger.error("http get/post fail")
        return
    if ret_data["result"] != 0:
        logger.warning("fail,reason: {}".format(json.dumps(ret_data)))
        return
    account.secret = ret_data["secret"]
    account.uid = ret_data["uid"]
    logger.info("[{}] success with secret={}".format(account.uid, ret_data["secret"]))
    return ret_data


SYNC_DATA_URL = config.NetworkConfig.get_game_server_url("/account/syncData")
SYNC_DATA_DATA = {
    "platform": 1
}

def sync_data(account: PlayerAccount):
    logger.info("[{}] sync data with game server".format(account.uid))
    data = SYNC_DATA_DATA.copy()
    data["platform"] = config.PlatformKey.ANDROID.value

    ret_data = http_client.post_with_seqnum(account, SYNC_DATA_URL,
                                            data=json.dumps(data))
    if ret_data is None:
        logger.error("http get/post fail")
        return
    if ret_data["result"] != 0:
        logger.warning("fail,reason: {}".format(json.dumps(ret_data)))
        return
    account.login_time = ret_data['user']['pushFlags']['status']
    logger.info("[{}] get login_time={}".format(account.uid, account.login_time))
    account.data = ret_data['user']
    logger.info("[{}] updating data from sync data".format(account.uid))
    return ret_data


GET_UNCONFIRMED_ORDER_URL = config.NetworkConfig.get_game_server_url("/pay/getUnconfirmedOrderIdList")
GET_UNCONFIRMED_ORDER_DATA = {}

@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] retrieved all order"))
def get_unconfirmed_order(account: PlayerAccount):
    logger.info("[{}] get unconfirmed order".format(account.uid))
    ret_data = http_client.post_with_seqnum(account, GET_UNCONFIRMED_ORDER_URL,
                                            data=json.dumps(GET_UNCONFIRMED_ORDER_DATA))
    return ret_data


SYNC_STATUS_URL = config.NetworkConfig.get_game_server_url("/account/syncStatus")
SYNC_STATUS_DATA = {
    "modules": 1631,
    "params": {
        "16": {
            "goodIdMap": {
                "CASH": [
                    "icu_2021"
                ],
                "ES": [],
                "GP": [
                    "GP_Once_1"
                ],
                "HS": [],
                "LS": [],
                "SOCIAL": []
            }
        }
    }
}

@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] sync status ok"))
def sync_status(account: PlayerAccount):
    logger.info("[{}] sync status".format(account.uid))
    ret_data = http_client.post_with_seqnum(account, SYNC_STATUS_URL,
                                            data=json.dumps(SYNC_STATUS_DATA))
    return ret_data


from client.api.game_server.checkin import checkin
from client.api.game_server import mail
from client.api.game_server import mission
from client.api.game_server import battle
from client.api.game_server import building
from client.api.game_server import social