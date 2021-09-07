import base64
import hashlib
import hmac
import io
import json
import string
import random
import time
import zipfile
import zlib
import datetime
import binascii

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

U8_HMAC_SHA1_KEY = "91240f70c09a08a6bc72af1a5c8d4670"
LOG_TOKEN_KEY = "pM6Umv*^hVQuB6t&{login_time}"
DEFAULT_BATTLE_DATA_HASH_KEY = "62AE221E4C5D4CAD4B851D7380F4ED2C"
U8_LOGIN_DATA = "account={account}&captcha=&deviceId={device_id}&password={password}&platform={platform}"
U8_AUTH_DATA = "token={token}"
U8_PING_DATA = "token={token}"
U8_GET_TOKEN_DATA = "appId={app_id}&channelId={channel_id}" \
                    "&deviceId={device_id}&deviceId2={device_id2}&deviceId3={device_id3}" \
                    "&extension={extension}" \
                    "&platform={platform}&subChannel={sub_channel}&worldId={world_id}"
CHAT_MASK = "UITpAi82pHAWwnzq" \
            "HRMCwPonJLIB3WCl"


def get_random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def get_datetime_tuple_from_timestamp(timestamp):
    date_time = datetime.datetime.fromtimestamp(int(timestamp))
    return (date_time.year, date_time.month, date_time.day,
            date_time.hour, date_time.minute, date_time.second)


def get_md5(src):
    return hashlib.md5(src.encode()).hexdigest()


# aes-128-cbc encrypt
def rijndael_encrypt(data, key, iv):
    aes_obj = AES.new(key, AES.MODE_CBC, iv)
    encrypt_buf = aes_obj.encrypt(pad(data, AES.block_size))
    return encrypt_buf


# aes-128-cbc decrypt
def rijndael_decrypt(data, key, iv):
    aes_obj = AES.new(key, AES.MODE_CBC, iv)
    decrypt_buf = aes_obj.decrypt(data)
    return unpad(decrypt_buf, AES.block_size)


def get_u8_login_sign(account, password, device_id, platform):
    data = U8_LOGIN_DATA.format(account=account,
                                device_id=device_id,
                                password=password,
                                platform=platform)
    return hmac.new(U8_HMAC_SHA1_KEY.encode(), data.encode(), hashlib.sha1).hexdigest()


def get_u8_auth_sign(access_token):
    data = U8_PING_DATA.format(token=access_token)
    return hmac.new(U8_HMAC_SHA1_KEY.encode(), data.encode(), hashlib.sha1).hexdigest()


def get_u8_ping_sign(access_token):
    data = U8_PING_DATA.format(token=access_token)
    return hmac.new(U8_HMAC_SHA1_KEY.encode(), data.encode(), hashlib.sha1).hexdigest()


def get_u8_gettoken_sign(app_id, channel_id,
                         device_id, device_id2, device_id3,
                         extension,
                         platform, sub_channel, world_id):
    extension_text = json.dumps(extension).replace(" ", "")
    data = U8_GET_TOKEN_DATA.format(app_id=app_id,
                                    channel_id=channel_id,
                                    device_id=device_id,
                                    device_id2=device_id2,
                                    device_id3=device_id3,
                                    extension=extension_text,
                                    platform=platform,
                                    sub_channel=sub_channel,
                                    world_id=world_id)
    return hmac.new(U8_HMAC_SHA1_KEY.encode(), data.encode(), hashlib.sha1).hexdigest()


def decrypt_battle_data(data, login_time):
    battle_data = data[:-32:]
    battle_data_array = bytearray.fromhex(battle_data)
    iv = data[-32::]
    iv_array = bytearray.fromhex(iv)
    key_array = bytearray.fromhex(get_md5(LOG_TOKEN_KEY.format(login_time=login_time)))
    return rijndael_decrypt(battle_data_array, key_array, iv_array).decode()


