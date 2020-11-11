from typing import Final, Dict
import logging.config

LEVEL: Final = "info"

CONFIG: Dict = {
    "version": 1,
    "app": {
        "level": LEVEL,
    },
    "aiohttp.access": {
        "level": LEVEL,
    },
}


def install_log() -> None:
    logging.config.dictConfig(CONFIG)
