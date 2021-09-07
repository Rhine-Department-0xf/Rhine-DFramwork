import traceback

import jsonclass
from client import config
from client.db import logger

class ItemDBData():
    def __init__(self):
        self.itemId = None
        self.name = None
        self.description = None
        self.rarity = None
        self.iconId = None
        self.overrideBkg = None
        self.stackIconId = None
        self.sortId = None
        self.usage = None
        self.obtainApproach = None
        self.classifyType = None
        self.itemType = None
        self.stageDropList = None
        self.buildingProductList = None


ItemDB = {}
def __load_data():
    global ItemDB
    try:
        ItemDB = {}
        for key, val in config.load_json_resource("item_table.json")["items"].items():
            ItemDB[key] = jsonclass.json_unmarshall(ItemDBData, val)
    except:
        traceback.print_exc()
        logger.warn("Fail to load item_table.json")

__load_data()
def get_item_data(itemId) -> ItemDBData:
    return ItemDB.get(itemId)

def get_item_data_by_name(name)-> ItemDBData:
    for val in ItemDB.values():
        if val.name == name:
            return val
    return None