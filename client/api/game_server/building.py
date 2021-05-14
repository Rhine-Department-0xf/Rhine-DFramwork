import json

from client import config
from client.api import http_client
from client.api._api_process import response_process_flow
from client.api._api_process.response_processor import update_player_delta, just_log
from client.api.game_server import logger
from client.data_model.akaccount import PlayerAccount
from client.data_model import BuildingModel

logger = logger.getChild("building")

BUILDING_SYNC_URL = config.NetworkConfig.get_game_server_url("/building/sync")
BUILDING_SYNC_DATA = {}
@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] sync building success..."))
def sync_building(account:PlayerAccount):
    logger.info("[{}] sync building..".format(account.uid))
    ret_data = http_client.post_with_seqnum(account, BUILDING_SYNC_URL,
                                            data=json.dumps(BUILDING_SYNC_DATA))
    return ret_data

GAIN_ALL_INTIMACY_URL = config.NetworkConfig.get_game_server_url("/building/gainAllIntimacy")
GAIN_ALL_INTIMACY_DATA = {}
@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] get all intimacy success"))
def get_all_intimacy(account:PlayerAccount):
    logger.info("[{}] getting all intimacy..".format(account.uid))
    ret_data = http_client.post_with_seqnum(account, GAIN_ALL_INTIMACY_URL,
                                            data=json.dumps(GAIN_ALL_INTIMACY_DATA))
    return ret_data



SETTLE_MANUFACTURE_URL = config.NetworkConfig.get_game_server_url("/building/settleManufacture")
SETTLE_MANUFACTURE_DATA = {
    "roomSlotIdList": [
        "slot_6",
        "slot_5",
        "slot_7"
    ],
    "supplement": 1
}
@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] settle manufacture success"))
def settle_manufacture(account:PlayerAccount,*ids,slot_ids=None):
    slot_ids = [] if slot_ids is None else slot_ids
    slot_ids.extend(ids)
    if len(slot_ids) == 0:
        slot_ids = [room.slot_id for room in BuildingModel.get_room_by_type(account,"MANUFACTURE")]
    logger.info("[{}] settle manufacture for slot_ids={}".format(account.uid,slot_ids))
    data = SETTLE_MANUFACTURE_DATA.copy()
    data["roomSlotIdList"] = slot_ids
    ret_data = http_client.post_with_seqnum(account, SETTLE_MANUFACTURE_URL,
                                            data=json.dumps(data))
    return ret_data

DELIVERY_BATCH_ORDER_URL = config.NetworkConfig.get_game_server_url("/building/deliveryBatchOrder")
DELIVERY_BATCH_ORDER_DATA = {
    "slotList": [
        "slot_15",
        "slot_14",
        "slot_24"
    ]
}
@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] delivery batch order success"))
def delivery_batch_order(account:PlayerAccount,*ids,slot_ids=None):
    slot_ids = [] if slot_ids is None else slot_ids
    slot_ids.extend(ids)
    if len(slot_ids) == 0:
        slot_ids = [room.slot_id for room in BuildingModel.get_room_by_type(account,"TRADING")]
    logger.info("[{}] delivery batch order for slot_ids={}".format(account.uid,slot_ids))
    data = DELIVERY_BATCH_ORDER_DATA.copy()
    data["slotList"] = slot_ids
    ret_data = http_client.post_with_seqnum(account, DELIVERY_BATCH_ORDER_URL,
                                            data=json.dumps(data))
    return ret_data