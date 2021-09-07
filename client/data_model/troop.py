class CharacterSkill():
    def __init__(self):
        self.skillId = None
        self.unlock = None
        self.state = None
        self.specializeLevel = None
        self.completeUpgradeTime = None

class Character():
    def __init__(self):
        self.instId = None
        self.charId = None
        self.favorPoint = None
        self.potentialRank = None
        self.mainSkillLvl = None
        self.skin = None
        self.level = None
        self.exp = None
        self.evolvePhase = None
        self.defaultSkillIndex = None
        self.gainTime = None
        self.skills = [CharacterSkill]