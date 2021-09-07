import json

from client.api import http_client, logger
from client.config import get_resource_path

logger = logger.getChild("data_server")

GAME_DATA_URL = "https://cdn.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master/zh_CN/gamedata/excel/{}"

MISSION_TABLE_URL = "https://cdn.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master/zh_CN/gamedata/excel/mission_table.json"
CHARACTER_TABLE_URL = "https://cdn.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master/zh_CN/gamedata/excel/character_table.json"
SKIN_TABLE_URL = "https://cdn.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master/zh_CN/gamedata/excel/skin_table.json"
ITEM_TABLE_URL = "https://cdn.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master/zh_CN/gamedata/excel/item_table.json"
STAGE_TABLE_URL = "https://cdn.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master/zh_CN/gamedata/excel/stage_table.json"

def data_updater(datafile):
    logger.info("updating {}".format(datafile))
    data = http_client.get(None, GAME_DATA_URL.format(datafile))
    if data is None:
        logger.error("updating {} fail".format(datafile))
        return
    with open(get_resource_path(datafile), "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
    logger.info("success")
    return data

def update_mission_table():
    logger.info("updating mission table")
    data = http_client.get(None,MISSION_TABLE_URL)
    if data is None:
        logger.error("updating mission table fail")
        return
    with open(get_resource_path("mission_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))
    logger.info("success")
    return data

def update_character_table():
    logger.info("updating character table")
    data = http_client.get(None,CHARACTER_TABLE_URL)
    if data is None:
        logger.error("updating character table fail")
        return
    with open(get_resource_path("character_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))
    logger.info("success")
    return data

def update_skin_table():
    logger.info("updating skin table")
    data = http_client.get(None,SKIN_TABLE_URL)
    if data is None:
        logger.error("updating skin table fail")
        return
    with open(get_resource_path("skin_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))
    logger.info("success")
    return data

def update_item_table():
    logger.info("updating item table")
    data = http_client.get(None,ITEM_TABLE_URL)
    if data is None:
        logger.error("updating item table fail")
        return
    with open(get_resource_path("item_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))
    logger.info("success")
    return data

def update_stage_table():
    logger.info("updating stage table")
    data = http_client.get(None,STAGE_TABLE_URL)
    if data is None:
        logger.error("updating stage table fail")
        return
    with open(get_resource_path("stage_table.json"),"w",encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))
    logger.info("success")
    return data

def update_gacha_table():
    return data_updater("gacha_table.json")