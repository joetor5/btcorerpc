# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

BTCORE_HOME = os.getenv("BTCORE_HOME")
BTCORE_HOME = Path(BTCORE_HOME) if BTCORE_HOME else Path.home()

def create(logger_name):

    set_logging = True if os.getenv("BTCORERPC_LOG") == "1" else False
    set_logging_console = True if os.getenv("BTCORERPC_LOG_CONSOLE") == "1" else False
    set_logging_debug = True if os.getenv("BTCORERPC_LOG_DEBUG") == "1" else False

    logging_level = logging.CRITICAL if not set_logging else logging.INFO
    if set_logging_debug:
        logging_level = logging.DEBUG

    log_file = f"{logger_name.split('.')[1]}.log"
    log_dir = BTCORE_HOME / ".btcore"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    logger_format = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(Path.joinpath(log_dir, log_file), maxBytes=10000000, backupCount=3)
    file_handler.setFormatter(logger_format)
    logger.addHandler(file_handler)

    if set_logging_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logger_format)
        logger.addHandler(console_handler)

    return logger
