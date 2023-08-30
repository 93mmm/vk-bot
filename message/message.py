from helpers import download_and_save
from const import DOCS_PATH, PHOTOS_PATH, VOICE_PATH, NOT_FOUND
from structs import ConversationCaches, LinkCaches

from vk_api import VkUpload, VkApi
from random import randint
from datetime import datetime
from threading import Thread

class Attachment:
    def __init__(self):
        self.upload: VkUpload = None
        self.path: str = None
        self.title: str = None
    
    def prepare_to_send(self, vk: VkApi, title: str):
        self.upload = VkUpload(vk)
        self.title = title
        self.path = self.get_folder() + title

    def prepare_to_download(self, title: str, url: str):
        self.url = url
        self.title = title
        self.path = self.get_folder() + title

    def download(self):
        th = Thread(target=download_and_save, args=[self.path, self.url])
        th.start()
    
    def get_folder(self) -> str:
        t = type(self)
        if t == Doc:
            return DOCS_PATH
        if t == Photo:
            return PHOTOS_PATH
        if t == Voice:
            return VOICE_PATH
        raise Exception

    def __str__(self):
        return self.title


class Doc(Attachment):
    def __init__(self):
        super().__init__()

    def get_link(self) -> str:
        cache = LinkCaches()
        link = cache.get_link(self.path)
        if link == NOT_FOUND:
            doc = self.upload.document(self.path, title=self.title)["doc"]
            link = f"doc{doc['owner_id']}_{doc['id']}"
            cache.add_link(self.path, link)
        return link


class Photo(Attachment):
    def __init__(self):
        super().__init__()
    
    def get_link(self) -> str:
        cache = LinkCaches()
        link = cache.get_link(self.path)
        if link == NOT_FOUND:
            photo = self.upload.photo_messages(self.path)[0]
            link = f"photo{photo['owner_id']}_{photo['id']}"
            cache.add_link(self.path, link)
        return link


class Voice(Attachment):
    def __init__(self):
        super().__init__()
    
    def get_link(self) -> str:
        cache = LinkCaches()
        link = cache.get_link(self.path)
        if link == NOT_FOUND:
            voice = self.upload.audio_message(self.path)["audio_message"]
            link = f"audio_message{voice['owner_id']}_{voice['id']}"
            cache.add_link(self.path, link)
        return link


class TextMessage:
    def __init__(self, peer_id: int, attachments: list[Voice | Doc | Photo], text="", sticker_id=0):
        self.peer_id: int = None
        self.attachments: list[Voice | Doc | Photo] = None
        self.text: str = None
        self.sticker_id: int = None

        self.peer_id = peer_id
        self.attachments = attachments
        self.text = text
        self.sticker_id = sticker_id
    
    def send(self, api):
        for index, element in enumerate(self.attachments):
            self.attachments[index] = self.attachments[index].get_link()
        api.messages.send(peer_id=self.peer_id, 
                          random_id=randint(0, 100000),
                          message=self.text, 
                          attachment=",".join(self.attachments),
                          sticker_id=self.sticker_id)

    def __str__(self):
        output = list()
        if self.text != "":
            output.append(f"Text: {self.text}")
        if self.sticker_id != 0:
            output.append(f"Sticker: {self.sticker_id}")

        output.append(f"To: {self.peer_id}")
        atts = "Attachments"
        if len(self.attachments) != 0:
            attachments = " | ".join(list(map(str, self.attachments)))
            output.append(f"{atts}: {attachments}")
        output.append(f"At the time: {datetime.now()}\n\n")

        return "\n".join(output)
