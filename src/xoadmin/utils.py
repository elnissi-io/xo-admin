import logging
import os

from colorlog import ColoredFormatter

# Global logger variable
logger = None


def init_logging():
    global logger
    if logger is None:
        debug_mode = os.getenv("DEBUG", "").lower() in ["true", "1"]
        logger = logging.getLogger("xoadmin")
        logger.setLevel(logging.INFO)

        formatter = ColoredFormatter(
            fmt=(
                "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:\033[97m%(lineno)d\033[0m - \033[97m%(message)s\033[0m"
                if debug_mode
                else "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - \033[97m%(message)s\033[0m"
            ),
            datefmt=None,  # You can specify your date format here
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            secondary_log_colors={},
            style="%",
        )

        # Handler for printing logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Adjusted formatter to include module names

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


def get_logger(module_name=None):
    global logger
    if logger is None:
        init_logging()
    if module_name:
        # Create or retrieve a logger with the name specified by module_name
        module_logger = logging.getLogger(module_name)
        module_logger.handlers = logger.handlers  # Copy handlers from the global logger
        module_logger.setLevel(logger.level)  # Ensure logging level consistency
        return module_logger
    return logger
