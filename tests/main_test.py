from os import path
from sys import exit

from tests.paths import *
import json_cfg
import logger


def renew_logs_files():
    files = logger.LogsWriter()
    files.renew_files()


def check_files():
    red = "\033[1;31;40m"
    red_end = "\033[0m"
    messages = json_cfg.JsonMessagesHolder().messages
    for el in messages["messages"]:
        el = el["photos"]
        for photo in el:
            if not path.exists(PHOTOS_PATH + photo):
                print(f"{red}WARNING File {PHOTOS_PATH}{photo} is not exists{red_end}")
                exit()
    for voice in messages["voice-messages"]:
        if not path.exists(VOICE_PATH + voice):
            print(f"{red}WARNING File {VOICE_PATH}{voice} is not exists{red_end}")
            exit()
    # TODO: check voices


def test():
    check_files()
    renew_logs_files()
    print("TESTS PASSED")
