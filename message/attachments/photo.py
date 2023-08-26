from helpers import download_and_save
from vk_api import VkUpload, VkApi
from const import PHOTOS_PATH


class Photo:
    def __init__(self):
        self.upload: VkUpload = None
        self.path: str = None
        self.name: str = None
        self.filename: str = None

    def prepare_to_send(self, vk: VkApi, path: str):
        self.upload = VkUpload(vk)
        self.path = path
    
    def send(self) -> str:
        photo = self.upload.photo_messages(self.path)[0]
        return f"photo{photo['owner_id']}_{photo['id']}"

    def prepare_to_download(self, filename: str, url: str):
        self.filename = filename
        self.path = PHOTOS_PATH + filename
        self.url = url

    def download(self):
        download_and_save(self.path, self.url)

    def __str__(self):
        return self.filename