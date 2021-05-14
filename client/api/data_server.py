import json

from client.api import http_client, logger
from client.config import get_resource_path

logger = logger.getChild("data_server")

MISSION_TABLE_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/mission_table.json"
CHARACTER_TABLE_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json"
SKIN_TABLE_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/skin_table.json"


def update_mission_table():
    logger.info("updating mission table")
    data = http_client.get(None,MISSION_TABLE_URL)
    if data is None:
        logger.error("updating mission table fail")
        return
    with open(get_resource_path("mission_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2))
    logger.info("success")
    return data

def update_character_table():
    logger.info("updating character table")
    data = http_client.get(None,CHARACTER_TABLE_URL)
    if data is None:
        logger.error("updating character table fail")
        return
    with open(get_resource_path("character_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2))
    logger.info("success")
    return data

def update_skin_table():
    logger.info("updating skin table")
    data = http_client.get(None,SKIN_TABLE_URL)
    if data is None:
        logger.error("updating skin table fail")
        return
    with open(get_resource_path("skin_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2))
    logger.info("success")
    return data