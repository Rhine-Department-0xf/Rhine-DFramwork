import json
import time

from client import config
from client.data_model import mission as mission_model
from client.data_model.akaccount import PlayerAccount
from client.api._api_process import response_process_flow
from client.api._api_process.response_processor import update_player_delta, just_log
from client.api.game_server import logger, http_client

logger = logger.getChild("mission")

CONFIRM_MISSION_URL = config.NetworkConfig.get_game_server_url("/mission/confirmMission")
CONFIRM_MISSION_DATA = {
    "missionId": "daily_4313"
}


@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] success"))
def confirm_mission(account: PlayerAccount, mission_id):
    logger.info("[{}] confirm mission id={}".format(account.uid,
                                                    mission_id))
    data = CONFIRM_MISSION_DATA.copy()
    data["missionId"] = mission_id
    ret_data = http_client.post_with_seqnum(account,
                                            CONFIRM_MISSION_URL,
                                            data=json.dumps(data))
    return ret_data


def confirm_all_mission(account: PlayerAccount):
    missions = list(filter(lambda m: m.can_confirm(), mission_model.get_all_mission(account)))
    logger.info("[{}] confirming all mission, {} left".format(account.uid,
                                                              len(missions)))
    if len(missions) == 0:
        logger.info("[{}] all mission can be confirmed have been confirmed".format(account.uid))
        return
    for mission in missions:
        mission: mission_model.Mission
        ret = confirm_mission(account, mission.id)
        if ret is None:
            logger.error("[{}] stop confirming mission due to http connection error".format(account.uid))
            return
    logger.info("[{}] try to get more mission".format(account.uid))
    confirm_all_mission(account)


def confirm_mission_by_type(account: PlayerAccount, mission_type):
    missions = list(filter(lambda m: m.can_confirm(), mission_model.get_mission_by_type(account, mission_type)))
    logger.info("[{}] confirming mission type = {}, {} left".format(account.uid,
                                                                    mission_type,
                                                                    len(missions)))
    if len(missions) == 0:
        logger.info("[{}] all mission can be confirmed have been confirmed".format(account.uid))
        return
    for mission in missions:
        mission: mission_model.Mission
        ret = confirm_mission(account, mission.id)
        if ret is None:
            logger.error("[{}] stop confirming mission due to http connection error".format(account.uid))
            return
        if ret.get("playerDataDelta") is None:
            logger.error("[{}] stop confirming mission due to api error".format(account.uid))
            return
    logger.info("[{}] try to get more mission".format(account.uid))
    confirm_mission_by_type(account, mission_type)


EXCHANGE_MISSION_REWARDS_URL = config.NetworkConfig.get_game_server_url("/mission/exchangeMissionRewards")
EXCHANGE_MISSION_REWARDS_DATA = {
    "targetRewardsId": "reward_daily_388"
}


@response_process_flow(logger,
                       update_player_delta(),
                       just_log("[{}] success"))
def exchange_mission_reward(account: PlayerAccount, reward_id):
    logger.info("[{}] exchange mission reward id={}".format(account.uid,
                                                            reward_id))
    data = EXCHANGE_MISSION_REWARDS_DATA.copy()
    data["targetRewardsId"] = reward_id
    ret_data = http_client.post_with_seqnum(account,
                                            EXCHANGE_MISSION_REWARDS_URL,
                                            data=json.dumps(data))
    return ret_data


def exchange_mission_reward_by_type(account: PlayerAccount, mission_type):
    mission_rewards = list(
        filter(lambda m: m.can_exchange(), mission_model.get_mission_rewards_by_type(account, mission_type)))
    logger.info("[{}] exchange mission reward type = {}, {} left".format(account.uid,
                                                                         mission_type,
                                                                         len(mission_rewards)))
    if len(mission_rewards) == 0:
        logger.info("[{}] all mission rewards can be exchange have been exchanged".format(account.uid))
        return
    for mission_reward in mission_rewards:
        mission_reward: mission_model.MissionReward
        ret = exchange_mission_reward(account, mission_reward.id)
        if ret is None:
            logger.error("[{}] stop exchange mission reward due to http connection error".format(account.uid))
            return
        if ret.get("playerDataDelta") is None:
            logger.error("[{}] stop exchange mission reward due to api error".format(account.uid))
            return
    logger.info("[{}] try to exchange more mission".format(account.uid))
    exchange_mission_reward_by_type(account, mission_type)