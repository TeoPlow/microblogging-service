import logging
import logging.config
import sys
import colorama
from app.config import Config


class ColoredFormatter(logging.Formatter):
    """
    Цветные логи :)
    """

    COLORS = {
        logging.DEBUG: colorama.Fore.WHITE,
        logging.INFO: colorama.Fore.CYAN,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Fore.MAGENTA,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, colorama.Fore.RESET)
        record.color = color
        message = super().format(record)
        return f"{color}{message}{colorama.Style.RESET_ALL}"


def configure_logger():
    """
    Конфигуратор логгера со всеми его настройками и форматированием.
    """
    colorama.init()

    format_str = (
        "(%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - "
        "%(message)s)"
    )
    datefmt = "%Y-%m-%dT%H:%M:%S"

    formatters = {
        "console": {
            "()": ColoredFormatter,
            "format": format_str,
            "datefmt": datefmt,
        },
        "file": {"format": format_str, "datefmt": datefmt},
    }

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "stream": sys.stdout,
            "level": Config.LOG_LEVEL,
        }
    }

    if Config.LOG_SAVE_TO_FILE:
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "file",
            "filename": "logfile.log",
            "level": Config.LOG_LEVEL,
        }

    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "loggers": {
            "": {
                "handlers": list(handlers.keys()),
                "level": Config.LOG_LEVEL,
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(logger_config)


configure_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Возвращает логгер для добавление его в код.
    """
    return logging.getLogger(name)
