import json

from client import config
from client.data_model.akaccount import PlayerAccount
from client.api._api_process import response_process_flow
from client.api._api_process.response_processor import update_player_delta, just_log
from client.api.game_server import logger, http_client

CHECKIN_URL = config.NetworkConfig.get_game_server_url("/user/checkIn")
CHECKIN_DATA = {}

@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] check in success..."))
def checkin(account:PlayerAccount):
    logger.info("[{}] checkin".format(account.uid))
    ret_data = http_client.post_with_seqnum(account, CHECKIN_URL,
                                            data=json.dumps(CHECKIN_DATA))
    return ret_data