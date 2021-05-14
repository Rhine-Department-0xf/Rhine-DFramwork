from client.data_model import ArkEnum
from client.data_model.akaccount import PlayerAccount


class RoomTypeString(ArkEnum):
    CONTROL = "CONTROL"
    POWER = "POWER"
    MANUFACTURE = "MANUFACTURE"
    SHOP = "SHOP"
    DORMITORY = "DORMITORY"
    MEETING = "MEETING"
    HIRE = "HIRE"
    ELEVATOR = "ELEVATOR"
    CORRIDOR = "CORRIDOR"
    TRADING = "TRADING"
    WORKSHOP = "WORKSHOP"
    TRAINING = "TRAINING"

class Room():
    def __init__(self,slot_id,r_type):
        self.slot_id = slot_id
        self.type = r_type

    @property
    def room_type(self):
        return RoomTypeString(self.type)


def get_all_room(account:PlayerAccount):
    rooms = []
    for slot_id,slot_data in account.data["building"]["roomSlots"].items():
        rooms.append(Room(slot_id,slot_data["roomId"]))
    return rooms

def get_room_by_type(account:PlayerAccount,room_type):
    room_type = RoomTypeString.get_value_or_default(room_type)
    if account.data["building"]["rooms"].get(room_type) is None:
        return []
    return [Room(slot_id,room_type) for slot_id in account.data["building"]["rooms"].get(room_type).keys()]