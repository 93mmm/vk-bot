from helpers import download_and_save
from vk_api import VkUpload, VkApi
from const import DOCS_PATH


class Doc:
    def __init__(self, ):
        self.upload: VkUpload = None
        self.path: str = None
        self.name: str = None
        self.filename: str = None

    def prepare_to_send(self, vk: VkApi, path: str):
        self.upload = VkUpload(vk)
        self.path = path

    def send(self) -> str:
        doc = self.upload.document(self.path)["doc"]
        return f"doc{doc['owner_id']}_{doc['id']}"

    def prepare_to_download(self, filename: str, url: str):
        self.filename = filename
        self.path = DOCS_PATH + filename
        self.url = url

    def download(self):
        download_and_save(self.path, self.url)

    def __str__(self):
        return self.filename
