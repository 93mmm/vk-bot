from os import path
from sys import exit
from include.const import *


def check_files():
    messages = read_data_from_json(MESSAGES_FILE)["messages"]
    for el in messages:
        el = el["photos"]
        for photo in el:
            if not path.exists(PHOTOS_PATH + photo):
                print(PHOTOS_PATH + photo, "is not exists")
                exit()


def renew_logs_files():
    writer = 
