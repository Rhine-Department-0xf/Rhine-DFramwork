import json

from client import config
from client.api import http_client
from client.api._api_process import response_process_flow
from client.api._api_process.response_processor import update_player_delta, just_log
from client.api.game_server import logger
from client.data_model.akaccount import PlayerAccount
from client.data_model import BattleModel

logger = logger.getChild("battle")

BATTLE_START_URL = config.NetworkConfig.get_game_server_url("/{battle_type}/battleStart")
BATTLE_START_REPLAY_DATA = {
    "assistFriend": None,
    "isReplay": 1,
    "isRetro": 0,
    "squad": {
        "name": None,
        "slots": [
            {
                "charInstId": 2,
                "skillIndex": -1
            },
            None, None, None, None, None,
            None, None, None, None, None, None
        ],
        "squadId": "0"
    },
    "stageId": "",
    "startTs": 1619682747,
    "usePracticeTicket": 0
}


@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] start battle replay success"))
def start_battle_replay(account: PlayerAccount, battle_type, stage_id):
    battle_type = BattleModel.BattleType.get_value_or_default(battle_type)
    api = BATTLE_START_URL.format(battle_type=battle_type)
    data = BATTLE_START_REPLAY_DATA.copy()
    mybattle = BattleModel.Battle(account, battle_type, stage_id)
    if not mybattle.has_battle_data():
        logger.error("[{}] battle reply data for stage id={} not found".format(account.uid,
                                                                               stage_id))
        return
    if account.current_battle.get(stage_id) is not None:
        logger.warning("[{}] already start battle for stage id={}".format(account.uid,
                                                                          stage_id))
        return
    logger.info("[{}] starting battle stage_id={}".format(account.uid,
                                                          stage_id))
    data["stageId"] = stage_id
    # simulate system delay
    data["startTs"] = mybattle.start_time - 1
    ret_data = http_client.post_with_seqnum(account,
                                            api,
                                            data=json.dumps(data))
    if ret_data.get("battleId") is None:
        logger.warning("[{}] fail to start battle replay, reason: {}".format(account.uid, ret_data))
        return ret_data
    mybattle.battle_id = ret_data.get("battleId")
    account.current_battle[stage_id] = mybattle
    return ret_data


BATTLE_FINISH_URL = config.NetworkConfig.get_game_server_url("/{battle_type}/battleFinish")
BATTLE_FINISH_DATA = {
    "battleData": {
        "completeTime": 42,
        "isCheat": "aWttOjc9PTc0aD9qNzQ4OGxpNGg3a2w0OGlta2s8Nzg4OGk6",
        "stats": {}
    },
    "data": ""
}


@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] finish battle success"))
def finish_battle(account: PlayerAccount, stage_id):
    mybattle: BattleModel.Battle = account.current_battle.get(stage_id)
    api = BATTLE_FINISH_URL.format(battle_type=mybattle.type)
    if mybattle is None:
        logger.warning("[{}] battle for stage id={} is finished or not started".format(account.uid,
                                                                                       stage_id))
    logger.info("[{}] finishing battle stage id={} battle_id={}".format(account.uid,
                                                                        stage_id,
                                                                        mybattle.battle_id))
    battle_data = mybattle.get_battle_data()
    data = BATTLE_FINISH_DATA.copy()
    data["data"] = battle_data
    data["battleData"]["completeTime"] = mybattle.complete_time
    data["battleData"]["isCheat"] = mybattle.is_cheat
    account.current_battle.pop(stage_id)
    ret_data = http_client.post_with_seqnum(account,
                                            api,
                                            data=json.dumps(data))
    return ret_data