# todo not test yet
def encrypt_battle_data(data, login_time):
    iv = bytearray(get_random_string(16).encode())
    key_array = bytearray.fromhex(get_md5(LOG_TOKEN_KEY.format(login_time=login_time)))
    return binascii.hexlify(rijndael_encrypt(data.encode(), key_array, iv) + iv).decode().upper()


def get_battle_data_access(login_time, hash_key=DEFAULT_BATTLE_DATA_HASH_KEY):
    return get_md5(hash_key + str(login_time)).upper()


def encrypt_battle_id(battle_id):
    data = bytearray(battle_id.encode())
    for i in range(len(data)):
        data[i] += 7
    return base64.b64encode(data).decode()


def decrypt_is_cheat(is_cheat):
    data = bytearray(base64.b64decode(is_cheat))
    for i in range(len(data)):
        data[i] -= 7
    return data.decode()


def decrypt_battle_replay(battle_replay):
    encoded_data = base64.b64decode(battle_replay)
    with zipfile.ZipFile(io.BytesIO(encoded_data), "r") as z_file:
        # for fileinfo in z_file.infolist():
        #     print(z_file.read(fileinfo).decode())
        return z_file.read("default_entry").decode()


# todo not tested yet
def encrypt_battle_replay(battle_replay):
    timestamp = json.loads(battle_replay)["timestamp"]
    string_io = io.BytesIO()
    with zipfile.ZipFile(string_io, "w", zipfile.ZIP_DEFLATED) as f:
        f.writestr(zipfile.ZipInfo(filename="default_entry",
                                   date_time=get_datetime_tuple_from_timestamp(timestamp)),
                   battle_replay,
                   compress_type=zipfile.ZIP_DEFLATED)
    return base64.b64encode(string_io.getvalue()).decode()


# TextAsset 资源解密
# Torappu_DB_CrypticConverter_A__DecodeInternal
def decrypt_text_asset(binarydata):
    # TextAsset资源使用aes-128-cbc加密算法, 加密key是CHAT_MASK前16字节
    aes_key = bytearray(CHAT_MASK[:16].encode())
    aes_iv  = bytearray(16)
    buf = binarydata[:16]
    mask = bytearray(CHAT_MASK[16:].encode())
    for i in range(16):
        aes_iv[i] = buf[i] ^ mask[i]
    return rijndael_decrypt(binarydata[16:], aes_key, aes_iv)

class mscorlib_Random():
    MBIG = 2147483647
    MSEED = 161803398
    MZ = 0

    def __init__(self, seed):
        self.seed = seed
        self.seed_array = [0 for i in range(56)]

        self.inext = 0
        self.inextp = 0
        self.__init_seed_array()

    def __init_seed_array(self):
        ii = 0
        mj, mk = 0, 0
        mj = self.MSEED - abs(self.seed)
        self.seed_array[55] = mj
        mk = 1
        for i in range(1, 55):
            ii = (21 * i) % 55
            self.seed_array[ii] = mk
            mk = mj - mk
            if (mk < 0):
                mk += self.MBIG
            mj = self.seed_array[ii]
        for k in range(1, 5):
            for i in range(1, 56):
                self.seed_array[i] -= self.seed_array[1 + (i + 30) % 55]
                if self.seed_array[i] < 0:
                    self.seed_array[i] += self.MBIG
        self.inext = 0
        self.inextp = 31

    @classmethod
    def init_with_time(cls):
        return cls(int(time.time()))

    def sample(self):
        self.inext = 1 if (self.inext + 1) >= 56 else self.inext + 1
        self.inextp = 1 if (self.inextp + 1) >= 56 else self.inextp + 1
        ret_val = self.seed_array[self.inext] - self.seed_array[self.inextp]
        if ret_val < 0:
            ret_val += self.MBIG
        self.seed_array[self.inext] = ret_val
        return ret_val * (1 / self.MBIG)

    def next_double(self):
        return self.sample()
