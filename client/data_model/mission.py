import json
from enum import Enum
from functools import reduce

from client import utils, config
from client.data_model import ArkEnum
from client.data_model.akaccount import PlayerAccount


class MissionState(ArkEnum):
    VANISH = 1
    IN_PROGRESS = 2
    FINISH = 3


class MissionType(ArkEnum):
    OPENSERVER = "OPENSERVER"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    GUIDE = "GUIDE"
    MAIN = "MAIN"
    ACTIVITY = "ACTIVITY"
    SUB = "SUB"


class MissionData():
    data = config.load_json_resource("mission_table.json")

    @classmethod
    def get_data_by_type(cls, m_type):
        if m_type == "WEEKLY":
            return cls.data["weeklyRewards"]
        if m_type == "DAILY":
            return cls.data["periodicalRewards"]
        return {}


class Mission():
    def __init__(self, account, id, m_type):
        self.account = account
        self.id = id
        self.type = m_type

    def __str__(self):
        return "<Mission id={} type={} state={} progress={} con_confirm={}>".format(self.id,
                                                                                    self.type,
                                                                                    self.state,
                                                                                    self.progress,
                                                                                    self.can_confirm())

    def __repr__(self):
        return self.__str__()

    @property
    def _data(self):
        return self.account.data["mission"]["missions"][self.type][self.id]

    @property
    def state(self):
        return self._data["state"]

    @property
    def progress(self):
        return self._data["progress"]

    @property
    def mission_state(self):
        return MissionState(self.state)

    @property
    def mission_type(self):
        return MissionType(self.type)

    def can_confirm(self):
        return self.state == MissionState.IN_PROGRESS.value and self.is_finish()

    def is_finish(self):
        return reduce(lambda x, y: x and y, map(lambda p: p["target"] == p["value"], self.progress))


def get_all_mission(account: PlayerAccount):
    missions = []
    for mission_type, data_a in account.data["mission"]["missions"].items():
        for mission_id in data_a.keys():
            missions.append(Mission(account, mission_id, mission_type))
    return missions


def get_mission_by_type(account: PlayerAccount, m_type):
    m_type = (MissionType(m_type) if isinstance(m_type, str) else m_type).value
    missions = []
    if account.data["mission"]["missions"].get(m_type) is None:
        return []
    for mission_id in account.data["mission"]["missions"][m_type].keys():
        missions.append(Mission(account, mission_id, m_type))
    return missions


class MissionReward():
    def __init__(self, account, id, m_type, pre_prerequisite=None):
        self.account = account
        self.id = id
        self.type = m_type
        self.pre_prerequisite = pre_prerequisite

    def __str__(self):
        return "<MissionReward id={} type={} state={} progress={}/{} con_exchange={}>".format(self.id,
                                                                                              self.type,
                                                                                              self.state,
                                                                                              self.current_point,
                                                                                              self.target_point,
                                                                                              self.can_exchange())

    def __repr__(self):
        return self.__str__()

    @property
    def _data(self):
        return self.account.data["mission"]["missionRewards"]["rewards"][self.type][self.id]

    @property
    def state(self):
        return self._data

    @property
    def target_point(self):
        data = MissionData.get_data_by_type(self.type).get(self.id)
        return -1 if data is None else data["periodicalPointCost"]

    @property
    def current_point(self):
        point = self.account.data["mission"]["missionRewards"].get(self.type.lower() + "Point")
        return -1 if point is None else point

    def reach_point(self):
        return self.current_point >= self.target_point

    def is_exchanged(self):
        return bool(self.state)

    def can_exchange(self):
        if self.pre_prerequisite is None:
            return not self.is_exchanged() and self.reach_point()
        else:
            return self.pre_prerequisite.is_exchanged() and not self.is_exchanged() and self.reach_point()


def get_mission_rewards_by_type(account: PlayerAccount, m_type):
    m_type = (MissionType(m_type) if isinstance(m_type, str) else m_type).value
    missions = []
    data = account.data["mission"]["missionRewards"]["rewards"].get(m_type)
    if data is None:
        return []
    pre = None
    for mission_id in data.keys():
        now = MissionReward(account, mission_id, m_type, pre_prerequisite=pre)
        missions.append(now)
        pre = now
    return missions
