import traceback
from typing import Dict

import requests
from client.data_model.akaccount import PlayerAccount



def update_header(origin,extra):
    origin.update(extra)
    return origin

class ArknightsHttpClient:
    COMMON_HEADER = {
        "Content-Type": "application/json",
        'X-Unity-Version': "2017.4.39f1",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
        "Connection": "Keep-Alive",
    }

    def __init__(self, maxTrial=1):
        self.maxTrial = maxTrial

    def get(self,account:PlayerAccount,url,**kwargs):
        ret = self._get(url,**kwargs)
        return None if ret is None else ret.json()

    def get_with_seqnum(self,account:PlayerAccount,url,headers=None,**kwargs):
        secure_header = {
                'uid': int(account.uid),
                'secret': account.secret,
                'seqnum': account.seqnum
            }
        headers = secure_header if headers is None else update_header(headers,secure_header)
        ret = self._get(url,headers = headers,**kwargs)
        if ret is None:
            account.seqnum = account.seqnum + 1
            return None
        else:
            account.seqnum = int(ret.headers.get("Seqnum"))
            return ret.json()


    def post(self,account:PlayerAccount,url,**kwargs):
        ret = self._post(url,**kwargs)
        return None if ret is None else ret.json()

    def post_with_seqnum(self,account:PlayerAccount,url,headers=None,**kwargs):
        secure_header = {
                'uid': account.uid,
                'secret': account.secret,
                'seqnum': str(account.seqnum)
            }
        headers = secure_header if headers is None else update_header(headers,secure_header)
        ret = self._post(url,headers = headers,**kwargs)

        if ret is None:
            account.seqnum = account.seqnum + 1
            return None
        else:
            try:
                account.seqnum = int(ret.headers.get("Seqnum"))
            except:
                account.seqnum = account.seqnum
            return ret.json()


    def _get(self, url, headers=None, **kwargs):
        headers = self.COMMON_HEADER.copy() if headers is None else update_header(headers,self.COMMON_HEADER)
        trial = 0
        while trial < self.maxTrial:
            try:
                return requests.get(url, headers=headers, timeout=5, **kwargs)
            except:
                traceback.print_exc()
                trial += 1
        return None

    def _post(self, url, headers: Dict = None, **kwargs):
        headers = self.COMMON_HEADER.copy() if headers is None else update_header(headers,self.COMMON_HEADER)
        trial = 0
        while trial < self.maxTrial:
            try:
                return requests.post(url, headers=headers, timeout=5, **kwargs)
            except:
                traceback.print_exc()
                trial += 1
        return None
