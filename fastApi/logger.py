#!/usr/bin/python3

import logging
import logging.handlers
import time

LOG_FILENAME = "{}.log".format(time.strftime("%Y%m%d", time.localtime()))
logger = logging.getLogger()
"""
日志模块
"""


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] - %(pathname)s %(levelname)s: %(message)s [Line: %(lineno)d]"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
