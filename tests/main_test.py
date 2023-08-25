from os import path
from sys import exit

from structs.config.messages import JsonMessagesHolder


PHOTOS_PATH = "files/assets/photos/"
VOICE_PATH = "files/assets/voice/"
DOCS_PATH = "files/assets/files/"


# def renew_logs_files():
#     files = LogsWriter()
#     files.renew_files()


def check_files():
    def warn(f: str):
        print(f"WARNING: File {f} is not exists")

    messages = JsonMessagesHolder().messages
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
        voice = msg["voice-message"]
        if voice != "" and not path.exists(VOICE_PATH + voice):
            warn(VOICE_PATH + voice)
            to_exit = True

    if to_exit:
        exit()


def test():
    pass
    #check_files()
    # renew_logs_files()
