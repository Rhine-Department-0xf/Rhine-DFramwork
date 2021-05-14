import json

from mitmproxy.http import HTTPFlow, HTTPResponse

from mitm.addons import ArkInterceptor


class TestFor(ArkInterceptor):
    def __init__(self):
        self.info("Loading success")

    def response(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            print(self.tBuilder.getCharData("char_172_svrash"))
            self.tBuilder.getCharData("char_172_svrash")["skin"] = "char_180_amgoat#2"
            print(self.tBuilder.getCharData("char_172_svrash"))
            flow.response.set_text(json.dumps(data))
            self.info("Complete")

class MonsterSirenMusic(ArkInterceptor):
    def __init__(self, mode="weak"):
        self.mode = mode
        self.info("Loading success, mode %s" % self.mode)

    def response(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith(
                "/announce/Android/announcement.meta.json"):
            data = json.loads(flow.response.get_text())
            data["announceList"][0]["webUrl"] = "https://monster-siren.hypergryph.com/"
            flow.response.set_text(json.dumps(data))
            self.info("Complete")

        if flow.request.host == "monster-siren.hypergryph.com" and (flow.request.path == "/" or
                                                                    flow.request.path == "/m"):
            data = flow.response.get_text()
            data = data.replace("</body>",
                                "<style>body {overflow:auto}.albumDetail___ML1yw{overflow:auto}</style></body>")
            flow.response.set_text(data)
            self.info("set overflow")
            print(flow.response.get_text())
