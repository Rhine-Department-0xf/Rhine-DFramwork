import json
import os
from enum import Enum
import urllib.parse


Data_Path = r"D:\Repository\Rhine-Department-0xf\data"

def get_resource_path(resource):
    return os.path.join(Data_Path,resource)

def load_json_resource(resource):
    with open(get_resource_path(resource), "r", encoding="utf-8") as f:
        return json.loads(f.read())

def load_battle_data(stage_id):
    path = get_resource_path("battle_data/{}.json".format(stage_id))
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.loads(f.read())
    return None

class ProductionConfig():
    assetsVersion = "21-04-20-13-10-55-17ee8d"
    clientVersion = "1.5.01"

class NetworkConfig():
    version = "5"
    network = {}
    game_server = "https://ak-gs-gf.hypergryph.com"
    auth_server = "https://as.hypergryph.com"

    @classmethod
    def get_game_server_url(cls,path):
        return urllib.parse.urljoin(cls.game_server,path)

    @classmethod
    def get_auth_server_url(cls, path):
        return urllib.parse.urljoin(cls.game_server, path)

class LoginPara(Enum):
    APP_ID = "1"
    CHANNEL_ID = "1"
    WORLD_ID = "1"
    SUB_CHANNEL = "1"
    NETWORK_VERSION = "5"

class PlatformName(Enum):
    NONE = "Android"
    IOS = "IOS"
    ANDROID = "Android"

class PlatformKey(Enum):
    NONE = -1
    IOS = 0
    ANDROID = 1


class EnvironmentConfig():
    platform_key = PlatformKey.ANDROID
    platform_name = PlatformName.ANDROID
