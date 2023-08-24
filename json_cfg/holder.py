import json
from random import choice
from structs import TextMessage, Voice, Doc, Photo
from vk_api import VkApi

MESSAGES = "files/json/messages.json"

PHOTOS_PATH = "files/assets/photos/"
VOICE_PATH = "files/assets/voice/"
DOCS_PATH = "files/assets/files/"


def save_into_json_file(path: str, info: dict):
    with open(path, "w") as file:
        file.write(json.dumps(info, indent=4))


class JsonMessagesHolder:
    def __init__(self):
        with open(MESSAGES) as file:
            self.messages = json.load(file)

    def generate_random_message(self, vk: VkApi, peer_id: int):
        # TODO: rewrite
        selected = choice(self.messages)
        attachments = list()
        text = selected["text"]
        sticker_id = selected["sticker_id"]

        for filename in selected["photos"]:
            photo = Photo()
            photo.prepare_to_send(vk, PHOTOS_PATH + filename)
            attachments.append(photo)
        for filename in selected["files"]:
            doc = Doc()
            doc.prepare_to_send(vk, DOCS_PATH + filename)
            attachments.append(doc)
        for filename in selected["voice-message"]:
            vm = Voice()
            vm.prepare_to_send(vk, VOICE_PATH + filename)
            attachments.append(vm)

        return TextMessage(peer_id, attachments, text, sticker_id)

    def add_new_message(self, text="", sticker_id=0, attachments=list()):
        # TODO: rewrite
        new_message = dict()
        if text != "":
            new_message["text"] = text
        if sticker_id != 0:
            new_message["sticker_id"] = sticker_id
        for el in attachments:
            if type(el) == Voice:
                new_message["voice-message"] = el.path
            elif type(el) == Doc:
                new_message["files"] = el.path
            elif type(el) == Photo:
                new_message["photos"] = el.path

        save_into_json_file(MESSAGES, new_message)


class JsonDialogNamesHolder:
    def __init__(self):
        pass

    def get_name(self, name):
        pass
