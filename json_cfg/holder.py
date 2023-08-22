import json
from random import choice
from structs import TextMessage, Voice, Doc, Photo

MESSAGES = "files/json/messages.json"

PHOTOS_PATH = "files/assets/photos/"
VOICE_PATH = "files/assets/voice/"
DOCS_PATH = "files/assets/files/"



class JsonMessagesHolder:
    def __init__(self):
        with open(MESSAGES) as file:
            self.messages = json.load(file)

    def generate_random_message(self, vk, peer_id):
        selected = choice(self.messages)
        attachments = list()
        text = selected["text"]
        sticker_id = selected["sticker_id"]

        for filename in selected["photos"]:
            attachments.append(Photo(vk, PHOTOS_PATH + filename))
        for filename in selected["files"]:
            attachments.append(Doc(vk, DOCS_PATH + filename))
        for filename in selected["voice-message"]:
            attachments.append(Voice(vk, VOICE_PATH + filename))

        return TextMessage(peer_id, attachments, text, sticker_id)

    def add_new_message(self, text="", attachments=list(), sticker_id=""):
        new_message = dict()
        new_message["text"] = text
        new_message["photos"] = attachments
        new_message["files"] = attachments
        new_message["sticker_id"] = sticker_id
        new_message["voice-message"] = sattachments
        self.write_changes()

    def write_changes(self):
        with open(MESSAGES, "w") as file:
            file.write(json.dumps(self.messages, indent=4))
