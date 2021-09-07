
import functools

from client.config import ConfigServerName, LoginParaBilibili
from client.data_model import MissionModel
from client.data_model.akaccount import PlayerAccount
from client.api import auth_server, game_server,config_server,data_server
import time
from client.data_model.mission import get_mission_by_type, MissionType

print(config_server.get_version())
print(config_server.get_network(ConfigServerName.BILIBILI.value))

acc = PlayerAccount.init_random_device()
acc.device_id = "a96df156d79640461a0d49511f490129"
acc.device_id2 = "910000000146166"
acc.device_id3 = ""
acc.access_token = "f500b56eff8233cb35c984a988a1308b_sh"
auth_server.get_token(acc,LoginParaBilibili)
time.sleep(1)
game_server.login(acc)
time.sleep(1)
game_server.sync_data(acc)
time.sleep(1)
game_server.get_unconfirmed_order(acc)
time.sleep(1)
game_server.sync_status(acc)
time.sleep(1)
game_server.mission.auto_confirm_missions_by_type(acc,MissionType.DAILY.value)