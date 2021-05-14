import json

from mitmproxy.http import HTTPFlow

from mitm.addons import ArkInterceptor
from client import encryption

class changeSeed(ArkInterceptor):

    def __init__(self,seed):
        self.seed = seed
        self.info("Loading success")

    def request(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/quest/saveBattleReplay"):
            data = json.loads(flow.request.get_text())
            b_data = json.loads(encryption.decrypt_battle_replay(data["battleReplay"]))
            b_data["journal"]["randomSeed"] = self.seed
            data["battleReplay"] = encryption.encrypt_battle_replay(json.dumps(b_data,separators=(',', ':')))
            flow.request.set_text(json.dumps(data))