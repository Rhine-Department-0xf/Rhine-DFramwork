import json

from client import encryption
from client.data_model.akaccount import PlayerAccount
from client.api import http_client, logger
from client.config import LoginPara, PlatformKey

logger = logger.getChild("auth_server")

U8_LOGIN_URL = "https://as.hypergryph.com/user/login"
U8_LOGIN_DATA = {
    "account": "",
    "captcha": "",
    "deviceId": "",
    "password": "",
    "platform": 1,
    "sign": ""
}


def login(account: PlayerAccount):
    logger.info("login by username={} and password={}".format(account.username, account.password))
    data = U8_LOGIN_DATA.copy()
    data["account"] = account.username
    data["deviceId"] = account.device_id
    data["password"] = account.password
    data["platform"] = PlatformKey.ANDROID.value
    data["sign"] = encryption.get_u8_login_sign(account.username,
                                                account.password,
                                                account.device_id,
                                                PlatformKey.ANDROID.value)
    ret_data = http_client.post(account, U8_LOGIN_URL, data=json.dumps(data))
    if ret_data is None:
        logger.error("http get/post fail")
        return
    if ret_data["result"] != 0:
        logger.warning("fail,reason: {}".format(json.dumps(ret_data)))
        return
    account.channel_uid = ret_data["uid"]
    account.access_token = ret_data["token"]
    logger.info("login success with channel_uid={},access_token={}".format(ret_data["uid"], ret_data["token"]))
    return ret_data


U8_AUTH_URL = "https://as.hypergryph.com/user/auth"
U8_AUTH_DATA = {
    "token": "",
    "sign": ""
}


def auth(account: PlayerAccount):
    logger.info("login by access_token={}".format(account.access_token))
    data = U8_AUTH_DATA.copy()
    data["token"] = account.access_token
    data["sign"] = encryption.get_u8_auth_sign(account.access_token)
    ret_data = http_client.post(account, U8_AUTH_URL, data=json.dumps(data))
    if ret_data is None:
        logger.error("http get/post fail")
        return
    if ret_data.get("uid") is None:
        logger.warning("fail,reason: {}".format(json.dumps(ret_data)))
        return
    account.channel_uid = ret_data["uid"]
    logger.info("auth success with channel_uid={}".format(ret_data["uid"]))
    return ret_data


U8_PING_URL = "https://as.hypergryph.com/online/v1/ping"
U8_PING_DATA = {
    "sign": "1d8115e3ab844f2beb8d88c94068dd94f695b56a",
    "token": "83LeEClhQj9myccG8mn2F4OcQj8GQgU0"
}


def ping(account: PlayerAccount):
    logger.info("ping auth server")
    data = U8_PING_DATA.copy()
    data["token"] = account.access_token
    data["sign"] = encryption.get_u8_auth_sign(account.access_token)
    ret_data = http_client.post(account, U8_PING_URL, data=json.dumps(data))
    if ret_data is None:
        logger.error("http get/post fail")
        return
    if ret_data["result"] != 0:
        logger.warning("fail,reason: {}".format(json.dumps(ret_data)))
        return
    logger.info("success")
    return ret_data


U8_GETTOKEN_URL = "https://as.hypergryph.com/u8/user/v1/getToken"
U8_GETTOKEN_DATA = {
    "appId": "1",
    "channelId": "1",
    "deviceId": "",
    "deviceId2": "",
    "deviceId3": "",
    "extension": "{\"uid\":\"\",\"access_token\":\"\"}",
    "platform": 1,
    "sign": "",
    "subChannel": "1",
    "worldId": "1"
}


def get_token(account: PlayerAccount):
    logger.info("get token")
    data = U8_GETTOKEN_DATA.copy()
    data["appId"] = LoginPara.APP_ID.value
    data["channelId"] = LoginPara.CHANNEL_ID.value
    data["deviceId"] = account.device_id
    data["deviceId2"] = account.device_id2
    data["extension"] = json.dumps({"uid": account.channel_uid,
                                    "access_token": account.access_token}).replace(" ", "")
    data["platform"] = PlatformKey.ANDROID.value
    data["subChannel"] = LoginPara.SUB_CHANNEL.value
    data["worldId"] = LoginPara.WORLD_ID.value
    data["sign"] = encryption.get_u8_gettoken_sign(LoginPara.APP_ID.value,
                                                   LoginPara.CHANNEL_ID.value,
                                                   account.device_id,
                                                   account.device_id2,
                                                   account.device_id3,
                                                   {"uid": account.channel_uid,
                                                    "access_token": account.access_token},
                                                   PlatformKey.ANDROID.value,
                                                   LoginPara.SUB_CHANNEL.value,
                                                   LoginPara.WORLD_ID.value
                                                   )
    ret_data = http_client.post(account, U8_GETTOKEN_URL, data=json.dumps(data))
    if ret_data is None:
        logger.error("http get/post fail")
        return
    if ret_data["result"] != 0:
        logger.warning("fail,reason: {}".format(json.dumps(ret_data)))
        return
    account.uid = ret_data["uid"]
    account.token = ret_data["token"]
    account.channel_uid = ret_data["channelUid"]
    logger.info("get token success with uid={},token={}".format(ret_data["uid"], ret_data["token"]))
    return ret_data
