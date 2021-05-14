from mitmproxy.http import HTTPFlow,HTTPResponse

from client import encryption
from mitm.addons import ArkInterceptor
import json

class decryptBattleData(ArkInterceptor):

    def __init__(self):
        self.login_time = 0

    def response(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/account/syncData"):
            data = json.loads(flow.response.get_text())
            self.login_time = data["user"]['pushFlags']['status']
            self.info("get login time")
            return
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/quest/battleFinish"):
            data = json.loads(flow.request.content)
            print(encryption.decrypt_battle_data(data["data"],self.login_time))