import traceback

import jsonclass
from client import config
from client.db import logger

class GachaDBDataPoolClient():
    def __init__(self):
        self.gachaPoolId = None
        self.gachaIndex = None
        self.openTime = None
        self.endTime = None
        self.gachaPoolName = None
        self.gachaPoolSummary = None
        self.gachaPoolDetail = None
        self.guarantee5Avail = None
        self.guarantee5Count = None
        self.CDPrimColor = None
        self.CDSecColor = None
        self.LMTGSID = None
        self.gachaRuleType = None

GachaDB = {}
def __load_data():
    global GachaDB
    try:
        GachaDB = {}
        for val in config.load_json_resource("gacha_table.json")["gachaPoolClient"]:
            GachaDB[val["gachaPoolId"]] = jsonclass.json_unmarshall(GachaDBDataPoolClient, val)
    except:
        traceback.print_exc()
        logger.warn("Fail to load gacha_table.json")

__load_data()

def get_gacha_pool_data(PoolId) -> GachaDBDataPoolClient:
    return GachaDB.get(PoolId)