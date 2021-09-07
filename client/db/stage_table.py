import traceback

import jsonclass
from client import config
from client.db import logger

class StageDBData():
    def __init__(self):
        self.stageType = None
        self.difficulty = None
        self.performanceStageFlag = None
        self.unlockCondition = None
        self.stageId = None
        self.levelId = None
        self.zoneId = None
        self.code = None
        self.name = None
        self.description = None
        self.hardStagedId = None
        self.dangerLevel = None
        self.dangerPoint = None
        self.loadingPicId = None
        self.canPractice = None
        self.canBattleReplay = None
        self.apCost = None
        self.apFailReturn = None
        self.etItemId = None
        self.etCost = None
        self.etFailReturn = None
        self.etButtonStyle = None
        self.apProtectTimes = None
        self.diamondOnceDrop = None
        self.practiceTicketCost = None
        self.dailyStageDifficulty = None
        self.expGain = None
        self.goldGain = None
        self.loseExpGain = None
        self.loseGoldGain = None
        self.passFavor = None
        self.completeFavor = None
        self.slProgress = None
        self.displayMainItem = None
        self.hilightMark = None
        self.bossMark = None
        self.isPredefined = None
        self.isHardPredefined = None
        self.isStoryOnly = None
        self.appearanceStyle = None
        self.stageDropInfo = None
        self.startButtonOverrideId = None
        self.isStagePatch = None
        self.mainStageId = None


StageDB = {}
def __load_data():
    global StageDB
    try:
        StageDB = {}
        for key, val in config.load_json_resource("stage_table.json")["stages"].items():
            StageDB[key] = jsonclass.json_unmarshall(StageDBData, val)
    except:
        traceback.print_exc()
        logger.warn("Fail to load stage_table.json")

__load_data()
def get_stage_data(stageId) -> StageDBData:
    return StageDB.get(stageId)

def get_stage_data_by_code(code)-> StageDBData:
    for val in StageDB.values():
        if val.code == code:
            return val
    return None

def get_stage_data_by_name(name)-> StageDBData:
    for val in StageDB.values():
        if val.name == name:
            return val
    return None