import jsonclass


class Stage():
    def __init__(self):
        self.stageId = None
        self.completeTimes = None
        self.startTimes = None
        self.practiceTimes = None
        self.state = None
        self.hasBattleReplay = None
        self.noCostCnt = None