import json

from client import utils
import os

class PlayerAccount():
    def __init__(self):
        self.username = ""
        self.password = ""
        self.uid = ""
        self.channel_uid = ""
        self.guest = False
        self.access_token = ""  # token from u8 server, used for auth server
        self.token = ""  # token get from access_token, used for login to gameserver
        self.secret = ""
        self.seqnum = 0
        self.login_time = 0

        self.device_id = ""
        self.device_id2 = ""
        self.device_id3 = ""

        self.data = {}

        # from battle
        self.current_battle = {}

    @classmethod
    def init_random_device(cls):
        a = cls()
        a.device_id = utils.get_random_device_id()
        a.device_id2 = utils.get_random_device_id2()
        return a

    @classmethod
    def init_from_json(cls, data):
        try:
            a = cls()
            a.load_json(data)
            return a
        except:
            return None

    def load_json(self, data):
        self.username = data["username"]
        self.password = data["password"]
        self.uid = data["uid"]
        self.channel_uid = data["channel_uid"]
        self.access_token = data["access_token"]
        self.token = data["token"]
        self.secret = data["secret"]
        self.seqnum = data["seqnum"]
        self.login_time = data["login_time"]
        self.device_id = data["device_id"]
        self.device_id2 = data["device_id2"]
        self.device_id3 = data["device_id3"]

    def to_json(self):
        return {"username": self.username,
                "password": self.password,
                "uid": self.uid,
                "channel_uid": self.channel_uid,
                "access_token": self.access_token,
                "token": self.token,
                "secret": self.secret,
                "seqnum": self.seqnum,
                "login_time": self.login_time,
                "device_id": self.device_id,
                "device_id2": self.device_id2,
                "device_id3": self.device_id3}

    def update_data(self, modified):
        self.data = utils.deep_update(self.data, modified)


def load_from_file(path):
    if os.path.exists(path):
        try:
            with open(path,"r",encoding="utf-8") as f:
                return PlayerAccount.init_from_json(json.loads(f.read()))
        except:
            pass
    return None


def save_to_file(account:PlayerAccount,path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(account.to_json(),indent=4))
    except:
        pass