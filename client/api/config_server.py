import json

from client.api import http_client,logger
from client import config
NETWORK_CONFIG_URL = "https://ak-conf.hypergryph.com/config/prod/{}/network_config"
REMOTE_CONFIG_URL = "https://ak-conf.hypergryph.com/config/prod/{}/remote_config"
VERSION_URL = "https://ak-conf.hypergryph.com/config/prod/official/Android/version"

logger = logger.getChild("config_server")


def get_version():
    logger.info("getting production version")
    data = http_client.get(None,VERSION_URL)
    if data is None:
        return
    config.ProductionConfig.clientVersion = data["clientVersion"]
    config.ProductionConfig.assetsVersion = data["resVersion"]
    logger.info("finish")
    return data["resVersion"],data["clientVersion"]

def get_network(config_server_name):
    logger.info("getting network version")
    data = http_client.get(None, NETWORK_CONFIG_URL.format(config_server_name))
    if data is None:
        return
    json_data = json.loads(data["content"])
    config.NetworkConfig.version = json_data["configVer"]
    config.NetworkConfig.network = json_data["configs"][json_data["funcVer"]]["network"]
    config.NetworkConfig.update_server_url()
    logger.info("finish")
    return json_data
