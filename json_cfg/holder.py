import json
from random import choice
from json_cfg.filenames import *


class JsonMessagesHolder:
    # TODO: return msg structs
    def __init__(self):
        with open(MESSAGES) as file:
            self.messages = json.load(file)

    def generate_random_message(self):
        todo = choice([self.get_random_sticker, self.get_random_sticker, self.get_random_message,
                       self.get_random_message])
        return todo()

    def get_random_sticker(self):
        return choice(self.messages["stickers"])

    def get_random_voice(self):
        return choice(self.messages["voice-messages"])

    def get_random_message(self):
        return choice(self.messages["messages"])


class RunConfig:
    def __init__(self):
        with open(CONFIG) as file:
            info = json.load(file)
        self.token = info["token"]
        self.conference_ids_to_monitor = info["conference-ids-to-monitor"]