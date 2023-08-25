from random import choice
from vk_api import VkApi

from message import *
from structs.events.received_message import ReceivedMessage
from helpers import read_json, write_json

MESSAGES = "files/json/messages.json"

PHOTOS_PATH = "files/assets/photos/"
VOICE_PATH = "files/assets/voice/"
DOCS_PATH = "files/assets/files/"


class JsonMessagesHolder:
    def __init__(self):
        self.messages: list = None

        self.messages = read_json(MESSAGES)

    def generate_random_message(self, vk: VkApi, peer_id: int):
        # TODO: rewrite with checks
        selected = choice(self.messages)
        text = ""
        sticker_id = 0
        attachments = list()
        if "text" in selected:
            text = selected["text"]
        if "sticker_id" in selected:
            sticker_id = selected["sticker_id"]
        if "photos" in selected:
            for filename in selected["photos"]:
                photo = Photo()
                photo.prepare_to_send(vk, PHOTOS_PATH + filename)
                attachments.append(photo)
        if "files" in selected:
            for filename in selected["files"]:
                doc = Doc()
                doc.prepare_to_send(vk, DOCS_PATH + filename)
                attachments.append(doc)
        if "voice-message" in selected:
            for filename in selected["voice-message"]:
                vm = Voice()
                vm.prepare_to_send(vk, VOICE_PATH + filename)
                attachments.append(vm)

        return TextMessage(peer_id, attachments, text, sticker_id)

    def add_new_message(self, msg: ReceivedMessage):
        # TODO: rewrite
        new_message = dict()
        if msg.message_text != "":
            new_message["text"] = msg.message_text
        if msg.sticker_id != 0:
            new_message["sticker_id"] = msg.sticker_id
        for el in msg.attachments:
            if type(el) == Voice:
                new_message["voice-message"] = el.path
            elif type(el) == Doc:
                new_message["files"] = el.path
            elif type(el) == Photo:
                new_message["photos"] = el.path
        if new_message != dict() and not new_message in self.messages:
            self.messages.append(new_message)

            write_json(MESSAGES, self.messages)
