import json

from client import config
from client.api._api_process import response_process_flow
from client.api._api_process.response_processor import update_player_delta, check_key, just_log
from client.data_model.akaccount import PlayerAccount
from client.api.game_server import logger, http_client

logger = logger.getChild("mail")

SORT_LIST_URL = config.NetworkConfig.get_game_server_url("/social/getSortListInfo")

FRIEND_INFO_URL = config.NetworkConfig.get_game_server_url("/social/getFriendList")
FRIEND_INFO_DATA = {
    "idList": [
        ""
    ]
}


@response_process_flow(logger,
                       update_player_delta(),
                       check_key("friends"),
                       just_log("[{}] friend info get ok"))
def get_friend_info(account: PlayerAccount, *uids, uid_list=None):
    id_list = [] if uid_list == None else uid_list
    id_list.extend(list(uids))
    logger.info("[{}] get friend info for uid={}".format(account.uid, id_list))
    data = FRIEND_INFO_DATA.copy()
    data["idList"] = id_list
    ret_data = http_client.post_with_seqnum(account, FRIEND_INFO_URL,
                                            data=json.dumps(data))
    return ret_data


CURRENT_FRIEND_DATA = {
    "param": {},
    "sortKeyList": [
        "level",
        "infoShare"
    ],
    "type": 1
}


@response_process_flow(logger,
                       update_player_delta(),
                       check_key("result"),
                       just_log("[{}] get current friend list ok"))
def get_current_friend(account: PlayerAccount):
    logger.info("[{}] get current friend list".format(account.uid))
    data = CURRENT_FRIEND_DATA.copy()
    ret_data = http_client.post_with_seqnum(account, SORT_LIST_URL,
                                            data=json.dumps(data))
    return ret_data


SEARCH_ACCOUNT_DATA = {
    "param": {
        "nickName": "",
        "nickNumber": ""
    },
    "sortKeyList": [
        "level"
    ],
    "type": 0
}


@response_process_flow(logger,
                       update_player_delta(),
                       check_key("result"),
                       just_log("[{}] get current friend list ok"))
def search_account(account: PlayerAccount, nickname="", nicknumber=""):
    logger.info("[{}] search friend with {}#{}".format(account.uid, nickname, nicknumber))
    data = SEARCH_ACCOUNT_DATA.copy()
    data["param"] = {"nickName": nickname,
                     "nickNumber": nicknumber}
    ret_data = http_client.post_with_seqnum(account, SORT_LIST_URL,
                                            data=json.dumps(data))
    return ret_data


SEARCH_PLAYER_INFO_URL = config.NetworkConfig.get_game_server_url("/social/searchPlayer")
SEARCH_PLAYER_INFO_DATA = {
    "idList": [
    ]
}
@response_process_flow(logger,
                       update_player_delta(),
                       check_key("players"),
                       just_log("[{}] get search result list ok"))
def search_player_info_by_uid(account: PlayerAccount, *uids, uid_list=None):
    id_list = [] if uid_list == None else uid_list
    id_list.extend(list(uids))
    logger.info("[{}] get search result for uid={}".format(account.uid, id_list))
    data = SEARCH_PLAYER_INFO_DATA.copy()
    data["idList"] = id_list
    ret_data = http_client.post_with_seqnum(account, SEARCH_PLAYER_INFO_URL,
                                            data=json.dumps(data))
    return ret_data