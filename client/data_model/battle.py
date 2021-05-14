import json
import random
import time

from client import encryption, config
from client.data_model import ArkEnum


class BattleType(ArkEnum):
    QUEST = "quest"
    CAMPAIGNS = "campaignsV2"

class Battle():
    def __init__(self, account, b_type, stage_id, start_time=None):
        self.account = account
        self.type = b_type
        self.stage_id = stage_id
        self.battle_id = ""
        self.start_time = int(time.time()) if start_time is None else start_time
        self.end_time = 0
        self.complete_time = 0

    def __str__(self):
        return "<Battle type={} id={} start_time={}>".format(self.type,self.battle_id,self.start_time)

    def __repr__(self):
        return self.__str__()

    @property
    def battle_type(self):
        return BattleType(self.type)

    @property
    def is_cheat(self):
        return encryption.encrypt_battle_id(self.battle_id)

    @property
    def random_complete_time(self):
        return int((random.random() * 0.233 + 0.666) * (self.end_time - self.start_time))

    def has_battle_data(self):
        return config.load_battle_data(self.stage_id) is not None

    def get_battle_data(self, end_time=None,complete_time=None):
        self.end_time = int(time.time()) if end_time is None else end_time
        self.complete_time = self.random_complete_time if complete_time is None else complete_time
        data = config.load_battle_data(self.stage_id)
        if data is None:
            return ""
        data["battleId"] = self.battle_id
        data['battleData']['isCheat'] = self.is_cheat

        data['battleData']['stats']['beginTs'] = self.start_time
        data['battleData']['stats']['endTs'] = self.end_time
        data['battleData']['completeTime'] = self.complete_time

        hash_key = data['battleData']['stats'].get("hash")
        if hash_key is None:
            data['battleData']['stats']["access"] = encryption.get_battle_data_access(self.account.login_time)
        else:
            data['battleData']['stats']["access"] = encryption.get_battle_data_access(self.account.login_time,
                                                                                      hash_key=hash_key)
        return encryption.encrypt_battle_data(json.dumps(data,separators=(',', ':')),
                                              self.account.login_time)