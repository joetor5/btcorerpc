# Copyright (c) 2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def create(logger_name):
    log_dir_file = logger_name.split(".")
    log_file = f"{log_dir_file[1]}.log"
    log_dir = f".{log_dir_file[0]}"
    log_dir = Path.joinpath(Path.home() / log_dir)
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger_format = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(Path.joinpath(log_dir, log_file), maxBytes=10000000, backupCount=3)
    file_handler.setFormatter(logger_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logger_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
