from json_message_holder.filenames import *
import json

class JsonMessagesHolder:
    def __init__(self):
        with open(MESSAGES) as file:
            self.messages = json.load(file)

    def get_random_message(self):
        pass # TODO: choice sticker or message or voice
        # TODO: return message as class
