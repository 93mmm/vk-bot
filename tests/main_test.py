from os import path
from sys import exit

from tests.paths import *
import json_cfg
import logger


def renew_logs_files():
    files = logger.LogsWriter()
    files.renew_files()


def check_files():
    def warn(path):
        print(f"WARNING: File {path} is not exists")

    messages = json_cfg.JsonMessagesHolder().messages
    to_exit = False
    for msg in messages:
        for photo in msg["photos"]:
            if not path.exists(PHOTOS_PATH + photo):
                warn(PHOTOS_PATH + photo)
                to_exit = True
        for doc in msg["files"]:
            if not path.exists(DOCS_PATH + doc):
                warn(DOCS_PATH + doc)
                to_exit = True
        if msg["voice-message"] != "" and not path.exists(VOICE_PATH + voice):
            warn(VOICE_PATH + voice)
            to_exit = True

    if to_exit:
        exit()


def test():
    check_files()
    renew_logs_files()
