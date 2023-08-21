from os import path
from sys import exit

from tests.paths import *
import json_cfg
import logger


def renew_logs_files():
    files = logger.LogsWriter()
    files.renew_files()


def check_files():
    messages = json_cfg.JsonMessagesHolder().messages
    to_exit = False
    for el in messages["messages"]:
        el = el["photos"]
        for photo in el:
            if not path.exists(PHOTOS_PATH + photo):
                print(f"WARNING File {PHOTOS_PATH}{photo} is not exists")
                to_exit = True
    for voice in messages["voice-messages"]:
        if not path.exists(VOICE_PATH + voice):
            print(f"WARNING File {VOICE_PATH}{voice} is not exists")
            to_exit = True
    if to_exit:
        exit()


def test():
    # TODO: add python unittests
    check_files()
    renew_logs_files()
