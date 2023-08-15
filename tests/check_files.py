from os import path
from sys import exit
import json_message_holder
from tests.paths import *


def check_files():
    messages = json_message_holder.JsonMessagesHolder().messages["messages"]
    for el in messages:
        el = el["photos"]
        for photo in el:
            if not path.exists(PHOTOS_PATH + photo):
                print(PHOTOS_PATH + photo, "is not exists")
                exit()