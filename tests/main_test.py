from os import path

from const import *
from structs import JsonMessagesHolder
from helpers import read_json, write_lines, exit_from_script


def check_and_warn_about_errors_in_json_files():
    # TODO: -change-statuses warn (haven't selected satatuses)
    # TODO: rebase tests into helpers
    pass


def renew_logs_files():
    for el in [EXCEPTIONS_FILE, RECEIVED_MESSAGES_FILE, SENT_MESSAGES_FILE]:
        write_lines(el, [], "\n")


def check_files():
    def warn(f: str):
        print(f"WARNING: File {f} is not exists")

    messages = JsonMessagesHolder().messages
    to_exit = False
    for msg in messages:
        if "photos" in msg:
            for photo in msg["photos"]:
                if not path.exists(PHOTOS_PATH + photo):
                    warn(PHOTOS_PATH + photo)
                    to_exit = True
        if "files" in msg:
            for doc in msg["files"]:
                if not path.exists(DOCS_PATH + doc):
                    warn(DOCS_PATH + doc)
                    to_exit = True
        if "voice-message" in msg:
            if not path.exists(VOICE_PATH + msg["voice-message"]):
                warn(VOICE_PATH + msg["voice-message"])
                to_exit = True

    if to_exit:
        exit_from_script()


def test():
    renew_logs_files()
    check_files()
