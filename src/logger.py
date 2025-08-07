
import logging
import os
import sys

def configure_logger(name: str = __name__) -> logging.Logger:
    
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    print('log_level_name', log_level_name)
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if log_level_name not in valid_levels:
        log_level_name = "INFO"

    log_level = getattr(logging, log_level_name)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
