from helpers import download_and_save
from vk_api import VkUpload, VkApi
from const import VOICE_PATH


class Voice:
    def __init__(self):
        self.upload: VkUpload = None
        self.path: str = None
        self.filename: str = None

    def prepare_to_send(self, vk: VkApi, path: str):
        self.upload = VkUpload(vk)
        self.path = path

    def send(self) -> str:
        voice = self.upload.audio_message(self.path)["audio_message"]
        return f"audio_message{voice['owner_id']}_{voice['id']}"

    def prepare_to_download(self, filename: str, url: str):
        self.filename = filename
        self.path = VOICE_PATH + filename
        self.url = url

    def download(self):
        download_and_save(self.path, self.url)

    def __str__(self):
        return self.filename