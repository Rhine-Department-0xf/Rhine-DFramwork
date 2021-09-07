import logging

from colorlog import ColoredFormatter

logger = logging.getLogger("ArkClient")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter_console = ColoredFormatter(
    "%(log_color)s%(levelname)s: %(name)s.%(funcName)s -> %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'bold_yellow',
        'ERROR': 'bold_red',
        'CRITICAL': 'bold_red,bg_white',
    },
    secondary_log_colors={},
    style='%'

)
ch.setFormatter(formatter_console)
logger.addHandler(ch)