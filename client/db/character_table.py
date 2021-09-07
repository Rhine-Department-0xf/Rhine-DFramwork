import traceback

import jsonclass
from client import config
from client.db import logger
class CharacterDBData():
    def __init__(self):
        self.name = None
        self.description = None
        self.canUseGeneralPotentialItem = None
        self.potentialItemId = None
        self.nationId = None
        self.groupId = None
        self.teamId = None
        self.displayNumber = None
        self.tokenKey = None
        self.appellation = None
        self.position = None
        self.tagList = None
        self.itemUsage = None
        self.itemDesc = None
        self.itemObtainApproach = None
        self.isNotObtainable = None
        self.isSpChar = None
        self.maxPotentialLevel = None
        self.rarity = None
        self.profession = None
        self.trait = None
        self.phases = None
        self.skills = None
        self.talents = None
        self.potentialRanks = None
        self.favorKeyFrames = None
        self.allSkillLvlup = None

CharacterDB = {}
def __load_data():
    global CharacterDB
    try:
        CharacterDB = {}
        for key, val in config.load_json_resource("character_table.json").items():
            CharacterDB[key] = jsonclass.json_unmarshall(CharacterDBData, val)
    except:
        traceback.print_exc()
        logger.warn("Fail to load character_table.json")

__load_data()
def get_character_data(charId) -> CharacterDBData:
    return CharacterDB.get(charId)

def get_character_data_by_name(name)-> CharacterDBData:
    for val in CharacterDB.values():
        if val.name == name:
            return val
    return None

def get_character_data_by_appellation(appellation)-> CharacterDBData:
    for val in CharacterDB.values():
        if val.appellation == appellation:
            return val
    return appellation