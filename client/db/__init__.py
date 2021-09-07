from client.vlogger import logger

logger = logger.getChild("db")

class DataDB():
    def __init__(self):
        self.db = {}




from client.db import character_table as character_db
from client.db import item_table as item_db
from client.db import stage_table as stage_db
from client.db import gacha_table as gacha_db