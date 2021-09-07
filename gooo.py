import functools

from client.config import ConfigServerName
from client.data_model import MissionModel
from client.data_model.akaccount import PlayerAccount
from client.api import auth_server, game_server,config_server,data_server
import time
from client.data_model.mission import get_mission_by_type, MissionType

data_server.update_mission_table()
data_server.update_character_table()
data_server.update_skin_table()

data_server.update_item_table()
data_server.update_gacha_table()
print(config_server.get_version())
print(config_server.get_network(ConfigServerName.OFFICIAL.value))

acc = PlayerAccount.init_random_device()

acc.username = "miao"
acc.password = "miao"
# # acc = load_from_file("tempuser.json")
# # auth_server.auth(acc)
auth_server.login(acc)
time.sleep(1)
auth_server.ping(acc)
time.sleep(1)
auth_server.get_token(acc)
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
# # save_to_file(acc,"tempuser.json")
# # acc = load_from_file("tempuser.json")
# game_server.checkin(acc)
# game_server.mail.receive_all_mail_with_item(acc)
# print(game_server.social.get_friend_info(acc,"634747842"))
# print(game_server.social.get_current_friend(acc))
# print(game_server.social.search_player_info_by_uid(acc,"634747842"))
# print(game_server.social.search_account(acc,nickname="海猫"))
# print(game_server.battle.start_battle_replay(acc,"quest","main_00-01"))
# print(acc.current_battle)
# time.sleep(20)
# print(game_server.battle.finish_battle(acc,"main_00-01"))

# print(game_server.building.sync_building(acc))
# time.sleep(2)
# print(game_server.building.get_all_intimacy(acc))
# time.sleep(2)
# print(game_server.building.settle_manufacture(acc))
# time.sleep(2)
# print(game_server.building.delivery_batch_order(acc))
# time.sleep(2)
#
# game_server.mission.confirm_mission_by_type(acc,"DAILY")
# game_server.mission.exchange_mission_reward_by_type(acc,"DAILY")