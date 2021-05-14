import json
import time

from client import config
from client.data_model.akaccount import PlayerAccount
from client.api._api_process import response_process_flow
from client.api._api_process.response_processor import check_key, update_player_delta, just_log
from client.api.game_server import logger, http_client

logger = logger.getChild("mail")

META_INFO_URL = config.NetworkConfig.get_game_server_url("/mail/getMetaInfoList")
META_INFO_DATA = {
    "from": 1619248335
}


@response_process_flow(logger,
                       update_player_delta(),
                       check_key("result"),
                       just_log("[{}] mail meta info get ok"))
def get_meta_info_list(account: PlayerAccount):
    logger.info("[{}] get mail meta info".format(account.uid))
    data = META_INFO_DATA.copy()
    data["from"] = int(time.time())
    ret_data = http_client.post_with_seqnum(account, META_INFO_URL,
                                            data=json.dumps(data))
    return ret_data


LIST_MAILBOX_URL = config.NetworkConfig.get_game_server_url("/mail/listMailBox")
LIST_MAILBOX_DATA = {
    "mailIdList": [],
    "sysMailIdList": []
}


@response_process_flow(logger,
                       update_player_delta(),
                       check_key("mailList"),
                       just_log("[{}] mail info get ok"))
def list_mail_box(account: PlayerAccount, *ids, id_list=None):
    id_list = [] if id_list == None else id_list
    id_list.extend(list(ids))
    logger.info("[{}] get mail info for id={}".format(account.uid, id_list))
    data = LIST_MAILBOX_DATA.copy()
    #todo: temporary solution
    data["mailIdList"] = list(filter(lambda x:int(x)>10000,id_list))
    data["sysMailIdList"] = list(filter(lambda x:int(x)<=10000,id_list))
    ret_data = http_client.post_with_seqnum(account, LIST_MAILBOX_URL,
                                            data=json.dumps(data))
    return ret_data


RECEIVE_ALL_MAIL_URL = config.NetworkConfig.get_game_server_url("/mail/receiveAllMail")
RECEIVE_ALL_MAIL_DATA = {
    "mailIdList": [],
    "sysMailIdList": [
    ]
}


@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] retrieved all mail"))
def receive_all_mail(account: PlayerAccount, *ids, id_list=None):
    id_list = [] if id_list == None else id_list
    id_list.extend(list(ids))
    logger.info("[{}] receive mail for id={}".format(account.uid, id_list))
    data = RECEIVE_ALL_MAIL_DATA.copy()
    # todo: temporary solution
    data["mailIdList"] = list(filter(lambda x: int(x) > 10000, id_list))
    data["sysMailIdList"] = list(filter(lambda x: int(x) <= 10000, id_list))
    ret_data = http_client.post_with_seqnum(account, RECEIVE_ALL_MAIL_URL,
                                            data=json.dumps(data))
    return ret_data


def receive_all_mail_with_item(account: PlayerAccount):
    logger.info("[{}] receive mail with item".format(account.username))
    meta_info = get_meta_info_list(account)
    if meta_info is None or len(meta_info) == 0:
        logger.info("[{}] no mail in the box or get mail fail".format(account.username))
        return
    id_list = [rs["mailId"] for rs in meta_info["result"]]
    mail_info = list_mail_box(account, id_list=id_list)
    if mail_info is None or len(mail_info) == 0:
        logger.info("[{}] no mail in the box or get mail fail".format(account.username))
        return
    valid_ids = []
    for mail in mail_info["mailList"]:
        if mail["hasItem"] == 1 and mail["state"] == 0:
            valid_ids.append(mail["mailId"])
    if len(valid_ids) == 0:
        logger.info("[{}] no mail need to be receive".format(account.username))
        return
    return receive_all_mail(account, id_list=valid_ids)
