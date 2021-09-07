import json
import os
from enum import Enum
import urllib.parse

Data_Path = r"D:\Repository\Rhine-Department-0xf\data"


def get_resource_path(resource):
    return os.path.join(Data_Path, resource)


def load_json_resource(resource):
    with open(get_resource_path(resource), "r", encoding="utf-8") as f:
        return json.loads(f.read())


def load_battle_data(stage_id):
    path = get_resource_path("battle_data/{}.json".format(stage_id))
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    return None


class ProductionConfig():
    assetsVersion = "21-07-09-11-29-30-f11d8b"
    clientVersion = "1.5.40"


class NetworkConfig():
    version = "5"
    network = {}
    game_server = "https://ak-gs-gf.hypergryph.com"
    auth_server = "https://as.hypergryph.com"

    @classmethod
    def update_server_url(cls):
        try:
            cls.game_server = cls.network["gs"]
            cls.auth_server = cls.network["as"]
        except:
            cls.game_server = "https://ak-gs-gf.hypergryph.com"
            cls.auth_server = "https://as.hypergryph.com"

    @classmethod
    def get_game_server_url(cls, path):
        return urllib.parse.urljoin(cls.game_server, path)

    @classmethod
    def get_auth_server_url(cls, path):
        return urllib.parse.urljoin(cls.game_server, path)


class LoginPara():
    def __init__(self, app_id, channel_id, world_id, sub_channel, network_version):
        self.APP_ID = app_id
        self.CHANNEL_ID = channel_id
        self.WORLD_ID = world_id
        self.SUB_CHANNEL = sub_channel
        self.NETWORK_VERSION = network_version


LoginParaBilibili = LoginPara("1", "2", "2", "2", "5")
LoginParaAndroid = LoginPara("1", "1", "1", "1", "5")


class ConfigServerName(Enum):
    OFFICIAL = "official"
    BILIBILI = "b"


class PlatformName(Enum):
    NONE = "Android"
    IOS = "IOS"
    ANDROID = "Android"
    BILIBILI = "Bilibili"


class PlatformKey(Enum):
    NONE = -1
    IOS = 0
    ANDROID = 1


class EnvironmentConfig():
    platform_key = PlatformKey.ANDROID
    platform_name = PlatformName.ANDROID
