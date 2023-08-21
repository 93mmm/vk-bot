import json
from random import choice

MESSAGES = "files/json/messages.json"


class JsonMessagesHolder:
    # TODO: return msg structs
    def __init__(self):
        with open(MESSAGES) as file:
            self.messages = json.load(file)

    def generate_random_message(self):
        def get_random_sticker():
            return choice(self.messages["stickers"])

        def get_random_voice():
            return choice(self.messages["voice-messages"])

        def get_random_message():
            return choice(self.messages["messages"])

        todo = choice([get_random_sticker,
                       get_random_voice,
                       get_random_message,
                       get_random_message])
        return todo()

    def append_sticker(self, sticker_id: int):
        self.messages["stickers"].append(sticker_id)
        self.write_changes()

    def append_voice_message(self, file: str):
        self.messages["voice-messages"].append(file)
        self.write_changes()

    def append_message(self):
        # TODO: edit
        obj_to_paste = dict()
        obj_to_paste["message"] = str()
        obj_to_paste["photos"] = list()
        obj_to_paste["files"] = list()
        self.messages["messages"].append(obj_to_paste)
        self.write_changes()

    def write_changes(self):
        with open(MESSAGES, "w") as file:
            file.write(json.dumps(self.messages, indent=4))
