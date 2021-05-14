from enum import Enum


class ArkEnum(Enum):

    @classmethod
    def get_all(cls):
        return [c for c in cls]

    @classmethod
    def get_names(cls):
        return [c.name for c in cls]

    @classmethod
    def get_values(cls):
        return [c.value for c in cls]

    @classmethod
    def get_value_or_default(cls, name):
        if isinstance(name, str):
            try:
                return cls(name).value
            except:
                for en in cls:
                    return en.value
        else:
            return name.value


from client.data_model import akaccount as AccountModel
from client.data_model import mission as MissionModel
from client.data_model import battle as BattleModel
from client.data_model import building as BuildingModel