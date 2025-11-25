import logging
import logging.config
from pathlib import Path

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "simple": {
                "format": "%(levelname)s: %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "INFO"
            },
            "file_debug": {
                "class": "logging.FileHandler",
                "filename": "logs/debug.log",
                "formatter": "standard",
                "level": "DEBUG",
            },
        },

        "root": {
            "handlers": ["console", "file_debug"],
            "level": "DEBUG",
        },

        # Additional Control: You can override individual module logging levels
        "loggers": {
            "application.routing": {"level": "DEBUG"},
            "application.topology": {"level": "INFO"},
            "infrastructure.repository": {"level": "INFO"},
        }
    }

    logging.config.dictConfig(logging_config)