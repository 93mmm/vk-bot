from include.log_data import *
from os import path

def check_files():
    messages = MessagesJsonHolder().messages["messages"]
    for el in messages:
        el = el["photos"]
        for photo in el:
            if not path.exists(PHOTOS_PATH + photo):
                print(PHOTOS_PATH + photo, "is not exists")
                exit()


def renew_logs_files():
    files = LogsWriter()
    files.renew_files()


def test():
    check_files()
    renew_logs_files()
    print("TESTS PASSED")