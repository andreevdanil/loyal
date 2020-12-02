import logging.config
from typing import Final

__all__ = ("setup_logging",)

LEVEL: Final[str] = "INFO"
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

ACCESS_LOG_FORMAT: Final[str] = (
    'remote_addr="%a" '
    'user_agent="%{User-Agent}i" '
    'protocol="%r" '
    'response_code="%s" '
    'request_time="%Tf" '
)

CONFIG: Final[dict] = {
    "version": 1,
    "disable_existing_loggers": True,
    "loggers": {
        "root": {
            "level": LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "app": {
            "level": LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
        "gunicorn.error": {
            "level": LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": LEVEL,
            "handlers": ["access"],
            "propagate": False,
        },
    },
    "handlers": {
        "default": {
            "level": LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
            ],
        },
        "console": {
            "level": LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
            ],
        },
        "access": {
            "level": LEVEL,
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
            ],
        },
    },
    "formatters": {
        "default": {
            "format": (
                'time="%(asctime)s" '
                'level="%(levelname)s" '
                'logger="%(name)s" '
                'service_name="%(service_name)s" '
                'pid="%(process)d" '
                'request_id="%(request_id)s" '
                'message="%(message)s" '
            ),
            "datefmt": DATETIME_FORMAT,
        },
        "access": {
            "format": (
                'time="%(asctime)s" '
                'level="%(levelname)s" '
                'logger="%(name)s" '
                'service_name="%(service_name)s" '
                'pid="%(process)d" '
                "%(message)s "
            ),
            "datefmt": DATETIME_FORMAT,
        },
    },
    "filters": {
        "service_name": {
            "()": "loyal.log.ServiceNameFilter",
        },
    },
}


class ServiceNameFilter(logging.Filter):

    def __init__(self, name: str = ""):
        self.service_name = "loyal"

        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "service_name", self.service_name)

        # noinspection PyTypeChecker
        return super().filter(record)


def setup_logging() -> None:
    logging.config.dictConfig(CONFIG)
